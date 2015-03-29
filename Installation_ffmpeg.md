#Installation instructions for ffmpeg

# Installation from deb-packages #
Many Linux distributions offer precompiled versions of ffmpeg.
On Ubuntu you can install a minimal version of ffmpeg by issuing the command
```
sudo apt-get install ffmpeg
```
For use with sinthgunt we recommend that you compile ffmpeg yourself since many codecs are disabled in the precompiled version.
# Compiling ffmpeg on Ubuntu 8.10/9.04 #
This guide is based a forum post by FakeOutdoorsman over at [Ubuntuforums](http://ubuntuforums.org/showthread.php?t=786095).

## Getting the Dependencies ##
1. Uninstall x264, libx264-dev, and ffmpeg if they are already installed. Open a terminal and run the following:
```
sudo apt-get purge ffmpeg x264 libx264-dev
```
Next, get all of the packages you will need to install FFmpeg and x264 (you may need to enable the universe and multiverse repositories):
```
sudo apt-get update
sudo apt-get install build-essential subversion git-core checkinstall yasm texi2html libfaac-dev libfaad-dev libmp3lame-dev libsdl1.2-dev libtheora-dev libx11-dev libxvidcore4-dev zlib1g-dev
```

## Installing x264 ##
Get the most current source files from the official x264 git repository, compile, and install. You can run "./configure --help" to see what features you can enable/disable. If you are behind a firewall or unable to use git, then daily source tarballs are also available.
```
cd
git clone git://git.videolan.org/x264.git
cd x264
./configure
make
sudo checkinstall --fstrans=no --install=yes --pkgname=x264 --pkgversion "1:0.svn`date +%Y%m%d`-0.0ubuntu1" --default
```

## Installing FFmpeg ##
Get the most current source files from the official FFmpeg svn, compile, and install. Run "./configure --help" to see what features you can enable/disable. If you are behind a firewall or unable to use subversion, then nightly FFmpeg snapshots are also available.
```
cd
svn checkout svn://svn.ffmpeg.org/ffmpeg/trunk ffmpeg
cd ffmpeg
./configure --enable-gpl --enable-nonfree --enable-pthreads --enable-libfaac --enable-libfaad --enable-libmp3lame --enable-libtheora --enable-libx264 --enable-libxvid --enable-x11grab
make
sudo checkinstall --fstrans=no --install=yes --pkgname=ffmpeg --pkgversion "3:0.svn`date +%Y%m%d`-12ubuntu3" --default
sudo cp /usr/local/bin/ff* /usr/bin/
```
That's it!