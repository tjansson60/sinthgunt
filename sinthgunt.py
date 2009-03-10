#!/usr/bin/python
# $Id$

import sys
import os
import pygtk; pygtk.require("2.0")
import gtk
import gtk.glade
import subprocess
import gobject
import time

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

        #Reads the config file 
        conf_file_holder = open("sinthgunt.conf","rd")
        # Creates a empty array for the options
        self.bm=[] 
        conf_file = [line[:-1] for line in conf_file_holder]
        
        #Searches through the configfile and splits the fields using ";"
        for line in conf_file:
            row = []	
            fields = line.split(";")
            for i in range(6):
                row.append(fields[i])
            self.bm.append(row)
        conf_file_holder.close
        
        #Counts the total number of options
        self.numbm=len(self.bm)

        #Populates combobox
        self.operation = self.wTree.get_widget("comboboxOperation")
        operation = self.operation.get_active_text()
        for i in range(self.numbm-2):
            self.Operation.append_text(self.bm[i+2][0])	        
        self.Operation.set_active(0)



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
        
            #if self.input == None:
            #    try:
            #        self.input = self.input_from_menu
            #    except:
            #        self.input = '/foo/bar'

            # start conversion
            self.operation = self.wTree.get_widget("comboboxOperation")
            operation = self.operation.get_active_text()
            for i in range(self.numbm-1):
                if operation == self.bm[i+1][0]:
                    # generate command line in subprocess syntax
                    subcommand = [str(self.bm[i+1][1])]
                    if self.bm[i+1][2]!='':
                        subcommand.extend(self.bm[i+1][2].split(' '))            
                    subcommand.extend([self.input])
                    if self.bm[i+1][3]!='': 
                        subcommand.extend(self.bm[i+1][3].split(' '))
                    subcommand.extend([str(self.input+"."+self.bm[i+1][5])])
                    if self.bm[i+1][4]!='': 
                        subcommand.extend(self.bm[i+1][4].split(' '))
                    # start converting
	            logfile.writelines(subcommand)
                    self.process = subprocess.Popen(args=subcommand, 
                        stdout=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        shell=False)



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
                        \nSee LICENSE.TXT for License information"
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


if __name__ == "__main__":
    program = sinthgunt()
    gtk.main()
