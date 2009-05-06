#!/usr/bin/env python

from distutils.core import setup

setup(name='Sinthgunt',
        version='1.0',
        description='Sinthgunt Converter',
        author='Kaare Hartvig Jensen and Thomas R. N. Janson',
        url='http://sinthgunt.googlecode.com',
        scripts = ['sinthgunt.py'],
        data_files=[('share/sinthgunt',['sinthgunt.glade','presets.xml','logo.png','icon.png','README.txt','LICENSE.txt'])]
)

