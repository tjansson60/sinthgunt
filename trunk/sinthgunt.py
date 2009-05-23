#!/usr/bin/python
# $Id$

# Description     
"""This is a program to ease the use of ffmpeg on Ubuntu based machines """

import os
import pygtk; pygtk.require("2.0")
import gtk.glade
import subprocess
import gobject
import time
import sys
from xml.etree import ElementTree as etree

# Check to see if ffmpeg is installed
if os.path.exists("/usr/bin/ffmpeg"):
    print('ffmpeg found. Starting Sinthgunt...')# carry on
else:
    print('It seems, that ffmpeg is not installed on this computer. \nSee http://sinthgunt.googlecode.com for installation instructions.')
    sys.exit(0) 

# Checks for absolute or relative path
if os.path.exists("/usr/bin/sinthgunt.py"):
    DATA_DIR="/usr/share/sinthgunt/"
else:
    DATA_DIR=""


# Opens the log file and write the name and curent data and time
logfile_filename = os.path.expanduser("~/.sinthgunt.log")
logfile = open(logfile_filename, 'a')
logfile.writelines('****** Sinthgunt log file START - '+
        str(time.ctime())+' *******\n')
logo_filename=DATA_DIR+"logo.png"

class sinthgunt:

    def load_conf_file(self):
        """ This function reads the configuration xml-file and populates the
        Preset menu with the conversion options.
        """
        # Load XML config file
        self.parseXML()
        # Local variables
        categorylist=self.categorylist  # List of categories
        presetlist=self.presetlist      # List of presets in the categories
        # Connect to menu
        actionmenu = self.wTree.get_widget("menu2")
        # Constants
        Ncategory = len(categorylist) # Number of categories
        self.Npreset = len(presetlist) # Number of presets
        counter = 0     # Counter that keeps track of the categories in the categorylist
        counter2 = 0    # Counter that keeps track of the codecs in the self.preset_enabled list

        # Create first, dummy item in group. All later items are attached to this group
        item = gtk.RadioMenuItem(group=None,label='') 
        # Initialise presetmenuheaderholder, a holder for the submenues
        self.presetmenu1headerholder = []
        self.preset_enabled = []
        # Generate submenues
        for category in categorylist:
            # Add submenu for category            
            presetmenu1header = gtk.Menu()
            self.presetmenu1headerholder.append(presetmenu1header)
            presetmenu1 = gtk.MenuItem(category)
            presetmenu1.set_submenu(self.presetmenu1headerholder[counter])
            # Add all presets in the category to this submenu
            for i in range(self.Npreset):
                if presetlist[i][0] == categorylist[counter]:
                    self.preset_enabled.append('')
                    # Create radio button for the preset
                    item = gtk.RadioMenuItem(group=item,label=presetlist[i][1])
                    # What to do when the radiobutton is clicked
                    item.connect("activate", self.menuradiobuttonselect)
                    # Check to see if the codecs required by the preset are supported by the users version of ffmpeg
                    for requiredcodec in self.presetlist[i][4]:
                            flag =0
                            notfound = 1
                            for codec in self.codecs:
                                # If encoding true
                                if requiredcodec==codec[0] and codec[1]==True and flag==0: # preset will work                    
                                    notfound = 0
                                    self.preset_enabled[counter2]=True
                                # if encoding false
                                if requiredcodec==codec[0] and codec[1]==False:
                                    label =  item.get_children()[0]
                                    label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#888888')) # preset will not work - grayed out
                                    notfound = 0
                                    flag=1
                                    item.set_tooltip_text('Your version of ffmpeg does not support this preset.')
                                    self.preset_enabled[counter2]=False
                            # if codec was not found
                            if notfound==1 and flag==0:
                                    label =  item.get_children()[0]
                                    label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#888888')) # preset might work - grayed out
                                    item.set_tooltip_text('Your version of ffmpeg does not support this preset.')    
                                    self.preset_enabled[counter2]=False
                    counter2 = counter2+1
                    # add item to the headerholder
                    self.presetmenu1headerholder[counter].append(item)

            # show stuff in the menu
            actionmenu.append(presetmenu1)        
            self.presetmenu1headerholder[counter].show_all()
            presetmenu1.show()
            counter = counter+1
            
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

        # Look for Classic errors. This should be done in a separate function sometime soon
        # "Must supply at least one output file"
        for i in range(N-1):
            if i>=2 and output_split[i]=='Must=' and output_split[i+1]=='supply': # an error has occured
                self.statusbar.push(context_id,'An error has occured. See the log file for details.')               
                self.progressbar.set_fraction(0.0)
                self.progressbar.set_text('')
                return False 



        # if no output detected, stop watching the process and write to statusbar
        if output =='':     
            self.statusbar.push(context_id,'Conversion completed!')
            self.progressbar.set_fraction(0.99999)
            self.progressbar.set_text(str(str(self.file_frames)+\
                                          ' of '+str(self.file_frames)+' frames converted.'))
            # this line would do the sames as return False: gobject.source_remove(self.source_id)          
            return False    
        else:
            return True
  
    
    
    def menuopenfile(self,widget):
        """ Defines the filters used when selecting new file."""
        
        # What does fc stand for?
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
        filter.add_pattern("*.mpeg")
        filter.add_pattern("*.MPG")
        filter.add_pattern("*.MPEG")
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

        subcommand = ['ffmpeg', '-y', '-itsoffset', '-5' ,'-i' ,self.input,\
                "-vcodec","mjpeg","-vframes", "1", "-an", "-f", "rawvideo", "-s", "170x128",\
                self.thumbnail_filename]
    
        thumb_process = subprocess.Popen(args=subcommand,
                            stdout=subprocess.PIPE,stdin=subprocess.PIPE,
                            stderr=subprocess.STDOUT,shell=False)

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
        mediaFileInformation = self.file_getinfo()
        
        # fill label with file info
        self.labelInput.set_text('')
        self.labelInput.set_text('Audio codec: '+str(self.audio_codec[0])+'\n'\
                                'Audio bitrate: '+str(self.audio_codec[4])+' kb/s\n'\
                                +'Video codec: '+ str(self.video_codec[0])\
                                +'\nVideo resolution: '+ str(self.video_codec[2])\
                                +'\nVideo bitrate: '+ str(self.video_codec[3])\
                                +'\n'+'Number of frames: '+str(self.file_frames))
        self.labelGuide.set_text('Input file: '+input_basename)

    
    
    def setoutput(self, widget):
        """ This functions gets the output filename from the GUI and provides
        it for the rest of the program. """
        
        self.outputtmp = self.wTree.get_widget("chooserOutput")
        self.output = self.outputtmp.get_filename()
        


    def activate(self,widget):
        """ This function starts the selected operation of the current selected
        file. """

        # Get selected operation from menu
        operation = self.operation_radiobutton

        if self.input == None or operation =='':
            self.no_file_selected_dialog(widget)
        else:
            self.progressbar.set_fraction(0.01)
            context_id = self.statusbar.get_context_id("Activation")  
            self.statusbar.push(context_id,'Running...')
        
            #start watching output
            self.source_id = gobject.timeout_add(100, self.checkfile)
        
            for i in range(self.Npreset):
                if operation == self.presetlist[i][1]:
                    # generate command line in subprocess syntax
                    subcommand = ['/usr/bin/ffmpeg','-y','-i']
                    subcommand.extend([self.input])
                    temp1=self.presetlist[i][2].split(' ')
                    # remove empty entries ('') from the array
                    for ii in range(20):
                        try:
                            temp1.remove('')
                        except:
                            pass
                    temp1.extend([str(self.input+"."+self.presetlist[i][3])])
                    subcommand.extend(temp1)
                    # Start converting
                    self.process = subprocess.Popen(args=subcommand,
                            stdout=subprocess.PIPE,stdin=subprocess.PIPE,
                            stderr=subprocess.STDOUT,shell=False)
                    
                    logfile.writelines(subcommand)



    def stop(self,widget):
        """ Tried to kill the conversion process before it is done."""
        try:
            os.kill(self.process.pid,9)
            gobject.source_remove(self.source_id)
            self.progressbar.set_fraction(0.0)
            self.progressbar.set_text('')
            logfile.writelines('Conversion stopped\n')
            context_id = self.statusbar.get_context_id("Activation")  
            self.statusbar.push(context_id,'Conversion aborted!')
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
        counter=0
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
                       # self.video_codec = [output_split[i+1].strip(','),
                        #        output_split[i+2].strip(','),
                         #       output_split[i+3].strip(',')]
                        self.video_codec[0] = output_split[i+1].strip(',')
                        self.video_codec[1] = output_split[i+2].strip(',')
                        self.video_codec[2] = output_split[i+3].strip(',')

                    # Find video bitrate            
                    if output_split[i]=='bitrate:':
                        self.video_codec[3] = output_split[i+1].strip(',')+' kb/s'

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

            if counter >= 1000:
                flag = 0
            counter = counter+1

    def aboutdialog(self,widget):
        """ Defines the about information about the program."""

        dialogtext = "The Sinthgunt Converter - a ffmpeg gui.\
                        \nBy Thomas R. N. Jansson (tjansson@tjansson.dk) and\
                        \n Kaare H. Jensen (kare1234@gmail.com)\
                        \n\nSee LICENSE.TXT for License information\
                        \nSelect the video file you wish to convert\
                        \nfrom the File menu. Then, select the type\
                        \nof conversion you want to perform from the\
                        \nPresets menu. To start converting, press the\
                        \nConvert button in the main window.\
                        \n\nPlease visit http://www.sinthgunt.org\
                        \nfor more info."
        message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, dialogtext)
        message.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        resp = message.run()
        if resp == gtk.RESPONSE_CLOSE:
            message.destroy()


    def no_file_selected_dialog(self,widget):
        """ If no file have been selected to send to ffmpeg this warning will
        be displayed."""

        dialogtext = "You have to select a file and/or a preset before you \
        \ncan begin converting!"
        message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, 
                gtk.BUTTONS_NONE, dialogtext)
        message.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        resp = message.run()
        if resp == gtk.RESPONSE_CLOSE:
            message.destroy()
    
    def unsupported_codec_dialog(self,widget):
        """ If an unsupported codec has been selected this warning will
        be displayed."""

        dialogtext = "You have selected a preset which is (probably) not supported by your version of ffmpeg. \
To upgrade ffmpeg, please check your distribution documentation. \
\n If you want, you may disregard this warning and check the log file (sinthgunt.log) \
after pressing the convert button"
        message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, 
                gtk.BUTTONS_NONE, dialogtext)
        message.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        resp = message.run()
        if resp == gtk.RESPONSE_CLOSE:
            message.destroy()

    def menuradiobuttonselect(self,widget):
        """ Function that detects which menu radio button has been selected."""

        self.operation_radiobutton = ''
        counter=0
        for presetmenu1header in self.presetmenu1headerholder:
            for item in presetmenu1header:
                if item.get_active() == True:
                    self.operation_radiobutton = self.presetlist[counter][1]
                    self.labelOperation.set_text('Output to '+self.presetlist[counter][1])
                    # if preset is not supported, display unsupported_codec_dialog                    
                    if self.preset_enabled[counter]==False:
                        self.unsupported_codec_dialog(widget)
                        self.labelOperation.set_text('Output to '+self.presetlist[counter][1]+'\n(Preset not supported by ffmpeg)')
                        #item.set_active(True)
                counter = counter + 1
                

    def parseXML(self):
        """ Parses the XML file to gather the different conversion presets into
        categories which will be inserted into the gui. 
(planned) In the future, this function should also test wether the preset will work with the version of ffmpeg avaliable to the user. The result should be included in the array presets e.g. by using row = [' ',' ',' ',' ',[],'encoding=True','decoding=False'] syntax. 
This would significantly improve the clarity of the load_conf_file(self) function."""

        xml_file = os.path.abspath(__file__)
        xml_file = os.path.dirname(xml_file) # load xml file
        xml_file = os.path.join(xml_file, DATA_DIR+"presets.xml")
        optionsXML = etree.parse(xml_file)
        presets=[]
        row = [' ',' ',' ',' ',[]]

	    # Iterate through presets in xml file
        for child in optionsXML.getiterator():
            if child.tag == 'label': # preset name
                row[1]=child.text

            if child.tag == 'params': # preset ffmpeg command line options
                row[2]=child.text

            if child.tag == 'extension': # output file extension
                row[3]=child.text.strip(' ')

            if child.tag == 'category': # preset category
                row[0]=child.text

            if child.tag == 'codecs': # encoding codecs required by preset
                row[4]=child.text.split(',')
                presets.append(row)
                row = [' ',' ',' ',' ',[]]
                # (planned): Test if codec will work

            
    	# Sort by category name
    	presets.sort(lambda x, y: cmp(x[0],y[0]))

    	# find category list
    	categories=[presets[0][0]]
    	for row in presets:
        	if row[0]!=categories[-1]:
            		categories.append(row[0])

        # make lists global        
        self.presetlist=presets
        self.categorylist=categories

        # Get codecs and check if encoding and/or decoding is avaliable
        self.ffmpeg_getcodecs()


    def ffmpeg_getinfo(self,widget):
        """ This function finds the information about the current selected
        file. Displays number of frames, audio codec and video codec.

        Get ffmpeg info function. For determining which version of ffmpeg the
        user has installed.
        """
        self.ffmpeg_getcodecs()
        command = ["ffmpeg","-version"]
        output = ''

        try:
            process = subprocess.Popen(args=command,stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,stderr=subprocess.STDOUT)
            output = str(process.stdout.read(10000))        
        except:
            None
           
        dialogtext=output
        dialogtitle='ffmpeg info'
        # check to see if ffmpeg is installed. Print error if it is not present
        if output=='':
            dialogtext='ffmpeg is not installed on this computer or something \
        else went wrong. See README.txt for installation instructions.'
        
        message = gtk.MessageDialog(None,gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, 
                gtk.BUTTONS_NONE, dialogtext)
        message.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        message.set_title('ffmpeg info')
        resp = message.run()
        if resp == gtk.RESPONSE_CLOSE:
            message.destroy()

    def ffmpeg_getcodecs(self):
        """ This function determines which codecs the user has installed by looking at the output from "ffmpeg -formats"
        """
        command = ["ffmpeg","-formats"]
        output = ''

        try:
            process = subprocess.Popen(args=command,stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,stderr=subprocess.STDOUT)
            output = str(process.stdout.read(10000))        
        except:
            None
        output_lines=output.split('\n')
        codecs_raw=[]
        Ncodecs=0
        for line in output_lines:
            line_split=line.split(' ')
            line_codec=line_split[0:7]
            for i in range(20):
                try:
                    line_codec.remove('')
                except:
                    pass
            codecs_raw.append(line_codec)
            Ncodecs=Ncodecs+1
        # look for encoding 
        self.codecs=[]
        for i in range(Ncodecs):
                flag = 0
                try:
                    # row: codec name, encode, decode
                    row = ['',False,False]
                    # Check to see if we can encode
                    if codecs_raw[i][0].find('E')== 0 or codecs_raw[i][0].find('E')== 1:
                        row[0]=codecs_raw[i][-1]  
                        row[1]=True
                        flag = 1
                    # Check to see if we can decode
                    if codecs_raw[i][0].find('D')== 0 or codecs_raw[i][0].find('D')== 1:
                        row[0]=codecs_raw[i][-1]
                        row[2]=True
                        flag =1
                    # Only add codec if we can either encode or decode
                    if flag==1:
                        self.codecs.append(row)                       
                except:     
                    pass
        # Print to console for debugging        
        # print self.codecs
        
