# imports
import csv, hashlib, glob
import simplejson as json
from urllib2 import urlopen, URLError
from datetime import datetime

import log
log.setPath("../logs/coop-parser-log.txt")

fileNames = []
for fname in glob.glob("/Users/mylestan/Git/syde-employment-data/raw/*.csv"):
	fileNames.append(fname)

# Read the result data into an object
with open('../data/coop-profiles.txt') as pf:
	profiles = json.loads(pf.read())
	if not profiles:
		profiles = {}

# THE FUN BEGINS HERE!!!
# Iterate through the co-op data files
for f in fileNames:
	log.rec('reading file: ' + f + '\n', True)
	with open(f) as csvFile:
		csvFile.readline() # First row is the titles: ignore
		keys = csvFile.readline().split(",") # second row is the technical property names: use this to build the properties!
		csvFile.readline() # Third row is the helper text: ignore

		fileReader = csv.DictReader(csvFile, fieldnames = keys)

		# Iterate through every line in the data file
		for row in fileReader:
			log.rec('reading a new line\n')

			# We assume that the row has these properties. They are necessary for creating the JSON structure
			name = row['name']
			year = row['year']
			term = row['term']
			termNumber = row['termNumber']

			nameHash = hashlib.sha224(name).digest().encode("hex") # hash the name
			termHash = hashlib.sha224(year + term).digest().encode("hex") # Hash the time of the term

			if not nameHash in profiles: # if name doesn't exist, make it
				profiles[nameHash] = {}

			if not termHash in profiles[nameHash]: # If term doesn't exist, make it
				profiles[nameHash][termHash] = {}

			# We only write the properties we need!
			transferKeys = ['name','classYear','year','term','termNumber','isWorking','title','employer','employerUrl','city','province','country','description','industry','sector']

			for key in transferKeys:
				if key in row:
					profiles[nameHash][termHash][key] = row[key]
				else:
					profiles[nameHash][termHash][key] = None

		# End of infoArray in fileReader
	# End of with statement for csv
# End of file loop

# Open result data file, write, Close
pf = open('../data/coop-profiles.txt', 'w')
pf.write(json.dumps(profiles))
pf.close()
