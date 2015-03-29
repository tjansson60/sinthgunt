# Installing Sinthgunt #
This page describes how to install sinthgunt on various Linux distributions.
Note that Sinthgunt relies on you having ffmpeg installed, including many of the non-free plugins. The Sinthgunt dev team therefore recommends that you either
install it through your package manager or follow an installation guide, such as
[this one](http://code.google.com/p/sinthgunt/wiki/Installation_ffmpeg) (probably obsolete).
## Recommended installation instructions ##
The recommended way of installing sinthgunt is to check out the latest version through svn:
```
svn checkout http://sinthgunt.googlecode.com/svn/trunk/ sinthgunt
cd sinthgunt
sudo python setup.py install  
```
### Running Sinthgunt ###
To run sinthgunt, simply click the icon in the multimedia part of your start menu, or issue the command
```
sinthgunt 
```
## Troubleshooting ##
  * If you get an error regarding the file _sinthgunt.glade_, try installing sinthgunt with
```
sudo python setup.py install --prefix='/usr'
```

# Distribution-specific installation instructions #
Below, please find detailed installation instructions for
  * Ubuntu 8.10/9.04/Debian
  * Frugalware
  * openSuse 11
  * Fedora 10
  * Mandriva 2009.1

## Ubuntu/Debian ##
  * Last tested: Feb 12, 2013
### Installation using a .deb package ###
Download that latest .deb package from the [downloads tab](http://code.google.com/p/sinthgunt/downloads/list).
Then, install Sinthgunt by issuing the commands
```
sudo dpkg -i sinthgunt-*.deb
sudo apt-get -f --force-yes --yes install
sudo dpkg -i sinthgunt-*.deb
```
Finally, install non-free plugins from the multivers repo
```
sudo apt-get install libavcodec-extra-53 libavdevice-extra-53 libavfilter-extra-2 libavformat-extra-53 libavutil-extra-51 libpostproc-extra-52 libswscale-extra-2 
```
### Installation from source ###
To install Sinthgunt,
  * Download the latest tarball from the downloads tab - or - checkout the latest source snapshot by issuing the command
```
svn checkout http://sinthgunt.googlecode.com/svn/trunk/ sinthgunt
```
  * To install Sinthgunt, issue the command
```
sudo python setup.py install
```
### Running Sinthgunt ###
To run Sinthgunt, type
```
sinthgunt
```
in a console. Then, open a video file, select a preset and press convert.
## Frugalware ##
<img src='http://frugalware.org/images/logo-new.png'></li></ul>

To install Sinthgunt, execute as root<br>
<pre><code>pacman -S sinthgunt<br>
</code></pre>
<h2>openSuse 11 ##
<img src='http://tuxtraining.com/wp-content/plugins/wp-post-icon/img/suse.png'>
<ul><li>Add the Packman repository (eg. at <a href='http://packman.jacobs-university.de/suse/11.0/'>http://packman.jacobs-university.de/suse/11.0/</a>) to YaST.<br>
</li><li>Install some nessecary packages<br>
<pre><code>yast -i python-devel ffmpeg subversion<br>
</code></pre>
</li></ul><ul><li>Download the latest tarball from the downloads tab - or - checkout the latest source snapshot by issuing the command<br>
<pre><code>svn checkout http://sinthgunt.googlecode.com/svn/trunk/ sinthgunt<br>
</code></pre>
<ul><li>Install Sinthgunt by running (as root from the sinthgunt directory)<br>
<pre><code>python setyp.py install<br>
</code></pre>
<h3>Running Sinthgunt</h3>
To run Sinthgunt, type<br>
<pre><code>sinthgunt<br>
</code></pre>
in a console. Then, open a video file, select a preset and press convert.<br>
<h2>Fedora 10</h2>
<img src='http://tuxtraining.com/wp-content/plugins/wp-post-icon/img/fedora.png'>
</li><li>Add the rpmfusion repositories. Run as root<br>
<pre><code>rpm -Uvh http://rpm.livna.org/livna-release.rpm  http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-stable.noarch.rpm  http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-stable.noarch.rpm<br>
</code></pre>
</li><li>Install ffmpeg and subversion. Run as root<br>
<pre><code>yum install ffmpeg subversion python-devel<br>
</code></pre>
</li></ul></li><li>Download the latest tarball from the downloads tab - or - checkout the latest source snapshot by issuing the command<br>
<pre><code>svn checkout http://sinthgunt.googlecode.com/svn/trunk/ sinthgunt<br>
</code></pre>
<ul><li>Install Sinthgunt by running (as root from the sinthgunt directory)<br>
<pre><code>python setyp.py install<br>
</code></pre>
<h3>Running Sinthgunt</h3>
To run Sinthgunt, type<br>
<pre><code>sinthgunt<br>
</code></pre>
in a console. Then, open a video file, select a preset and press convert.<br>
<h2>Mandriva 2009.1</h2>
<img src='http://www.dnabaser.com/baser-on-linux-mac/logos/mandriva.png'>
</li><li>Install subversion and python-devel libs. Run as root<br>
<pre><code>urpmi subversion python-devel<br>
</code></pre>
</li></ul></li><li>Download the latest tarball from the downloads tab - or - checkout the latest source snapshot by issuing the command<br>
<pre><code>svn checkout http://sinthgunt.googlecode.com/svn/trunk/ sinthgunt<br>
</code></pre>
<ul><li>Install Sinthgunt by running (as root from the sinthgunt directory)<br>
<pre><code>python setyp.py install<br>
</code></pre>
<h3>Running Sinthgunt</h3>
To run Sinthgunt, type<br>
<pre><code>sinthgunt<br>
</code></pre>
in a console. Then, open a video file, select a preset and press convert.