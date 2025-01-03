# 1.0 ABOUT The Sinthgunt Converter
The Sinthgunt Converter is an easy to use gui for the ffmpeg package. Using pre-configured conversion settings, it makes the task of converting between different media formates very easy. 

For more info, please visit http://www.sinthgunt.org

> [!CAUTION]
> Sinthgunt has not been actively maintained since 2013 and was developed in Python 2.7, making it unlikely to function on modern systems without significant updates. Additionally, the SVN installation guide is severely outdated, predating platforms like GitHub, and the website is no longer available.

# 2.0 INSTALLATION
For detailed installation instructions, see [code.google.com/p/sinthgunt/wiki/Installation](http://code.google.com/p/sinthgunt/wiki/Installation)
Dependencies: python-gtk2 python-glade2

The generic installation procedures is

* Download the latest source snapshot by issuing the command
```bash
svn checkout http://sinthgunt.googlecode.com/svn/trunk/ sinthgunt
```

* Install sinthgunt by running the command (as root)
```bash
python setup.py install
```

* Run Sinthgunt by issuing the command
```bash
sinthgunt
```

# 3.0 KNOWN ISSUS / TODO
* The thumbnails are not generated for some files
* How about a direct "Download youtube movie and convert to mp3 function"?

# 4.0 LICENSE
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
along with the Sinthgunt Converter. If not, see [www.gnu.org/licenses](http://www.gnu.org/licenses)

Parts of the file `presets.xml` are Copyright 2006-2009 Matthew Weatherford and are (re)used here under the GPL v3 license.

# 5.0 Related projects
* http://code.google.com/p/winff/
* http://code.google.com/p/pyffmpeg/
* http://code.google.com/p/wffmpeg/
* http://code.google.com/p/jffmpeggui/
http://code.google.com/p/medpiper/
http://pspvc.sourceforge.net/
