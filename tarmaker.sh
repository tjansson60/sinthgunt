#!/bin/bash

#This line collects and compresses the files for the tarball
tar -cvzf sinthgunt-latest.tar.gz sinthgunt.py sinthgunt.glade presets.xml \
	      icon.png logo.png README.txt LICENSE.txt setup.py

# Creates html documentation. Why is this a part of the tarmake
# script? It is not even included in the tarball.
#pydoc -w sinthgunt
