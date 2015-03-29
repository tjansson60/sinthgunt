#Instructions for building the Sinthgunt debian package

Create packages
```
sudo make builddeb
```
```
sudo make buildrpm
```
```
sudo make source
```
```
sudo make clean
```
# Instructions below are obsolete #
Sinthgunt no longer uses debianpackagemaker. I will leave this up for anyone how is looking for at guide on how to use the program.

# Introduction #
Sinthgunt uses [debianpackagemaker](http://code.google.com/p/debianpackagemaker/) to create deb packages.

## Installing debianpackagemaker ##
  * Download [debianpackagemaker](http://code.google.com/p/debianpackagemaker/) from http://code.google.com/p/debianpackagemaker/downloads/list. Currently, I am using dpm\_0.4~welemski1\_ubuntu8.04\_i386.deb (May, 2009).

## Using debianpackagemaker ##
Launch debianpackagemaker from the terminal by typing
```
debianpackagemaker
```
Then, open the file sinthgunt\_debianpackagemaker\_config.txt.dpm (or another relevant dpm file). Once the file is loaded, you will be presented with three tabs in the main window
  * Install Structure - this is where you specify which files go where on the end users computer.
  * Package info - this is where you specify the package info - eg. version number and the name of the maintainer.
  * Dependencies - this is where you specify the dependencies. So far, it only depends on ffmpeg.
Once you have entered the nessecary information, press the **Create package** button and specify an output file name, eg. sinthgunt-1.0.1.deb

## Screenshots ##
### Install structure ###
<img src='http://www.hartvig.de/files/sinthgunt/debianpackagemaker-installstructure.png'>
<h3>Package info</h3>
<img src='http://www.hartvig.de/files/sinthgunt/debianpackagemaker-packageinfo.png'>
<h3>Dependencies</h3>
<img src='http://www.hartvig.de/files/sinthgunt/debianpackagemaker-dependencies.png'>

<h1>Automatic uploads to the Downloads page</h1>
Get the google upload script<br>
<pre><code>wget http://googlecode-upload.googlecode.com/svn/trunk/googlecode_upload.pl<br>
</code></pre>

Upload the latest deb package and tarball by issuing the commands:<br>
<pre><code>googlecode_upload.pl -s 'Sinthgunt 2.1.0 Debian package' -proj 'sinthgunt' -l 'Featured,Type-Package,OpSys-Linux' -u 'kare1234' -f sinthgunt_2.1.0_all.deb<br>
</code></pre>
<pre><code>googlecode_upload.pl -s 'Sinthgunt 2.1.0 RPM package' -proj 'sinthgunt' -l 'Featured,Type-Package,OpSys-Linux' -u 'kare1234' -f sinthgunt-2.1.0/dist/sinthgunt-2.1.0-1.noarch.rpm <br>
</code></pre>
<pre><code>googlecode_upload.pl -s 'Sinthgunt 2.1.0 source tarball' -proj 'sinthgunt' -l 'Featured,Type-Archive,OpSys-Linux' -u 'kare1234' -f sinthgunt-2.1.0/dist/sinthgunt-2.1.0.tar.gz <br>
</code></pre>