""" This module is for using the EIA API for accessing
data series """
#TODO: fix module so it can be deployed in a working Python environment
import requests, json, sys, re

glbUrl = 'http://129.152.144.84:5001/rest/native/?query='
glbCount = 0

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

	""" This can be used to pull data in a time frame by passing
{"start":"YYYY-MM-DD"} according to API documentation. An function call can be
<eia.>getSeriesData(series,apiKey,**{'start':'2015-05-15'}) """

	url = 'http://api.eia.gov/series/?api_key=' + apiKey + '&series_id=' + ser.upper()
	
	if kwargs is not None:
		for key, value in kwargs.iteritems():
			url = url + '&' + key + '=' + value
	try:
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
	try:
		alias = getAlias(series_id,header)  
		if alias is None:
			return
		url = glbUrl + '\'CREATE TABLE ' + alias + ' (PRICE_DATE DATE NOT NULL, PRICE NUMBER (12,3) )\'' 
		r=requests.get(url,headers=header)
		if (r.json().values()[0] == []):
			print r.text
			return None
	except requests.exceptions.RequestException,e:
		print 'The request failed: %s' % (e)
	except BaseException, e:
		print 'Unexpected error: %s' % (e)

##############################################################################
def getAlias(series_id,header):
	""" Returns the alias for the series_id from the ALIASES table
for the createTable method. Eliminated need for double-quoting table name
and keeps names (nominally) under 30 bytes """

	global glbUrl
	qry = '\"SELECT * FROM ALIASES WHERE NAME = \'' + series_id + '\'\"'
	url = glbUrl + qry
	regex = re.compile(',\]')

	try:	
#		if (not checkExists(series_id,header)):
#			return None
		r = requests.get(url,headers=header)
		s = json.loads(re.sub(regex,']',r.text))
		#if (r.json().values()[0] == []):
		#	print r.text
		#	return None
		return str(s['ALIAS'][0])
	except requests.exceptions.RequestException,e:
		print 'The request failed: %s' % (e)
	except BaseException, e:
		print 'Unexpected error: %s' % (e)

##############################################################################
def checkExists(alias,header):
	""" Checks if a table exists """
	global glbUrl

	qry = '\"SELECT COUNT(1) FROM ALL_TABLES WHERE TABLE_NAME=\''
	url = glbUrl + qry + alias + '\'\"'
	regex = re.compile(',\]')

	try: 
		r = requests.get(url,headers=header)
		if not r.status_code == 200:
			return False
		s = json.loads(re.sub(regex,']',r.text))
		if (s['COUNT(1)'][0] > 0):
			return True
		else:
			return False 
	except requests.exceptions.RequestException,e:
		print 'The request failed: %s' % (e)
	except BaseException, e:
		print 'Unexpected error: %s' % (e)

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
	print 'Attempting to truncate table ' + alias + '\nUsing url ' + url
	try:
		return requests.get(url,headers=header)
	except requests.exceptions.RequestException,e:
		print 'The request failed: %s' % (e)
	except BaseException, e:
		print 'Unknown exception: %s' % (e)

##############################################################################
def dateAdd(date):
	""" This method will do a quick time delta for the last updated value to
create the relevant parameter for calling a limited dataset in updateTable()
"""
	import datetime as dt
	try:
		date = dt.datetime.strptime(date,'%Y-%m-%d')
		delta = dt.timedelta(days=1)
		newdate = (str((date+delta).date())).split("-")
		return (newdate[0]+newdate[1]+newdate[2])
	except BaseException,e:
		print 'Unexpected exception: %s' % (e)

##############################################################################
def updateTable(series_id,header,tok):
	""" This method checks LAST_UPDATE for the series_id and returns the date
of the last data point entered into database. If series_id is not in the
table, then checkExists() is called. If that is false, createTable() is
called, followed by getSeriesData() and insertRecords(). If true, all
data is retrieved from EIA wirh getSeriesData() call and insertRecords(). """

	try:
		# Check for entry in LAST_UPDATE table
		lastUpdate = getLastUpdated(series_id,header)
		if (lastUpdate is None):		
			print 'No last updated entry for %s' % (series_id)
			alias = getAlias(series_id,header)
			if (alias is None):		# if there is no entry in the alias table
				ra = series_id.split(".")		# Split up the long series name
				alias = ra[1]+ra[-1]		# Create new alias
				print 'No alias for %s, created %s' % (series_id,alias)
			"""
			if (not checkExists(alias,header)):	# See if table exists despite missing alias
				print 'Creating table %s' % (alias)
				r = createTable(alias,header) # Create a table if not 
				if r is None:
					return
			"""
			print checkExists(alias,header)
			if checkExists(alias,header):
				data = getSeriesData(series_id,tok)
				insertRecords(data.json(),header)
			else:
				print 'No table exists for %s' % (alias)
		else:
			print 'Last update for %s: %s' % (series_id,lastUpdate)
			newdate = dateAdd(lastUpdate)
			print 'Getting data since %s' % (newdate)
			data = getSeriesData(series_id,tok,**{'start':newdate})
			if (data.json()['series'][0]['data'] == []):
				print 'Nothing to update'
				return
			insertRecords(data.json(),header)
	except requests.exceptions.RequestException,e:
		print 'The request failed: %s' % (e)
	except BaseException, e:
		print 'Unknown exception: %s' % (e)

