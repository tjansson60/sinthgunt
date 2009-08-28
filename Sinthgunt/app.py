#!/usr/bin/python
# $Id$

####################
# =========
# sinthgunt
# =========
#
# Copyright 2009 Kaare Hartvig Jensen (kare1234@gmail.com) and 
# Thomas R. N. Jansson (tjansson@tjansson.dk). 
#
# The Sinthgunt Converter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# The Sinthgunt Converter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sinthgunt. If not, see http://www.gnu.org/licenses/
#
# Description     
# ===========
"""Sinthgunt is an open source graphical user interface for ffmpeg, 
a computer program that can convert digital audio and video into 
numerous formats. Using pre-configured conversion settings, it makes
 the task of converting between different media formates very easy.
 """
####################

####################
# Import Python Libraries
####################
import os
import pygtk; pygtk.require("2.0")
import gtk.glade
import subprocess
import gobject
import time
import sys
import urllib
from xml.etree import ElementTree as etree



def main():
    ####################
    # System checks
    ####################
    # Check to see if ffmpeg is installed
    if os.path.exists("/usr/bin/ffmpeg"):
        print('ffmpeg found. Starting Sinthgunt...')# carry on
    else:
        print('It seems, that ffmpeg is not installed on this computer. \nSee http://www.sinthgunt.org for installation instructions.') # Display error message, then carry on

    # Define data directory
    DATA_DIR="/usr/share/sinthgunt/"
    
    # Opens the log file and write the name and curent data and time
    logfile_filename = os.path.expanduser("~/.sinthgunt.log")
    logfile = open(logfile_filename, 'a')
    logfile.writelines('****** Sinthgunt log file START - '+
            str(time.ctime())+' *******\n')
    logo_filename=DATA_DIR+"logo.png"
  
    # Carry over variables to class
    sinthgunt.logo_filename = logo_filename
    sinthgunt.DATA_DIR      = DATA_DIR
    sinthgunt.logfile       = logfile

    # Run the main loop
    program = sinthgunt()
    gtk.main()