#####################
## The init function
#####################
    
    def __init__(self):
        """ Reads the information from glade file and connects the buttons with
        the functions."""

        #Set the Glade file
        self.gladefile = DATA_DIR+"sinthgunt.glade"  
        self.wTree = gtk.glade.XML(self.gladefile) 

        #Get the Main Window, and connect the "destroy" event
        self.window = self.wTree.get_widget("MainWindow")

        if (self.window):
            # connect to label
            self.labelGuide = self.wTree.get_widget("labelGuide")
            self.labelInput = self.wTree.get_widget("labelInput")
            self.labelOperation = self.wTree.get_widget("labelOperation")        
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
                        "on_toolbarconvert_clicked"  : self.activate,
                        "on_button_stop_clicked"     : self.stop,
                        "on_toolbarstop_clicked"     : self.stop,
                        "MainWindow_destroy"         : self.quit_program,
                        "on_menuquit_activate"       : self.quit_program,
                        "on_menuopen_activate"       : self.menuopenfile,
                        "on_toolbaropen_clicked"     : self.menuopenfile,
                        "on_menuconvert_activate"    : self.activate,
                        "on_menuabout_activate"      : self.aboutdialog,
                        "on_menuffmpeginfo_activate" : self.ffmpeg_getinfo}
            
            #Do the magic connecting to the widgets
            self.wTree.signal_autoconnect(self.dic)        
            self.input = None


##########################
## The main loop
##########################

if __name__ == "__main__":
    program = sinthgunt()
    gtk.main()
