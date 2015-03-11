#############################################################
# Edouard TALLENT @TaGoMa . Tech, November, 2014
# EIA data interface
# QuantCorner @ https://quantcorner.wordpress.com
#
# Modified: Jared McArthur
# Date:     03/11/2015	
#
#############################################################

import json
#import numpy as np
#import pandas as pd
from urllib import urlopen
from urllib2 import Request, urlopen
from urllib2 import URLError, HTTPError
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
        
        date_ = self.Raw(self.series[0])        
        
#        pp.pprint(date_)
        
        date_series = date_['series'][0]['data']
        endi = len(date_series) # or len(date_['series'][0]['data'])
        
        #print('end: ', end)
        date = []
        for i in range (endi):
            date.append(date_series[i][0])
				
        print(len(self.series))
        return date
'''       
        # Create dataframe
        df = pd.DataFrame(data=date)
        df.columns = ['Date']

        # Deal with data
        lenj = len(self.series)
'''
'''
         It looks like orig. developer used a pseudo head/tail to select first
         and last 30 lines of output. This should be adjusted to obtain
         full output for the dataframe that is returned
'''
'''
        for j in range (lenj):
            data_ = self.Raw(self.series[j])
            data_series = data_['series'][0]['data']
            data = []
            endk = len(date_series)         
            for k in range (endk):
                data.append(data_series[k][1])
            df[self.series[j]] = data
        
        return df
'''
if __name__ == '__main__':
    tok = '88465F906011215AB185A6E2A1D3994B'
        
    # Electricity - Monthly data
    '''
    test = ['ELEC.REV.AL-ALL.M', 'ELEC.REV.AK-ALL.M', 'ELEC.REV.CA-ALL.M']
    #test = ['PET.RWTC.D']
    data = EIAgov(tok, test)
    print(data.GetData())
    ''' 
    
    # Petroleum and products imports - quarterly data
    test2 = ['STEO.RNNIPUS.Q', 'STEO.PAIMPORT.Q', 'STEO.UONIPUS.Q']
    data = EIAgov(tok, test2)
    #data.GetData()
    print(data.GetData())

    '''
    # Petroleum and products supply - annual data
    test3 = ['STEO.DFPSPP1.A', 'STEO.DFPSPP2.A', 'STEO.DFPSPP3.A', 'STEO.DFPSPP4.A', 'STEO.DFPSPP5.A']
    data = EIAgov(tok, test3)
    print(data.GetData())
    '''
    ''' 
    # US ethanol output - weekly data
    test4 = ['PET.W_EPOOXE_YOP_NUS_MBBLD.W', 'PET.W_EPOOXE_YOP_R10_MBBLD.W', 'PET.W_EPOOXE_YOP_R20_MBBLD.W', 'PET.W_EPOOXE_YOP_R30_MBBLD.W', 'PET.W_EPOOXE_YOP_R40_MBBLD.W', 'PET.W_EPOOXE_YOP_R50_MBBLD.W']
    data = EIAgov(tok, test4)
    print(data.GetData())
    '''	