class sinthgunt:
####################
# FUNCTIONS START
####################
    def systemCheck(self):
        ####################
        # Description
        # ===========
        """ This function performs a system check when sinthgunt is started."""
        # Arguments
        # =========
        #
        # Further Details
        # ===============
        # The function 
        # - looks for ffmpeg in /usr/bin/
        # - 
        # - 
        ####################

    def load_conf_file(self):
        ####################
        # Description
        # ===========
        """ This function reads the configuration xml-file and populates the
        Preset menu with the conversion options.
        """
        # Arguments
        # =========
        #
        # Further Details
        # ===============
        #
        ####################
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
        ####################
        # Description 
        # ===========
        """ This function is executed many times to check on the progress of
        the conversion. """
        # Arguments
        # =========
        #
        # Further details
        # ===============
        # 
        ####################
        context_id = self.statusbar.get_context_id("Activation")        
        output = ''
        try:
            output_raw = str(self.process.stdout.read(80))
            output = output_raw.replace('\n','')
        except:
            pass
        self.logfile.writelines('Conversion status: '+output+'\n')
        output_split = output.split(' ')
        N=len(output_split)
        
        # get the number of frames converted
        for i in range(N):
            if i>=2 and output_split[i]=='fps=':
               file_frames_completed = output_split[i-1]              
               self.logfile.writelines('Frames completed: '+file_frames_completed+'\n')
               # update progressbar and statusbar
               try:
                   context_id = self.statusbar.get_context_id("Activation")  
                   self.statusbar.push(context_id,'Frames converted: '+str(file_frames_completed))
               except:
                   pass
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
            #self.progressbar.set_text(str(str(self.file_frames)+\
            #                              ' of '+str(self.file_frames)+' frames converted.'))
            # this line would do the sames as return False: gobject.source_remove(self.source_id)          
            return False    
        else:
            return True
  
    
    
    def menuopenfile(self,widget):
        ####################
        # Description 
        # ===========
        """ This function open a file selection dialog. """
        # Arguments
        # =========
        #
        # Further details
        # ===============
        # 
        ####################
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
            self.input = fc.get_filename()
            fc.destroy()
            test = self.setinput(widget)
        else:
            fc.destroy()
    

    
    def setinput(self, widget): 
        ####################
        # Description
        # ===========
        """This function generates a thumbnail and saves it to /tmp directory AND 
        extracts information about the video/audio file.
         """
        # Arguments
        # =========
        #
        # Further Details
        # ===============
        #
        ####################
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
            self.logfile.writelines('Thumbnail process status: '+output+'\n')
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

    def activate(self,widget):
        ####################
        # Description
        # ===========
        """This function starts the conversion process.
         """
        # Arguments
        # =========
        # self.input    Path to input file 
        #
        # Further Details
        # ===============
        #
        ####################

        # Get selected operation from menu
       
        try:
            operation = self.operation_radiobutton
            self.progressbar.set_fraction(0.01)
            context_id = self.statusbar.get_context_id("Activation")  
            self.statusbar.push(context_id,'Running...')
        
            #start watching output
            self.source_id = gobject.timeout_add(500, self.checkfile)
        
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
                    # path to output file
                    self.output=str(self.input+"."+self.presetlist[i][3])
                    subcommand.extend(temp1)
                    # Start converting
                    self.process = subprocess.Popen(args=subcommand,
                            stdout=subprocess.PIPE,stdin=subprocess.PIPE,
                            stderr=subprocess.STDOUT,shell=False)
                    
                    self.logfile.writelines('Conversion command: '+str(subcommand)+'\n')
        except:
            self.no_file_selected_dialog(widget)


    def stop(self,widget):
        ####################
        # Description
        # ===========
        """This function tries to stop the conversion process before it is done."""
        # Arguments
        # =========
        # self.process.pid  process id of the ffmpeg process that we want to kill.
        #
        # Further Details
        # ===============
        #
        ####################
        try:
            os.kill(self.process.pid,9)
            gobject.source_remove(self.source_id)
            self.progressbar.set_fraction(0.0)
            self.progressbar.set_text('')
            self.logfile.writelines('Conversion aborted by user\n')
            context_id = self.statusbar.get_context_id("Activation")  
            self.statusbar.push(context_id,'Conversion aborted!')
        except:
            pass
            
   

    def quit_program(self,widget):
        ####################
        # Description
        # ===========
        """ When the program is closed the stop function and the logfile is
        updated and program is terminated. """
        # Arguments
        # =========
        #
        # Further Details
        # ===============
        #
        ####################
        self.stop
        self.logfile.writelines('****** Sinthgunt log file STOP - '+str(time.ctime())+' *******\n')
        self.logfile.close
        gtk.main_quit()



    def file_getinfo(self):
        #################### 
        # Description
        # ===========
        """ This function finds the information about the current selected
        file. Displays number of frames, audio codec and video codec."""
        # Arguments
        # =========
        #
        # Further Details
        # ===============
        #
        ####################
        self.audio_codec = ['N/A','N/A','N/A','N/A','N/A']
        self.video_codec = ['N/A','N/A','N/A','N/A','N/A']
        self.file_frames = 0
        command = ["ffmpeg","-i",self.input]

        process = subprocess.Popen(args=command,stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,stderr=subprocess.STDOUT)

        flag = 1
        counter=0
        while flag == 1:   
            try:       
                output = str(process.stdout.read(10000))        
            except:
                break

            if output != '\n' and output != '':
                self.logfile.writelines('Get file info status: '+output+'\n')
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
        self.logfile.writelines('Audio codec: '+str(self.audio_codec)+'\n')
        self.logfile.writelines('Video codec: '+str(self.video_codec)+'\n')
        self.logfile.writelines('Number of frames: '+str(self.file_frames)+'\n')

    def aboutdialog(self,widget):
        ####################
        # Description
        # ===========
        """ Defines the about information about the program."""
        # Arguments
        # =========
        #
        # Further Details
        # ===============
        #
        #################### 
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
        ####################
        # Description
        # ===========
        """ If no file have been selected to send to ffmpeg this warning will
        be displayed."""
        # Arguments
        # =========
        #
        # Further Details
        # ===============
        #
        #################### 

        dialogtext = "You have to select a file and/or a preset before you \
        \ncan begin converting!"
        message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, 
                gtk.BUTTONS_NONE, dialogtext)
        message.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        resp = message.run()
        if resp == gtk.RESPONSE_CLOSE:
            message.destroy()
    
    def unsupported_codec_dialog(self,widget):
        ####################
        # Description
        # ===========
        """ If an unsupported codec has been selected this warning will
        be displayed."""
        # Arguments
        # =========
        #
        # Further Details
        # ===============
        #
        #################### 

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
        ####################
        # Description
        # ===========
        """ Function that detects which menu radio button has been selected."""
        # Arguments
        # =========
        #
        # Further Details
        # ===============
        #
        #################### 
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
        ####################
        # Description
        # ===========
        """ Parses the XML file to gather the different conversion presets into
        categories which will be inserted into the gui.
         
        (planned) In the future, this function should also test wether the preset 
        will work with the version of ffmpeg avaliable to the user. The result should 
        be included in the array presets e.g. by using row = [' ',' ',' ',' ',[],'encoding=True',
        'decoding=False'] syntax. This would significantly improve the clarity of 
        the load_conf_file(self) function."""
        # Arguments
        # =========
        #
        # Further Details
        # ===============
        #
        ####################
        xml_file = os.path.abspath(__file__)
        xml_file = os.path.dirname(xml_file) # load xml file
        xml_file = os.path.join(xml_file, self.DATA_DIR+"presets.xml")
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
        ####################
        # Description
        # ===========
        """ This function finds the information about the current selected
        file. Displays number of frames, audio codec and video codec.

        Get ffmpeg info function. For determining which version of ffmpeg the
        user has installed.
        """
        # Arguments
        # =========
        #
        # Further Details
        # ===============
        #
        ####################
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
        ####################
        # Description
        # ===========
        """ This function determines which codecs the user has installed by looking at the output from "ffmpeg -formats"
        """
        # Arguments
        # =========
        #
        # Further Details
        # ===============
        #
        ####################
        command = ["ffmpeg","-formats"]
        output = ''

        try:
            process = subprocess.Popen(args=command,stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,stderr=subprocess.STDOUT)
            output = str(process.stdout.read(20000))        
        except:
            None
        self.logfile.writelines('ffmpeg_getcodecs output: '+str(output))
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
        self.logfile.writelines('ffmpeg_getcodecs codecs_raw: '+str(codecs_raw))
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
        # Debugging codec row
        row = ['debugcodec',True,True]
        self.codecs.append(row)  
        self.logfile.writelines('ffmpeg_getcodecs self.codecs: '+str(self.codecs))
 

