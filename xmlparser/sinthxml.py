#!/usr/bin/env python

from xml.dom import minidom
from xml.etree import ElementTree as etree
import os

def main():
	# load xml file
	xml_file = os.path.abspath(__file__)
        xml_file = os.path.dirname(xml_file)
        xml_file = os.path.join(xml_file, "presets.xml")
	optionsXML = etree.parse(xml_file)

	presets=[]
	row = []

	# Iterate through presets
	for child in optionsXML.getiterator():
		if child.tag == 'category':
			row.append(child.text)
		if child.tag == 'label':
			row.append(child.text)
		if child.tag == 'params':
			row.append(child.text)
		if child.tag == 'extension':
			row.append(child.text)
			presets.append(row)
			row = []

	# Print some stuff
	print presets[0][0]
	print presets

if __name__ == "__main__":
	# Someone is launching this directly
	main()

