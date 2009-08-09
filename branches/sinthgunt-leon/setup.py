#!/usr/bin/env python

from distutils.core import setup
import os, sys

files=[]
for f in os.path.abspath(''):
    files.append(f)

setup(name = 'sinthgunt',
    version = '1.0',
    description = 'Sinthgunt Converter',
    long_description = 'Sinthgunt Converter',
    author = 'Kaare Hartvig Jensen and Thomas R. N. Janson',
    author_email = 'kare1234@gmail.com',
    url = 'http://sinthgunt.googlecode.com',
    license = ['GPLv3'],
    packages = ['Sinthgunt'],
    package_data = {'sinthgunt': files},
    scripts = ['sinthgunt'],
    data_files=[
        ('share/sinthgunt',['share/sinthgunt.glade','share/presets.xml','share/logo.png','share/icon.png','README.txt','LICENSE.txt','sinthgunt.html'])
    ]
)