#####################
## YouTube functions
#####################
    def menuopenyoutube(self,widget):  
        ####################
        # Description
        # ===========
        """ Dialog that allows the user to enter a YouTube url. 
            Once the user presses the 'ok' button, the download will begin"""
        # Arguments
        # =========
        #
        # Further Details
        # ===============
        #
        ####################      
        #base this on a message dialog  
        dialog = gtk.MessageDialog(None,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_QUESTION,gtk.BUTTONS_OK,None)  
        dialog.set_markup('Please enter YouTube URL or a direct link to a video file, eg.')  
        #create the text input field  
        entry = gtk.Entry()  
        #allow the user to press enter to do ok  
        #entry.connect("activate", dialog.response(response), dialog, gtk.RESPONSE_OK)  
        #create a horizontal box to pack the entry and a label  
        hbox = gtk.HBox()  
        hbox.pack_start(gtk.Label("URL:"), False, 5, 5)  
        hbox.pack_end(entry)  
        #some secondary text  
        dialog.format_secondary_markup("<i>http://www.youtube.com/watch?v=MRn-Rmp6iwA</i>\n- or-\n<i>http://hartvig.de/files/dod/16cwillcttt_teaser.avi</i>")  
        #add it and show it  
        dialog.vbox.pack_end(hbox, True, True, 0)  
        dialog.show_all()  
        #go go go  
        dialog.run()  
        self.youtubeurl = entry.get_text()  
        dialog.destroy()  
        dialog.destroy()
        # Look for direct link to media file
        if self.youtubeurl[-4]=='.':
            # find last '/'
            for i in range(len(self.youtubeurl)):
                if self.youtubeurl[-i]=='/':
                    output=self.youtubeurl[-i+1:]
                    break
            print output
            print self.youtubeurl
            self.input=os.getenv("HOME")+'/'+output
            self.download(self.youtubeurl)
            self.setinput(widget)
        else:            
            self.download_youtube()
            self.setinput(widget)
            

    def download(self,url):
        ####################
        # Description
        # ===========
        """Copy the contents of a file from a given URL to a local file.""" 
        # Arguments
        # =========
        # url   http url of the remote file to download eg. http://www.example.org/movie.mpg
        #
        # Further Details
        # ===============
        #
        ####################   
        
        webFile=urllib.urlretrieve(url, self.input,lambda nb, bs, fs, url=url: self._reporthook(nb,bs,fs,url))


    def _reporthook(self,numblocks, blocksize, filesize, url=None):
        ####################
        # Description
        # ===========
        """Prints the download status to the status bar."""
        # Arguments
        # =========
        #
        # Further Details
        # ===============
        #
        ####################  
        base = os.path.basename(url)
        #Should handle possible filesize=-1.
        try:
            percent = min((numblocks*blocksize*100)/filesize, 100)
        except:
            percent = 100
        if numblocks != 0:
            sys.stdout.write("\b"*70)
        context_id = self.statusbar.get_context_id("Activation")  
        self.statusbar.push(context_id,'Downloaded '+str(percent)+'% from '+self.youtubeurl)
        self.progressbar.set_fraction(float(percent)/100)
        if percent==100:
            self.statusbar.push(context_id,'Downloaded completed. Saved as '+self.dst)
        # Wait for gui to update
        while gtk.events_pending():
            gtk.main_iteration(False)


    def download_youtube(self):
        ####################
        # Description
        # ===========
        """This function finds the flash video source and title from the youtube page entered by the user."""
        # Arguments
        # =========
        #
        # Further Details
        # ===============
        #
        #################### 
            
        url=self.youtubeurl
        page=urllib.urlopen(url)
        result = page.read()
        youtubepage=result

        #find flash video url
        startindex = result.index("var swfArgs")
        result = result[startindex:]
        endindex=result.index("};")
        result=result[:endindex]
        result =  result.split(",")
        get={}
        for line in result:
            if "video_id" in line or "\"t\"" in line :
                v,vnum = line.replace("\"","").split(":")
                get[v.strip()]=vnum.strip()
    
        dload = "http://www.youtube.com/get_video?video_id=%s&t=%s" % ( get['video_id'],get['t'])
        
        # Find flash video title
        youtubepage_header=youtubepage[100:100+300]
        # Look for <title>        
        for i in range(len(youtubepage_header)-10):
            if youtubepage_header[i]=='<' and youtubepage_header[i+1]=='t' and youtubepage_header[i+2]=='i':
                title1=youtubepage_header[i+7:]
        # Look for </title>
        for i in range(len(title1)):
            if title1[i]=='<' and title1[i+1]=='/' and title1[i+2]=='t':
                title=title1[:i]
        self.youtube_title=title
               
        # Start downloading
        try :
            self.input=os.getenv("HOME")+'/'+self.youtube_title+".flv"
            self.download(dload)
        except Exception,e:
            print "Error: ",e
