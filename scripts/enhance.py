# Enhance.py
# Author: Myles Tan
# December 7th, 2013

# Takes the syde employment spreadsheets, and fills in missing information.

# Imports
import os
import csv
import glob

# we run it for each of the files:
for filename in glob.glob("/Users/mylestan/Git/syde-employment-data/raw/*.csv"):
	print '\n\n\n' + filename + '\n\n\n'
	with open(filename) as csvfile:
		csvfile.readline() # soft titles
		keys = csvfile.readline().split(",")
		csvfile.readline() # explanation text

		csvreader = csv.DictReader(csvfile, fieldnames = keys)
		for obj in csvreader:
			print obj
			print "\n\n\n"