""" This module is for using the EIA API for accessing
data series """
import requests, json, sys

def getData(*args):
	print args

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
	print "Please don't try to run me"
