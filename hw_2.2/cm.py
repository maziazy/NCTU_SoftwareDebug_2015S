#!/usr/bin/python
import xml.etree.cElementTree as ET
from os import listdir
from os.path import isdir, isfile, join


XML_HEADER	= """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="cmreport.xsl"?>\n\n"""

SXML_PATH	= "xml_success"
FXML_PATH	= "xml_fail"
RESULT_PATH	= "report.xml"

DSTAR_PARA	= 1

def listfiles(path):
	return [ f for f in listdir(path) if isfile(join(path,f)) ]
	
def checkFiles():
	if not isdir(SXML_PATH):
		print("Cannot find directory: "+SXML_PATH)
		return 1
	if not isdir(FXML_PATH):
		print("Cannot find directory: "+FXML_PATH)
		return 1
	if len(listfiles(SXML_PATH)) < 1:
		print("Need at least one successful test case")
		return 1
	if len(listfiles(FXML_PATH)) < 1:
		print("Need at least one fail test case")
		return 1
	return 0
def buildTemplate():
	path = join(SXML_PATH, listfiles(SXML_PATH)[0])
	tree = ET.ElementTree(file=path)
	
	for xline in tree.iter('line'):
		xline.attrib.pop('hits')
		xline.set('s', '0')
		xline.set('f', '0')
	
	return tree
# TODO: Fix the bad performence due to XPATH
def countHits(tag, path, report):
	if tag != 's' and tag != 'f':
		print("in procXML(): tag must be 's' or 'f'")
		return
	
	tree = ET.ElementTree(file=path)
	
	for xpackage in tree.iter('package'):
		for xclass in xpackage.iter('class'):
			for xline in xclass.iter('line'):
				pname	= xpackage.get('name')
				cname	= xclass.get('name')
				number	= xline.get('number')
				xpath = ".//package[@name='"+pname+"']//class[@name='"+cname+"']//line[@number='"+number+"']"
				
				# Update cover count
				if xline.get('hits') == '0':
					continue
				target = report.find(xpath)
				target.set(tag, str(int(target.get(tag))+1))
def calMetrics(Ns, Nf, report):
	Ns = float(Ns)
	Nf = float(Nf)
	
	for xline in report.iter('line'):
		Ncs = float(xline.get('s'))
		Ncf = float(xline.get('f'))		
		
		# Metrics 1
		if Ncf != 0:
			m1 = (Ncf/Nf) / ((Ncf/Nf) + (Ncs/Ns))
		else:
			m1 = 0
			
		# Metrics 2
		if Ncf != 0:		
			m2 = Ncf / (Nf*(Ncf+Ncs))**(.5)
		else:
			m2 = 0
		
		# Metrics 3
		m3 = Ncf - Ncs/(Ns+1)
		
		# Metrics 4
		if Nf-Ncf+Ncs != 0:
			m4 = (Ncf**DSTAR_PARA) / (Nf-Ncf+Ncs)
		else:
			m4 = "Inf"
		
		# Update XML
		xline.set('m1', str(m1))
		xline.set('m2', str(m2))
		xline.set('m3', str(m3))
		xline.set('m4', str(m4))
	
def main():
	if checkFiles():
		return
		
	# Build Template
	report = buildTemplate()
		
	# Hits count
	for file in listfiles(SXML_PATH):
		countHits('s', join(SXML_PATH, file), report)
	for file in listfiles(FXML_PATH):
		countHits('f', join(FXML_PATH, file), report)
		
	# Calculate Metrics
	ns = len(listfiles(SXML_PATH))
	nf = len(listfiles(FXML_PATH))
	calMetrics(ns, nf, report)
		

	with open(RESULT_PATH, 'w') as output:
		output.write(XML_HEADER)
		report.write(output, xml_declaration=False, encoding='utf-8') 

if __name__ == "__main__":
	main()