# Enhance.py
# Author: Myles Tan
# December 7th, 2013

# Takes the syde employment object and fills in missing information.

# Imports
import os, csv, glob, config
from datetime import datetime
import simplejson as json

import gmaps
gmaps.setApiKey(config.gmapsKey)

import linkedin
linkedin.setApiKey(config.linkedinKey)
linkedin.login()

import log
log.setPath("../logs/enhance-log.txt")

# Load the data file
profiles = {}
with open("../data/coop-profiles.txt", "r") as f:
	profiles = json.loads(f.read())

# Now we iterate through each profile, and each term within it, adding info where missing.
for profileKey in profiles:
	for termKey in profiles[profileKey]:
		p = profiles[profileKey][termKey] # for ease

		#####
		# We pull the company's data from linkedin
		# If the company url isn't set, we use the linekdin one
		# If the company industry isnt set, we set that one
		# In addition, we pull the company's size and status
		#####

		# Search for  the company
		log.rec("Search for company: " + p['employer'], True)
		searchResults = linkedin.searchForCompany(p['employer'])

		# Is the first one what we're looking for?
		log.rec(p['name'] + " worked at " + p['employer'] + ".\nLinkedin search found a company: " + searchResults[0]['name'], True)
		resp = raw_input("Would you like to use the data from this company? (y/n)")

		if resp is 'y': # Yay! use the data

			# get company data
			companyData = linkedin.getCompanyDetails(searchResults[0]['id'])

			# and update the site
			if 'employerUrl' in companyData:
				log.rec("Adding website url: " + companyData['employerUrl'], True)
				p['employerUrl'] = companyData['employerUrl']
			if 'industry' in companyData:
				log.rec("Adding industry: " + companyData['industry'], True)
				p['industry'] = companyData['industry']
			if 'employeeCountRange' in companyData:
				log.rec("Adding employee count range: " + companyData['employeeCountRange'], True)
				p['employeeCountRange'] = companyData['employeeCountRange']
			#TODO: handle map location?

		else: # hmm. check the others it found?
			log.rec("It also found:", True)
			for index in range(len(searchResults)):
				log.rec(str(index) + ": " + searchResults[index]['name'], True)
			chosen = raw_input("Any of these correct?")

			if chosen in range(len(searchResults)):

				# get the company data from linkedin
				companyData = linkedin.getCompanyDetails(searchResults[chosen]['id'])

				# and update the dict
				if 'employerUrl' in companyData:
					log.rec("Adding website url: " + companyData['employerUrl'], True)
					p['employerUrl'] = companyData['employerUrl']
				if 'industry' in companyData:
					log.rec("Adding industry: " + companyData['industry'], True)
					p['industry'] = companyData['industry']
				if 'employeeCountRange' in companyData:
					log.rec("Adding employee count range: " + companyData['employeeCountRange'], True)
					p['employeeCountRange'] = companyData['employeeCountRange']

			elif chosen == 'n': # Darn. Nothing we can do right now.
				log.rec("None :( moving on.", True)

			else: # didnt' understand
				log.rec("Moving on.", True)


		#####
		# Look for a map location
		#####
		if not 'mapLocation' in p: # if map-location doesn't exist, write it
			location = gmaps.getLocation(p['city'], p['province'], p['country'], p['employer'])
			if location:
				p['mapLocation'] = location
			else:
				log.rec('no location could be found for ' + p['name'] + '. Please resolve this row.\n')

		#####
		# Add a timestamp for the start date of the co-op
		#####
		if not 'termStartTimestamp' in p:
			if p['term'] == 'winter':
				m = 1
			elif p['term'] == 'summer':
				m = 5
			else:
				m = 9
			isoDateTime = datetime(int(p['year']), m, 1).isoformat("T") + "+00:00" # calculate the iso date time format
			p['termStartTimestamp'] = isoDateTime

with open("../data/coop-profiles.txt", "w") as f:
	f.write(json.dumps(profiles))

linkedin.closeLog()
gmaps.closeLog()
