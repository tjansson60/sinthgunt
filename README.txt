# $Id$

###################
# 1.0 ABOUT The Sinthgunt Converter
###################

The Sinthgunt Converter is a graphical front end to the notoriously complex 
ffmpeg command line.

Download and installation guide: http://code.google.com/p/sinthgunt/
SVN Stats: http://www.hartvig.de/sinthgunt

###################
# 2.0 INSTALLATION
###################

2.1 Linux(Ubuntu 8.10 or similar)

2.1.1 Requirements

Sinthgunt requires that you are running Linux, and that you have a working installation of python, pygtk and ffmpeg. On Ubuntu all you have to do is install ffmpeg by issuing the command 

    sudo apt-get install ffmpeg

2.1.2 Installation
Download the latest source snapshot by issuing the command
    svn checkout http://sinthgunt.googlecode.com/svn/trunk/ sinthgunt-read-only
Next, install sinthgunt by running the command

    python setup.py install

Now, run Sinthgunt by issuing the command
    
    sinthgunt.py

2.2 Windows 

Windows is not yet supported but ffmpeg, Python and GTK+ are available so 
maybe a future release of The Sinthgunt Converter will support Windows. 

###################
# 3.0 KNOWN ISSUS / TODO
###################

* The thumbnails are not generated for some files
* The configuration file should be in XML: name of operation,
  commando, preinput arguments, middle arguments,
  postoutput arguments, output filename extension 
  A huge collection of presets:
  http://code.google.com/p/winff/source/browse/trunk/%20winff%20--username%20bggmtt/presets.xml
* The input file selection dialog mime type should include more file types.
* Clean up of names like labelsovs to that is understandable and intuitive.  
* file_get_info uses flag=0 should be written pretty.
* How about a direct "Download youtube movie and convert to mp3 function"?

###################
# 4.0 LICENSE
###################

Copyright 2009 Kåre Hartvig Jensen (kare1234@gmail.com) and 
Thomas R. N. Jansson (tjansson@tjansson.dk). 

The Sinthgunt Converter is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The Sinthgunt Converter is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with the Sinthgunt Converter. If not, see <http://www.gnu.org/licenses/

4.1

Parts of the file presets.xml are Copyright 2006-2009 Matthew Weatherford and are (re)used here under the GPL v3 license.

##################
# 5.0 Related projects
##################
http://code.google.com/p/winff/
http://code.google.com/p/pyffmpeg/
http://code.google.com/p/wffmpeg/
http://code.google.com/p/jffmpeggui/
http://code.google.com/p/medpiper/
http://pspvc.sourceforge.net/
