logFile = None

def setPath(path):
	global logFile
	logFile = open(path, 'w')

def isPathSet():
	if logFile is None:
		print 'log warning: log path is not set.'

# logging function that writes to a log file and optionally to console
def rec(msg, printInConsole = False):
	isPathSet()

	logFile.write(str(msg).encode('utf-8'))
	if printInConsole:
		print str(msg).encode('utf-8')

def close():
	logFile.close()