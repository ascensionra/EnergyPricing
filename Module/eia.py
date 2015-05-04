""" This module is for using the EIA API for accessing
data series """
import requests, json, sys

def getSeriesData(ser,apiKey):
	""" Retrieves series data specified by 'ser'
and returns the standard EIA JSON object """
	url = 'http://api.eia.gov/series/?api_key=' + apiKey + '&series_id=' + ser.upper()
	try:
	 return requests.get(url).json()
	except HTTPError as e:
		print('HTTP error type.')
		print('Error code: ', e.code)

	except URLError as e:
		print('URL type error.')
		print('Reason: ', e.reason)

def createTable(series_id,header):
	""" Creates a table if it does not already exits in
the Oracle database. Due to current state of RESTful
API, we cannot return a success code. Header with connection
information will need to be provided. See example. """

	""" Example header for connecting to Oracle DB 
	head = {'DB':'jdbc:oracle:thin:@129.152.144.84:1521/PDB1.usuniversi01134.oraclecloud.internal',\
			'USER':'username','PASS':'password','MODE':'native_mode','MODEL':'model','returnDimensions':'False','returnFor':'JSON' }
	"""
	series_id = "\"" + series_id + "\""
	url = 'http://129.152.144.84:5001/rest/native/?query=\'CREATE TABLE IF NOT EXISTS ' + series_id + \
			' (PRICE_DATE DATE NOT NULL, PRICE NUMBER)\''
	print 'Attempting to create table ' + series_id + '\nUsing url ' + url
	return requests.get(url,headers=header)

def printJson(response):
  """ Prints JSON dictionary of a successful
response in a nice format """
  try:
    print json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '))
  except ValueError,e:
    print 'Decoding JSON has failed: %s' % (e)
  return

def writeJson(response,filename):
  """ Writes JSON dictionary of a successful
response in a nice format to a file """
  try:
    with open(filename,'w') as f:
      f.write(json.dumps(response.json(),sort_keys=True, indent=4, separators=(',', ': ')))
  except IOError,e:
    print "I/O error ((0)): (1)".format(e.errno, e.strerror)
  except BaseException,e:
    print 'Undexpected error: %s' % (e)
  return

if __name__ == '__main__':
	#print "Please don't try to run me"
	exit
