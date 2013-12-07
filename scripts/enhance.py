# Enhance.py
# Author: Myles Tan
# December 7th, 2013

# Takes the syde employment spreadsheets, and fills in missing information.

# Imports
import os

# we run it for each of the files:
for filename in glob.glob("/Users/mylestan/Git/syde-employment-data/raw/*.csv"):
	with open("../raw/" + filename):
		# tbc