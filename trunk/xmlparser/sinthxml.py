#!/usr/bin/env python

from xml.dom import minidom
from xml.etree import ElementTree as etree
import os

def parseXML():
	# load xml file
	xml_file = os.path.abspath(__file__)
        xml_file = os.path.dirname(xml_file)
        xml_file = os.path.join(xml_file, "presets.xml")
	optionsXML = etree.parse(xml_file)
        
	presets=[]
	row = [' ',' ',' ',' ']

	# Iterate through presets
	for child in optionsXML.getiterator():
		if child.tag == 'label':
			row[1]=child.text
		if child.tag == 'params':
			row[2]=child.text
		if child.tag == 'extension':
			row[3]=child.text
		if child.tag == 'category':
   			row[0]=child.text
			row[0]=child.text
			presets.append(row)
			row = [' ',' ',' ',' ']
    	# Sort by category
	presets.sort(lambda x, y: cmp(x[0],y[0]))
    	# find category list
    	categorylist=[presets[0][0]]
    	for row in presets:
        	if row[0]!=categorylist[-1]:
            		categorylist.append(row[0])
        
    	print categorylist
# print for debugging
	for row in presets:
		print row	
	print presets
    


	presetlist=presets
    
	
	# Print some stuff
#	print presets[0][0]
#	print presets

if __name__ == "__main__":
	# Someone is launching this directly
	parseXML()