#####################
## mplayer functions
#####################
    def mplayer_check(self,widget):
        ####################
        # Description
        # ===========
        """Checks if the user has mplayer installed.""" 
        # Arguments
        # =========
        #
        # Further Details
        # ===============
        #
        ####################
        return False 
        if os.path.exist('/usr/bin/mplayer'):
            return True
        else:
            return False
       
    def mplayer_play_input_file(self,widget):
        ####################
        # Description
        # ===========
        """Plays the input file using mplayer.""" 
        # Arguments
        # =========
        # whattoplay    = self.input, path to input file
        #
        # Further Details
        # ===============
        #
        ####################
        if self.mplayer_check:
            whattoplay=' '
            try:
                whattoplay=self.input
            except Exception, e:
                raise e
            command = ["mplayer","-vo","x11",whattoplay]
            process = subprocess.Popen(args=command)
        else:    
            print 'Mplayer must be installed and found in /usr/bin for this function to work'
   
    def mplayer_play_output_file(self,widget):
        ####################
        # Description
        # ===========
        """Plays the input file using mplayer.""" 
        # Arguments
        # =========
        # whattoplay    = self.output, path to output file
        #
        # Further Details
        # ===============
        #
        ####################  
        if self.mplayer_check:
            whattoplay=' '
            try:
                whattoplay=self.output
            except Exception, e:
                raise e
            command = ["mplayer","-vo","x11",whattoplay]
            process = subprocess.Popen(args=command)
        else:
            print 'Mplayer must be installed and found in /usr/bin for this function to work'

#####################
## The init function
#####################
    
    def __init__(self):
        """ Reads the information from glade file and connects the buttons with
        the functions."""

        #Set the Glade file
        self.gladefile = self.DATA_DIR+"sinthgunt.glade"  
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
            self.thumbnail.set_from_file(self.logo_filename)
            
            # set empty input and output strings
            #self.input = None
            #self.output = None


            #Create a dictionary of handles and functions
            self.dic = {#"on_chooserInput_file_set" : self.setinput,
                        "on_button_activate_clicked"    : self.activate,
                        "on_toolbarconvert_clicked"     : self.activate,
                        "on_button_stop_clicked"        : self.stop,
                        "on_toolbarstop_clicked"        : self.stop,
                        "MainWindow_destroy"            : self.quit_program,
                        "on_menuquit_activate"          : self.quit_program,
                        "on_menuopen_activate"          : self.menuopenfile,
                        "on_menuopenyoutube_activate"   : self.menuopenyoutube,
                        "on_toolbaropen_clicked"        : self.menuopenfile,
                        "on_toolbaropenyoutube_clicked" : self.menuopenyoutube,
                        "on_menuconvert_activate"       : self.activate,
                        "on_menuabout_activate"         : self.aboutdialog,
                        "on_menuffmpeginfo_activate"    : self.ffmpeg_getinfo,
                         "on_playbutton_input_clicked" : self.mplayer_play_input_file,
                         "on_playbutton_output_clicked"  : self.mplayer_play_output_file}
            #Do the magic connecting to the widgets
            self.wTree.signal_autoconnect(self.dic)        
            
