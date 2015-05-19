#############################################################
# Author: Jared McArthur
# Date:     03/11/2015	
#
#############################################################

import json
from urllib import urlopen
from urllib2 import Request, urlopen
from urllib2 import URLError, HTTPError
#import us
import os
import pprint

class EIAgov(object):
    def __init__(self, token, series):
        '''
        Purpose:
        Initialise the EIAgov class by requesting:
        - EIA token
        - id code(s) of the series to be downloaded

        Parameters:
        - token: string
        - series: string or list of strings
        '''
        self.token = token
        self.series = series
        self.data = None

    '''
    def __repr__(self):
        return str(self.series)
    '''

    def Raw(self, ser):
        # Construct url
        url = 'http://api.eia.gov/series/?api_key=' + self.token + '&series_id=' + ser.upper()

        try:
            # URL request, URL opener, read content
            req = Request(url)
            opener = urlopen(req)
            content = opener.read().decode() # Convert bytes to UTF-8

            # Jsonify 'content' object
            jso = json.loads(content)
            return jso

        except HTTPError as e:
            print('HTTP error type.')
            print('Error code: ', e.code)

        except URLError as e:
            print('URL type error.')
            print('Reason: ', e.reason)

    def GetData(self):
        # Deal with the date series                       
        # The pretty print stuff is added my jm for debugging
        pp = pprint.PrettyPrinter(indent=4)
        
        # date_ is a JSON object at this point
        for i in self.series:
          #print i
          #date_ = self.Raw(self.series[0])        
          date_ = self.Raw(i)
          self.data = date_
          #print "Printing self.data:\n",self.data['series'][0]['series_id']
        
          date_series = date_['series'][0]['data']
          endi = len(date_series) # or len(date_['series'][0]['data'])
        
          date = []
          for j in range (endi):
             date.append(date_series[j][0])
          #print "Printing date:\n",date
				
          self.PrintData()
#        return date_

    def PrintData(self):
        # Create an appropriate filename and generate SQL INSERT statements for that series.
         f = open("./output/"+self.data['series'][0]['series_id']+".sql","w")
         print "Generating INSERT statements for %s" % (self.data['series'][0]['series_id'])
         for i in self.data['series'][0]['data']:
           line = "INSERT INTO %s (DATE,PRICE) VALUES (%s, %s)\n" %(self.data['series'][0]['series_id'],i[0],i[1])
           #print line
           f.write(line)
         f.close()


def buildLists():
# create a list of state abbreviations for series id and filenames
  abb = []
  abb = [u'AL', u'AK', u'AZ', u'AR', u'CA', u'CO', u'CT', u'DE', u'DC', u'FL', u'GA', u'HI', u'ID', u'IL', u'IN', u'IA', u'KS', u'KY', u'LA', u'ME', u'MD', u'MA', u'MI', u'MN', u'MS', u'MO', u'MT', u'NE', u'NV', u'NH', u'NJ', u'NM', u'NY', u'NC', u'ND', u'OH', u'OK', u'OR', u'PA', u'RI', u'SC', u'SD', u'TN', u'TX', u'UT', u'VT', u'VA', u'WA', u'WV', u'WI', u'WY']
  ''' 
  for i in us.states.STATES:
    abb.append(i.abbr)
  '''
  abb.remove('DC')
  return abb

def generateOutfiles():
# use list of abbreviations and generate a filename/series ID for
# every state. 
# TODO: Generalize this function
  if not os.path.exists("./output"):
    os.makedirs("./output")
  abb = buildLists()

  names = []
  for a in abb:
    names.append("ELEC.REV." + a + "-ALL.M")
  return names

############################################################
# Main program starts below                                #
############################################################

if __name__ == '__main__':
    tok = 'YOUR API TOKEN HERE'

    '''
    # Crude oil production
    prod = ['PET.MCRFPAL2.M'] # this is a perfect set to generalize the filename generator
    data = EIAgov(tok,prod)
    data.GetData()

       
    # Crude spot prices - daily data
    crude = ['PET.RWTC.D', 'PET.RBRTE.D']
    data = EIAgov(tok, crude)
    data.GetData()
    '''
    # Electricity - ALL Monthly data
    
    #test = ['ELEC.REV.AL-ALL.M', 'ELEC.REV.AK-ALL.M', 'ELEC.REV.CA-ALL.M']
    series = generateOutfiles()
    data = EIAgov(tok, generateOutfiles())
    data.GetData()
    #print(data.GetData())
     
    '''    
    # Petroleum and products imports - quarterly data
    test2 = ['STEO.RNNIPUS.Q', 'STEO.PAIMPORT.Q', 'STEO.UONIPUS.Q']
    data = EIAgov(tok, test2)
    data.GetData()
    #print(data.GetData())

    
    # Petroleum and products supply - annual data
    test3 = ['STEO.DFPSPP1.A', 'STEO.DFPSPP2.A', 'STEO.DFPSPP3.A', 'STEO.DFPSPP4.A', 'STEO.DFPSPP5.A']
    data = EIAgov(tok, test3)
    data.GetData()
    #print(data.GetData())
    
     
    # US ethanol output - weekly data
    test4 = ['PET.W_EPOOXE_YOP_NUS_MBBLD.W', 'PET.W_EPOOXE_YOP_R10_MBBLD.W', 'PET.W_EPOOXE_YOP_R20_MBBLD.W', 'PET.W_EPOOXE_YOP_R30_MBBLD.W', 'PET.W_EPOOXE_YOP_R40_MBBLD.W', 'PET.W_EPOOXE_YOP_R50_MBBLD.W']
    data = EIAgov(tok, test4)
    data.GetData()
    #print(data.GetData())
    '''    	
