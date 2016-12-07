import oauth2 as oauth
import simplejson as json
import httplib2
import time, os
import urllib2

import log
log.setPath('../logs/linkedin-log.txt')

# global vars, need access across functions
linkedinKey = None
client = None

### function setApiKey
## keyObj: (dict) contains the four keys: consumerKey, consumerSecret, userToken, userSecret.
# Used to set the api key variable used to login. Also gives the option to login automatically.
def setApiKey(keyObj, login = False):
	global linkedinKey
	linkedinKey = keyObj
	if login:
		login()



### function isKeySet
# Used to check if the key values have been stored internally.
# Used mostly for internal functions as a check before they try to make an API call.
def isKeySet():
	if linkedinKey == None:
		log.rec('linkedin eror: it appears the key is not set.', True)



### function login
# Uses the keys and runs through the oauth process with the linkedin api.
def login():
	# Use your API key and secret to instantiate consumer object
	consumer = oauth.Consumer(linkedinKey['consumerKey'], linkedinKey['consumerSecret'])

	# Use the consumer object to initialize the client object
	client = oauth.Client(consumer)

	# Use your developer token and secret to instantiate access token object
	access_token = oauth.Token(key=linkedinKey['userToken'],secret=linkedinKey['userSecret'])

	# update the global var
	global client
	client = oauth.Client(consumer, access_token)



### function searchForCompany
## companyName: (string) the name of the company searching for
# returns a list of dicts, each containing the name and id of a potential company match in linkedin
def searchForCompany(companyName):
	log.rec('Search for: ' + companyName)

	response,content = client.request("http://api.linkedin.com/v1/company-search?keywords={" + urllib2.quote(companyName) + "}&format=json", "GET", "")
	content = json.loads(content)

	if int(response['status']) is not 200: # handle bad request
		# print response['status']
		# print u'200'
		# print response['status'] is not '200'
		log.rec("Oops, something went wrong with the URL request. Status code: " + response['status'], True)
		log.rec(response, True)
		return None
	elif content['numResults'] == 0: # no results
		log.rec('no results were found for company name: ' + companyName, True)
		return None
	else: # return the company list if found
		return content['companies']['values']



### function getCompanyDetails
## companyId: (int) the unique name of the company within linkedin.
##			   	This can be found by using searchForCompany with a generic company name
# Returns a dict containing the relevant details of a company for enhance.py.
def getCompanyDetails(companyId):
	log.rec('Search for: ' + str(companyId))

	# Make request, load the reponse and content
	requestList = ['name','industries','website-url','locations:(address)','employee-count-range','status']
	response,content = client.request("http://api.linkedin.com/v1/companies/" + str(companyId) + ":(" + ",".join(requestList) + ")?format=json", "GET", "")

	content = json.loads(content)

	if int(response['status']) is not 200: # handle bad request
		log.rec("Oops, something went wrong with the URL request. Status code: " + response['status'], True)
		log.rec(response)
		return None

	else:
		log.rec("company details:")
		log.rec(json.dumps(content))

		company = {}
		company['employerUrl'] = content['websiteUrl']
		company['industry'] = content['industries']['values'][0]['name']
		company['employeeCountRange'] = content['employeeCountRange']['name']
		company['location'] = content['locations']['values'][0]['address']

		return company

### Function closeLog
# Closes the log file being used by this script.
# This function should always be called before closing the parent script.
def closeLog():
	log.close()

