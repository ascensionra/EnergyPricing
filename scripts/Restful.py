import urllib,urllib2,httplib

url = 'http://http://129.152.144.84:5001/rest/native/?'

parameters = urllib.urlencode({ 'query':'INSERT INTO PET_SERIES(NAME,DESCRIPTION,SERIES_ID) VALUES ("a","b","c")','verbose':'TRUE' })

headers = {'DB':jdbc:oracle:thin:@129.152.144.84:1521/PDB1.usuniversi01134.oraclecloud.internal','USER':'cs370_jsm3287','PASS':'orcl','MODE':'native_mode','MODEL':'model','returnDimensions':'False','returnFor':'JSON','d':'i[0]','v':'i[1]' }

bigurl = url + urllib.urlencode(parameters) + urllib.urlencode(headers)

resp = urllib.urlopen(bigurl)
