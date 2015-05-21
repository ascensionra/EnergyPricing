""" This module is for using the EIA API for accessing
data series """
#TODO: fix module so it can be deployed in a working Python environment
import requests, json, sys, re

glbUrl = 'http://129.152.144.84:5001/rest/native/?query='
glbCount = 0
glbQry = '\"SELECT COUNT(1) FROM ALL_TABLES WHERE NAME = '

##############################################################################
def getSeriesData(ser,apiKey,**kwargs):
	""" Retrieves series data specified by 'ser'
and returns the standard EIA response object. Added **kwargs
to parameter list to enable flexibility for the EIA API which 
is currently in beta. Things like start and end dates can be
passed to the query. """
# TODO: check if table exists, and get LAST_UPDATED, then \
#		generate URL parameters/modifier to pull newer than
#		that date. This is being implemented with the **kwargs parameter

	url = 'http://api.eia.gov/series/?api_key=' + apiKey + '&series_id=' + ser.upper()
	
	if kwargs is not None:
		for key, value in kwargs.iteritems():
			url = url + '&' + key + '=' + value
	print 'Url: %s' % (url)

	try:
	 #return requests.get(url).json()
	 return requests.get(url)
	except requests.exceptions.RequestException,e:
		print 'The request failed: %s' % (e)
	except BaseException, e:
		print 'Unexpected exception: %s' % (e)

##############################################################################
def createTable(series_id,header):
	""" Creates a table if it does not already exits in
the Oracle database. Due to current state of RESTful
API, we cannot return a success code. Header with connection
information will need to be provided. See example. """
# TODO: check if table exists, first. Putting it in the 
#		query itself seems to break the execution.
#		May not be necessary, since the work in done server-side, and will fail
#		silently is table already exists.

	""" Example header for connecting to Oracle DB 
	head = {'DB':'jdbc:oracle:thin:@129.152.144.84:1521/PDB1.usuniversi01134.oraclecloud.internal',\
			'USER':'username','PASS':'password','MODE':'native_mode','MODEL':'model',\
			'returnDimensions':'False','returnFor':'JSON' }
	"""

	global glbUrl
	global glbCount
	#print '*****************************************************************'
	alias = getAlias(series_id,header)  
	url = glbUrl + '\'CREATE TABLE ' + alias + ' (PRICE_DATE DATE NOT NULL, PRICE NUMBER (12,3) )\'' 
	#print 'Attempting to create table ' + alias + '\nUsing url ' + url
	glbCount += 1 # this is for debugging to detect name collisions

	try:
		return requests.get(url,headers=header)
	except requests.exceptions.RequestException,e:
		print 'The request failed: %s' % (e)

##############################################################################
def getAlias(series_id,header):
	""" Returns the alias for the series_id from the ALIASES table
for the createTable method. Eliminated need for double-quoting table name
and keeps names (nominally) under 30 bytes """

	global glbUrl
	qry = '\"SELECT * FROM ALIASES WHERE NAME = \'' + series_id + '\'\"'
	url = glbUrl + qry
	#print 'Trying to get alias for ' + series_id + '\nUsing url ' + url

	try:	
		s = json.loads(re.sub(',\]',']',requests.get(url,headers=header).text))
#		printDict(s,'k')
		return str(s['ALIAS'][0])
	except requests.exceptions.RequestException,e:
		print 'The request failed: %s' % (e)
		print('Reason: ', e.reason)
	except BaseException, e:
		print 'Unexpected error: %s' % (e)

##############################################################################
def checkExists(alias,header):
	""" Checks if a table exists """
	global glbUrl

	print glbUrl + qry + alias
	#return requests.get(glbUrl + qry,headers=header)
"""
	try: 
		if ((requests.get(url,headers=header)):
			return -1
		else:
			return 1
	except requests.exceptions.RequestException,e:
		print 'The request failed: %s' % (e)
		print('Reason: ', e.reason)
	except BaseException, e:
		print 'Unexpected error: %s' % (e)
"""
##############################################################################
def dropTable(series_id,header):
	""" Drops the specified table from the Oracle database. 
Due to current state of RESTful API, we cannot return a success code. 
Header with connection information will need to be provided. See example. """

	""" Example header for connecting to Oracle DB 
	head = {'DB':'jdbc:oracle:thin:@129.152.144.84:1521/PDB1.usuniversi01134.oraclecloud.internal',\
			'USER':'username','PASS':'password','MODE':'native_mode','MODEL':'model','returnDimensions':'False','returnFor':'JSON' }
	"""

	global glbUrl
	alias = getAlias(series_id, header)
	url = glbUrl + '\"DROP TABLE ' + alias + '\"' 
	print 'Attempting to drop table ' + alias + '\nUsing url ' + url
	try:
		return requests.get(url,headers=header)
	except requests.exceptions.RequestException,e:
		print 'The request failed: %s' % (e)
	except BaseException, e:
		print 'Unknown exception: %s' % (e)

