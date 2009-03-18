#!/usr/bin/python
# $Id$

import os
import pygtk; pygtk.require("2.0")
import gtk.glade
import subprocess
import gobject
import time
from xml.etree import ElementTree as etree

logo_filename="logo.png"

# Opens the log file and write the name and curent data and time
logfile = open("sinthgunt.log", 'a')
logfile.writelines('****** Sinthgunt log file START - '+str(time.ctime())+' *******\n')


class sinthgunt:
    """This is a program to ease the use of ffmpeg
    on Ubuntu based machines """

    def load_conf_file(self):
        """ This function reads the configuration file and populates the
        interface with the options. 
        # bm[i][0] -- Operation description. This will appear as an entry in
        # the GUI
        # bm[i][1] -- Operation binary (eg. /usr/bin/ffmpeg or /usr/bin/cvlc)
        # bm[i][2] -- Command options before input file name
        # bm[i][4] -- Command options between input and output file names
        # bm[i][5] -- Command options after output file name (buggy, doesn't work
        # 	      with ffmpeg)
        # bm[i][6] -- Output file postfix
        """

        # Populates preset menu from XML file
        # Load XML config file
        self.parseXML()
        # local variables
        categorylist=self.categorylist
        presetlist=self.presetlist
        # connetc to menu
        actionmenu = self.wTree.get_widget("menu2")
      
        Ncategory = len(categorylist)
        self.Npreset = len(presetlist)
        counter = 0
        item = gtk.RadioMenuItem(group=None,label='')   # first, dummy item in group
        self.presetmenu1headerholder = []
        # Generate submues
        for category in categorylist:
            # add submenu for category            
            presetmenu1header = gtk.Menu()
            self.presetmenu1headerholder.append(presetmenu1header)
            presetmenu1 = gtk.MenuItem(category)
            presetmenu1.set_submenu(self.presetmenu1headerholder[counter])
            # add all presets in the category to this submenu
            for i in range(self.Npreset):
                if presetlist[i][0] == categorylist[counter]:
                    item = gtk.RadioMenuItem(group=item,label=presetlist[i][1])
                    item.connect("activate", self.menuradiobuttonselect)
                    self.presetmenu1headerholder[counter].append(item)
            self.operation_radiobutton = ''

            # show stuff in the menu
            actionmenu.append(presetmenu1)        
            self.presetmenu1headerholder[counter].show_all()
            presetmenu1.show()
            counter = counter+1

    def __init__(self):
        """ Reads the information from glade file and connects the buttons with
        the functions."""

        #Set the Glade file
        self.gladefile = "sinthgunt.glade"  
        self.wTree = gtk.glade.XML(self.gladefile) 

        #Get the Main Window, and connect the "destroy" event
        self.window = self.wTree.get_widget("MainWindow")

        if (self.window):
            # connect to label
            self.labelGuide = self.wTree.get_widget("labelGuide")
            self.labelInput = self.wTree.get_widget("labelInput")
            
            #Loads the operation combobox
            self.Operation = self.wTree.get_widget("comboboxOperation")

            #Loads the statusbar
            self.statusbar = self.wTree.get_widget("statusbar")
            context_id = self.statusbar.get_context_id("Activation")
            self.statusbar.push(context_id,"Welcome to the Sinthgunt converter!")
            
            # loads the progress bar
            self.progressbar = self.wTree.get_widget("progressbar")
            
            #Loads the configuration file
            self.load_conf_file()
            
            #Sets the default logo
            self.thumbnail = self.wTree.get_widget("thumbnail")
            self.thumbnail.set_from_file(logo_filename)

            #Create a dictionary of handles and functions
            self.dic = {#"on_chooserInput_file_set" : self.setinput,
                        "on_button_activate_clicked" : self.activate,
                        "on_button_stop_clicked"     : self.stop,
                        "MainWindow_destroy"         : self.quit_program,
                        "on_menuquit_activate"       : self.quit_program,
                        "on_menuopen_activate"       : self.menuopenfile,
                        "on_menuconvert_activate"    : self.activate,
                        "on_menuabout_activate"      : self.aboutdialog }
            
            #Do the magic connecting to the widgets
            self.wTree.signal_autoconnect(self.dic)        
            self.input = None


    def checkfile(self):
        """ This function is executed many times to check on the progress of
        the conversion. """
        
        context_id = self.statusbar.get_context_id("Activation")        
        output = ''
        try:
            output = str(self.process.stdout.read(20))
        except:
            pass
        logfile.writelines(output)
        output_split = output.split(' ')
        N=len(output_split)
        
        # Error handling
        if output.find("Could not")!=-1:
            logfile.writelines("\n ffmpeg error detected?....")
            self.statusbar.push(context_id,'ffmpeg error detected. See sinthgunt.log')

        # get the number of frames converted
        for i in range(N):
            if i>=2 and output_split[i]=='fps=':
               file_frames_completed = output_split[i-1]              
               # update progressbar
               try:
                   self.progressbar.set_fraction(float(\
                           file_frames_completed)/float(self.file_frames))
                   self.progressbar.set_text(str(file_frames_completed)+\
                           ' of '+str(self.file_frames)+' frames converted.')
               except:
                   pass

        # if no output detected, stop watching the process and write to statusbar
        if output =='':     
            self.statusbar.push(context_id,'Conversion completed!')
            self.progressbar.set_fraction(0.99999)
            self.progressbar.set_text(str(str(self.file_frames)+\
                                          ' of '+str(self.file_frames)+' frames converted.'))
            # this line would to the sames as return False: gobject.source_remove(self.source_id)          
            return False    
        else:
            return True
  
    
    
    def menuopenfile(self,widget):
        """ Defines the filters used when selecting new file."""

        fc = gtk.FileChooserDialog(title = "Select video file...",
                action = gtk.FILE_CHOOSER_ACTION_OPEN,
                buttons = (gtk.STOCK_CANCEL,
                    gtk.RESPONSE_CANCEL,
                    gtk.STOCK_OPEN,
                    gtk.RESPONSE_OK)
                )
        
        # Set input dialog mime type filters 
        filter = gtk.FileFilter()   
        filter.set_name("Videos")
        filter.add_pattern("*.avi")
        filter.add_pattern("*.AVI")
        filter.add_pattern("*.mpg")
        filter.add_pattern("*.MPG")
        filter.add_pattern("*.mp4")
        filter.add_pattern("*.MP4")
        filter.add_pattern("*.mov")
        filter.add_pattern("*.MOV")
        filter.add_pattern("*.flv")
        filter.add_pattern("*.FLV")
        filter.add_pattern("*.wmv")
        filter.add_pattern("*.WMV")
        fc.add_filter(filter)
        # all files       
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        fc.add_filter(filter)
        
        if fc.run() == gtk.RESPONSE_OK:
            self.input_from_menu = fc.get_filename()
            fc.destroy()
            test = self.setinput(widget)
        else:
            fc.destroy()
    

    
    def setinput(self, widget): 
        """ This function generates the thumbnail and saves it to the /tmp
        folder. It also extracts the information about the movie from ffmpeg
        and provides it to the screen. """

        self.input = self.input_from_menu
        temp = self.input.split('/')
        N = len(temp)        
        
        # get input basename
        input_basename = temp[N-1]
        # set thumbnail filename
        self.thumbnail_filename = "/tmp/"+str(input_basename)+".jpg"
            
        # ffmpeg tumbnail creator
        subcommand_str = "ffmpeg -y -itsoffset -5 -i "+self.input+\
                " -vcodec mjpeg -vframes 1 -an -f rawvideo -s 170x128 "+\
                self.thumbnail_filename
        subcommand = subcommand_str.split(' ')
        thumb_process = subprocess.Popen(args=subcommand, 
                        stdout=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        shell=False)

        # wait for thumbnail generation to complete
        try:
            output = str(self.thumb_process.stdout.read(100))
            logfile.writelines(output)
        except:
            pass
        thumb_process.wait()
        
        # update thumbnail
	if str(os.path.getsize(self.thumbnail_filename))!='0':
		self.thumbnail.set_from_file(self.thumbnail_filename)
        
        # get media file info
        pest = self.file_getinfo()
        
        # fill label with file info
        self.labelInput.set_text('')
        self.labelInput.set_text('Audio codec: '+str(self.audio_codec[0])+'\n'\
                                'Audio bitrate: '+str(self.audio_codec[4])+' kb/s\n'\
                                +'Video codec: '+ str(self.video_codec[0])\
                                +'\nVideo resolution: '+ str(self.video_codec[2])\
                                +'\n'+'Number of frames: '+str(self.file_frames))
        self.labelGuide.set_text(input_basename[:10]+' info:')

    
    
    def setoutput(self, widget):
        """ This functions gets the output filename from the GUI and provides
        it for the rest of the program. """
        
        self.outputtmp = self.wTree.get_widget("chooserOutput")
        self.output = self.outputtmp.get_filename()
        


    def activate(self,widget):
        """ This function starts the selected operation of the current selected
        file. """
        
        if self.input == None:
            self.no_file_selected_dialog(widget)
        else:
        
            context_id = self.statusbar.get_context_id("Activation")  
            self.statusbar.push(context_id,'Running...')
        
            #start watching output
            self.source_id = gobject.timeout_add(100, self.checkfile)
        
            # Get selected operation from menu
            operation = self.operation_radiobutton

            for i in range(self.Npreset):
                if operation == self.presetlist[i][1]:
                    # generate command line in subprocess syntax
                    subcommand = ['/usr/bin/ffmpeg','-y','-i']
                    subcommand.extend([self.input])
                    subcommand.extend(self.presetlist[i][2].split(' '))            
                    subcommand.extend([str(self.input+"."+self.presetlist[i][3])])
                    # remove empty entries ('') from the array
                    for i in range(20):
                        try:
                            subcommand.remove('')
                        except:
                            1+1 
                    # Start converting
                    self.process = subprocess.Popen(args=subcommand,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.STDOUT,shell=False)
                    
                    logfile.writelines(subcommand)



    def stop(self,widget):
        """ Tried to kill the process before it is done."""
        os.system('cat sinthgunt.log')
        try:
            os.kill(self.process.pid,9)
            logfile.writelines('Conversion stopped\n')
        except:
            pass
            
   

    def quit_program(self,widget):
        """ When the program is closed the stop function and the logfile is
        updated and program is terminated. """
        self.stop
        logfile.writelines('****** Sinthgunt log file STOP - '+str(time.ctime())+' *******\n')
        logfile.close
        gtk.main_quit()



    def file_getinfo(self):
        """ This function finds the information about the current selected
        file. Displays number of frames, audio codec and video codec."""
        self.audio_codec = ['','','','','']
        self.video_codec = ['','','','','']
        self.file_frames = 0
        command = ["ffmpeg","-i",self.input]

        process = subprocess.Popen(args=command,stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,stderr=subprocess.STDOUT)

        flag = 1
        while flag == 1:   
            try:       
                output = str(process.stdout.read(2000))        
            except:
                break

            if output != '\n' and output != '':
                logfile.writelines(output)
                output_split = output.split(' ')
                N=len(output_split)
                for i in range(N):

                    # Find length of audio/video file in seconds            
                    if output_split[i]=='Duration:':
                        file_length_min=output_split[i+1]
                        file_length_min_split=file_length_min.split(':')
                        temp = file_length_min_split[2].split('.')
                        file_length_min_split[2]=temp[0]
                        # Calculate length of file in seconds               
                        file_length_sec=3600*float(file_length_min_split[0])+\
                                60*float(file_length_min_split[1])+\
                                float(file_length_min_split[2])
            
                    # Find video codec            
                    if output_split[i]=='Video:':
                        self.video_codec = [output_split[i+1].strip(','),
                                output_split[i+2].strip(','),
                                output_split[i+3].strip(',')]
                        #self.video_codec = self.video_codec.strip(',')
                    # Find frames pr. second in the file 
                    if i>=2 and output_split[i]=='tb(r)\n':
                        file_fps=output_split[i-1]
                        # Calculate total number of frames
                        self.file_frames = int(file_length_sec*float(file_fps))
                
                    # Find audio codec
                    if output_split[i]=='Audio:':
                        self.audio_codec = [output_split[i+1].strip(','),
                                output_split[i+2].strip(','),
                                output_split[i+3].strip(','),
                                output_split[i+4].strip(','),
                                output_split[i+5]]
                        flag = 0  



    def aboutdialog(self,widget):
        """ Defines the about information about the program."""
        dialogtext = "The Sinthgunt Converter - a ffmpeg gui.\
                        \nBy Thomas R. N. Jansson (tjansson@tjansson.dk) and\
                        \nKaare H. Jensen (hartvig@hartvig.de)\
                        \nSee LICENSE.TXT for License information\
                        \nSelect the video file you wish to convert from the File menu.\
                        \nTheb, select the type of conversion you want to perform from the Presets menu.\
                        \nTo start converting, press the Convert button in the main window."
        message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, dialogtext)
        message.add_button(gtk.STOCK_QUIT, gtk.RESPONSE_CLOSE)
        resp = message.run()
        if resp == gtk.RESPONSE_CLOSE:
            message.destroy()
    def no_file_selected_dialog(self,widget):
        dialogtext = "You have to select a file before you can begin converting!"
        message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, dialogtext)
        message.add_button(gtk.STOCK_QUIT, gtk.RESPONSE_CLOSE)
        resp = message.run()
        if resp == gtk.RESPONSE_CLOSE:
            message.destroy()
    # menuradiobutton
    def menuradiobuttonselect(self,widget):
        self.operation_radiobutton = ''
        counter=0
        for presetmenu1header in self.presetmenu1headerholder:
            for item in presetmenu1header:
                if item.get_active() == True:
                    self.operation_radiobutton = self.presetlist[counter][1]
                counter = counter + 1
    
    # XML PARSER FUNCTION
    def parseXML(self):
    	# load xml file
        xml_file = os.path.abspath(__file__)
        xml_file = os.path.dirname(xml_file)
        xml_file = os.path.join(xml_file, "presets.xml")
        optionsXML = etree.parse(xml_file)
        presets=[]
        row = [' ',' ',' ',' ']

	    # Iterate through presets
        for child in optionsXML.getiterator():
            if child.tag == 'label':
                row[1]=child.text
            if child.tag == 'params':
                row[2]=child.text
            if child.tag == 'extension':
                row[3]=child.text.strip(' ')
            if child.tag == 'category':
                row[0]=child.text
                presets.append(row)
                row = [' ',' ',' ',' ']
    	# Sort by category
    	presets.sort(lambda x, y: cmp(x[0],y[0]))
    	# find category list
    	categories=[presets[0][0]]
    	for row in presets:
        	if row[0]!=categories[-1]:
            		categories.append(row[0])
        
        self.presetlist=presets
        self.categorylist=categories


    
if __name__ == "__main__":
    program = sinthgunt()
    gtk.main()