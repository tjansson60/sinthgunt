# $Id$

###################
# ABOUT Nobel Converter
###################

The Nobel Converter(TNC) is a graphical front end to the notoriously complex 
ffmpeg command line.

###################
# INSTALLATION
###################

# Linux(Ubuntu 8.10)
The only dependency in Ubuntu 8.10 is ffmpeg, which is installed by executing
sudo apt-get install ffmpeg

# Windows 
Windows is not yet supported but ffmpeg, Python and GTK+ are available so 
maybe a future release of TNC will support Windows. 

###################
# KNOWN ISSUS / TODO
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
#  LICENSE
###################

Copyright 2009 Kåre Hartvig Jensen (kare1234@gmail.com) and 
Thomas R. N. Jansson (tjansson@tjansson.dk). 

The Nobel Converter is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Nobel Converter is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with The Nobel Converter. If not, see <http://www.gnu.org/licenses/

##################
#  Related projects
##################
http://code.google.com/p/winff/
http://code.google.com/p/pyffmpeg/
http://code.google.com/p/wffmpeg/
http://code.google.com/p/jffmpeggui/
http://code.google.com/p/medpiper/