##############################################################################
def truncateTable(series_id,header):
	""" Truncates the specified table from the Oracle database. 
Due to current state of RESTful API, we cannot return a success code. 
Header with connection information will need to be provided. See example. """

	""" Example header for connecting to Oracle DB 
	head = {'DB':'jdbc:oracle:thin:@129.152.144.84:1521/PDB1.usuniversi01134.oraclecloud.internal',\
			'USER':'username','PASS':'password','MODE':'native_mode','MODEL':'model','returnDimensions':'False','returnFor':'JSON' }
	"""

	global glbUrl
	alias = getAlias(series_id, header)
	url = glbUrl + '\'TRUNCATE TABLE ' + alias + '\'' 
	print 'Attempting to drop table ' + alias + '\nUsing url ' + url
	try:
		return requests.get(url,headers=header)
	except requests.exceptions.RequestException,e:
		print 'The request failed: %s' % (e)
	except BaseException, e:
		print 'Unknown exception: %s' % (e)

##############################################################################
def insertRecords(seriesJson,h):
	""" Generate insert statements, and load data into table.
Must supply headers as in createTable """

	global glbUrl
	global glbCount
	newestDate = None
	count = 0

	try:
		for i in seriesJson['series'][0]['data']:
			count += 1 # for debugging
			glbCount += 1
			series_id = seriesJson['series'][0]['series_id']
			series_name = seriesJson['series'][0]['name']
			alias = getAlias(series_id,h)
			
			print "Processing %s" % (series_id)
			print "\tAlias for %s: %s" % (series_id,alias)
			
			qry = '"""INSERT INTO %s (PRICE_DATE,PRICE) VALUES (TO_DATE(\'%s\',\'yyyymmdd\'),TO_NUMBER(\'%s\'))"""' \
				% (alias,i[0],i[1])#,seriesJson['series'][0]['series_id'])
			
			if ( i[0] > newestDate ):
				newestDate = i[0]
			url = glbUrl + qry
			
			print "\tInserting %s, %s\t\t%d\n\tUsing URL %s" % (i[0],i[1],count,url)
			print requests.get(url,headers=h)
			#if count > 10: 
			#	break
		setLastUpdated(newestDate,series_id,series_name,h)

	except requests.exceptions.RequestException,e:
		print 'The request failed: %s' % (e)
	except BaseException,e:
		print 'Unexpected exception: %s' % (e)
		return
	finally:
		return glbCount

##############################################################################
def setLastUpdated(date,series_id,series_name,h):
	""" Prints JSON dictionary of a successful """
	global glbUrl

	try:
		qry = '"INSERT INTO LAST_UPDATE (SERIES,SERIES_NAME,UPDATED) VALUES (\'%s\',\'%s\',TO_DATE(\'%s\',\'yyyymmdd\'))"' \
			% (series_id,series_name,date)
		url = glbUrl + qry
		#print "Updating LAST_UPDATE for %s \n using URL: %s" % ( seriesJson['series'][0]['series_id'],url2 )
		requests.get(url,headers=h)	
	except requests.exceptions.RequestException,e:
		print 'The request failed: %s' % (e)
	except BaseException,e:
		print 'Unexpected exception: %s' % (e)

##############################################################################
def printJson(response):
	""" Prints JSON dictionary of a successful
response in a nice format """
	try:
		if (isinstance(response,dict)):
			print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
		else:
			print json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '))
	except ValueError,e:
		print 'Decoding JSON has failed: %s' % (e)
	except BaseException,e:
		print 'Unexpected exception: %s' % (e)

##############################################################################
def writeJson(response,filename):
	""" Writes JSON dictionary of a successful
response in a nice format to a file """
	try:
			
		with open(filename,'w') as f:
			if (isinstance(response,dict)):
				f.write(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))
			else:
				f.write(json.dumps(response.json(),sort_keys=True, indent=4, separators=(',', ': ')))
	except IOError,e:
		print "I/O error ((0)): (1)".format(e.errno, e.strerror)
	except BaseException,e:
 		print 'Undexpected error: %s' % (e)

##############################################################################
def printDict(dictionary,sortVal):
	""" Prints out the contents of a dictionary in a nice format
using OrderedDict from collections to sort the dict.""" 
	from collections import OrderedDict as OD
	try:
		if (sortVal.upper() == 'K' or sortVal.upper() == 'KEY'):
			ordered = OD(sorted(dictionary.items(), key = lambda t: t[0]))
		else:
			ordered = OD(sorted(dictionary.items(), key = lambda t: t[1], reverse=True))
		for key in ordered:
			print '%s: %s' % (key,ordered[key])
	except BaseException,e:
		print 'Unexpected error: %s' % (e)

##############################################################################
if __name__ == '__main__':
	#print "Please don't try to run me"
	exit
