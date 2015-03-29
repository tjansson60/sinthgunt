#Installation instructions for Windows

# Introduction #
When I tested I have some issues with the characters in the GUI being
messed up with python 2.6 which did not exist with python 2.5. The
following is instructions for python 2.5.4

## Install Python 2.5.4 (Final) ##
http://www.python.org/download/
download: python-2.5.4.msi

## Install pygtk ##
Install PyCairo, PyGobject and PyGTK installers from the PyGTK project
website [pygtk.org], note that you need them all installed to get
PyGTK working. The file used with succes was:

```
pygobject-2.14.2-2.win32-py2.5.exe
pycairo-1.4.12-2.win32-py2.5.exe
pygtk-2.12.1-3.win32-py2.5.exe
```

from the http://www.pygtk.org/downloads.html page.


If python 2.6 is installed instead you will need the
py2.6 versions


## Install glade and gtk+ libs ##
Gtk+ 2.12.9 Development Environment [Revision 2](https://code.google.com/p/sinthgunt/source/detail?r=2) (17,172KB)
http://gladewin32.sourceforge.net/
```
gtk-dev-2.12.9-win32-2.exe
```

## Install Windows build of ffmpeg ##
http://ffmpeg.arrozcru.org/builds/

By default the ffmpeg is not a part of the PATH so this need to be
changed by doing the following:
My Computer > Advanced > Enviromental Variables > Edit PATH and insert
the path to the ffmpeg path:
C:\Program Files\ffmpeg-[r16537](https://code.google.com/p/sinthgunt/source/detail?r=16537)-gpl-static-win32\bin
if this is the path to the ffmpeg installation