#!/usr/bin/env python
# $Id: ddmin.py,v 2.2 2005/05/12 22:01:18 zeller Exp $

import outputters
from xml.parsers.xmlproc import xmlproc
from split import split
from listsets import listminus
import re

PASS       = "PASS"
FAIL       = "FAIL"
UNRESOLVED = "UNRESOLVED"

def ddmin(circumstances, test):
	"""Return a sublist of CIRCUMSTANCES that is a relevant configuration
	   with respect to TEST."""
	
	assert test([]) == PASS
	assert test(circumstances) == FAIL

	n = 2
	while len(circumstances) >= 2:
		subsets = split(circumstances, n)
		assert len(subsets) == n

		some_complement_is_failing = 0
		for subset in subsets:
			complement = listminus(circumstances, subset)

			if test(complement) == FAIL:
				circumstances = complement
				n = max(n - 1, 2)
				some_complement_is_failing = 1
				break

		if not some_complement_is_failing:
			if n == len(circumstances):
				break
			n = min(n * 2, len(circumstances))

	return circumstances



if __name__ == "__main__":
	tests = {}
	circumstances = []

	def string_to_list(s):
		c = []
		for i in range(len(s)):
			c.append((i, s[i]))
		return c
		
	def read_file(filename):
		with open (filename, "r") as myfile:
			data=myfile.read()
		return data
	
	def mytest(c):
		# Sticky sticky
		xml = ""
		for (index, char) in c:
			xml += char

		# Write File
		fn = 'ddtmp.xml'
		f = open(fn,'w')
		f.write(xml)
		f.close() 
		
		# Initial		
		app	= xmlproc.Application()
		p	= xmlproc.XMLProcessor()
		err = outputters.MyErrorHandler(p, p, 0, 0, 0)
		
		p.set_error_handler(err)
		
		try:			
			p.parse_resource(fn)
		except:
			#print err
			print FAIL
			return FAIL
		print PASS
		return PASS
	
	circumstances = string_to_list(read_file("demo/urls.xml"))
	mytest(circumstances)
	print ddmin(circumstances, mytest)