##############################################################################
def insertRecords(seriesJson,h):
	""" Generate insert statements, and load data into table.
Must supply headers as in createTable """

	global glbUrl
	newestDate = None
	count = 0

	try:
		for i in seriesJson['series'][0]['data']:
			series_id = seriesJson['series'][0]['series_id']
			series_name = seriesJson['series'][0]['name']
			alias = getAlias(series_id,h)
			#print "Processing %s" % (series_id)
			#print "\tAlias for %s: %s" % (series_id,alias)
			qry = '"""INSERT INTO %s (PRICE_DATE,PRICE) VALUES (TO_DATE(\'%s\',\'yyyymmdd\'),TO_NUMBER(\'%s\'))"""' \
				% (alias,i[0],i[1])
			if ( i[0] > newestDate ):
				newestDate = i[0]
			url = glbUrl + qry
			count += 1
			print "\tInserting %s, %s into %s\t\t%d" % (i[0],i[1],alias,count)
			requests.get(url,headers=h)
		setLastUpdated(newestDate,series_id,series_name,h)
		count = 0
	except requests.exceptions.RequestException,e:
		print 'The request failed: %s' % (e)
	except BaseException,e:
		print 'Unexpected error: %s' % (e)
		return

##############################################################################
def deleteRecords(table,conditions,h):
	""" Will remove records from specified table that match the conditions specified. Accepts conditions as a dictionary. """
	global glbUrl

	try:
		for i in conditions:
			for j in conditions[i]:
				url = glbUrl + '"DELETE FROM %s WHERE %s = \'%s\'"' % (table,i,j) 
				print url
				return requests.get(url,headers=h)
	except requests.exceptions.RequestException,e:
		print 'The request failed: %s' % (e)
	except BaseException,e:
		print 'Unexpected exception: %s' % (e)

##############################################################################
def getLastUpdated(series_id,header):
	""" Retrieves last updated value from LAST_UPDATE for the specified series. """
	global glbUrl

	try:
		qry = '"SELECT UPDATED FROM LAST_UPDATE WHERE SERIES = \'' + series_id + '\'"'
		url = glbUrl + qry
		r = requests.get(url,headers=header)
		s = json.loads(re.sub(',\]',']',r.text))
		if not s['UPDATED']:
			return None
		else:
			return s['UPDATED'][0].split(" ")[0]
 	except requests.exceptions.RequestException,e:
 		print 'The request failed: %s' % (e) 
	except BaseException,e:
		print 'Unexpected exception: %s' % (e)

##############################################################################
def setLastUpdated(date,series_id,series_name,h):
	""" Updates the series entry in LAST_UPDATE with the most recent data value retrieved from EIA datastores.
Returns Requests response object. """
	global glbUrl

	try:
		if (getLastUpdated(series_id,h) is None):	# Check for existing entry in LAST_UPDATE table
			if (getAlias(series_id,h) is None):		# If None, check if table exists.
				return None							# If table does not exist, return None
			qry = '"INSERT INTO LAST_UPDATE (SERIES,SERIES_NAME,UPDATED) VALUES (\'%s\',\'%s\',TO_DATE(\'%s\',\'yyyymmdd\'))"' \
				% (series_id,series_name,date)
			url = glbUrl + qry
			return requests.get(url,headers=h)
		else:		# If an entry exists, update it
			qry = '"UPDATE LAST_UPDATE SET UPDATED = TO_DATE(\'%s\',\'yyyy-mm-dd\') WHERE SERIES = \'%s\'"' % (date,series_id)
			url = glbUrl + qry
			return requests.get(url,headers=h)
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
	exit
