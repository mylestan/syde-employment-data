# imports
import config
import simplejson as json
from urllib2 import urlopen, URLError
from datetime import datetime
import csv
import hashlib
import glob

import gmaps
gmaps.setApiKey(config.googleApiKey)

import linkedin
linkedin.setApiKey(config.linkedInKey)
linkedin.login()

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

# Create a csv writer for putting the data into a csv
# pfcsv = open("coop-profiles.csv", "wb")
# pfwriter = csv.writer(pfcsv, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)

# THE FUN BEGINS HERE!!!
# Iterate through the co-op data files
for f in range(len(fileNames)):
	log.rec('reading file: ' + fileNames[f] + '\n', True)
	with open(fileNames[f]) as csvFile:
		fileReader = csv.reader(csvFile)

		fileCols = fileReader.next() # First row is the titles: ignore
		propertyCols = fileReader.next() # second row is the technical property names: use this to build the properties!
		helperCols = fileReader.next() # Third row is the helper text: ignore

		# Iterate through every line in the data file
		for infoArray in fileReader:
			log.rec('reading a new line\n')

			# Read the row into a dict
			row={}
			for colIndex in range(len(propertyCols)):
				row[propertyCols[colIndex]] = infoArray[colIndex] # For each column in the sheet, we make a property for the 'row' with the appropriate property name.

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

			# if not 'mapLocation' in profiles[nameHash][termHash]: # if map-location doesn't exist, write it
			# 	location = gmaps.getLocation(row['city'], row['province'], row['country'], row['employer'])
			# 	if location:
			# 		profiles[nameHash][termHash]['mapLocation'] = location
			# 	else:
			# 		log.rec('no location could be found for ' + row['name'] + '. Please resolve this row.\n')

			# if 'mapLocation' in profiles[nameHash][termHash]:
			# 	# write all of the important into into a the csv file as well - this is for trasferring into a database if you wanted.
			# 	p = profiles[nameHash][termHash] # for ease
			# 	# calculate the iso date time format
			# 	if p['term'] == 'winter':
			# 		m = 1
			# 	elif p['term'] == 'summer':
			# 		m = 5
			# 	else:
			# 		m = 9
			# 	isoDateTime = datetime(int(p['year']), m, 1).isoformat("T") + "+00:00"

				# pString = [nameHash, termHash, p['classYear'], p['termNumber'], p['mapLocation']['lat'], p['mapLocation']['lng'], p['title'], p['employer'], p['employerUrl'], p['city'], p['province'], p['country'], p['industry'], p['description']]
				# pfwriter.writerow(pString)

		# End of infoArray in fileReader
	# End of with statement for csv
# End of file loop

# Open result data file, write, Close
pf = open('../data/coop-profiles.txt', 'w')
pf.write(json.dumps(profiles))
pf.close()

# close the csv
# pfcsv.close()
