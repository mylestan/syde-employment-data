from urllib2 import urlopen, URLError
import simplejson as json
import log
log.setPath("../logs/gmaps-log.txt")

url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&sensor=false&key='
apiKey = ''

# function to set the api key
def setApiKey(key):
	global apiKey
	apiKey = key

def isApiKey():
	if apiKey == '':
		print 'Warning: it appears the api key for gmaps has not been set. Please set the Api key before calling functions.'

# function which handles map requests for the given string, and returns the object
def mapsRequest(string):
	log.rec('gmaps request for string: ' + string + '\n')
	request = (url % string.replace(' ', '+')) + apiKey
	log.rec('request string: ' + request + '\n')

	try:
		response = urlopen(request)
	except URLError, e:
		log.rec('URL request failed. Reason: ' + str(e.reason))
	else:
		return json.load(response)

# function to return the map-location object for a co-op term, given the company and the location. keep this logic out of the main loop
def getLocation(city, prov, country, company = None):
	isApiKey()

	log.rec('getting map location\n')
	if company:
		log.rec('\tcompany: ' + company + '\n')
	log.rec ('\tlocation: ' + ', '.join([city,prov,country]) + '\n')

	# First we try to locate the company in the area
	reqString = ', '.join([company, city, prov, country]) if company else ', '.join([city, prov, country])
	response = mapsRequest(reqString)

	status = response['status']
	if status == 'OK':
		log.rec('\tresponse OK\n')
		# Take the first one. FAITH IN THE GOOGLES!
		first = response['results'][0]
		location = {}
		location['name'] = first['name']
		location['address'] = first['formatted_address']
		location['lat'] = first['geometry']['location']['lat']
		location['lng'] = first['geometry']['location']['lng']
		return location
	elif status == "ZERO_RESULTS":
		if company:
			log.rec('\tresponse no results, trying again for location\n')
			return getLocation(city, prov, country)
		else:
			log.rec('\tresponse no results, and no company provided. returning none. Review this entry.\n')
			return None
	else:
		log.rec('\tresponse error: ' + status + '\n')
		return None

def closeLog():
	log.close()
