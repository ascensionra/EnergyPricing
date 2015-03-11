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
import numpy as np
import pandas as pd
import urllib.request as request
from urllib.error import URLError, HTTPError
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
            req = request.Request(url)
            opener = request.urlopen(req)
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
        ''' The pretty print stuff is added my jm for debugging
        pp = pprint.PrettyPrinter(indent=4)
        '''
        date_ = self.Raw(self.series[0])        
        '''
        pp.pprint(date_)
        '''
        date_series = date_['series'][0]['data']
        endi = len(date_series) # or len(date_['series'][0]['data'])
        
        #print('end: ', end)
        date = []
        for i in range (endi):
            date.append(date_series[i][0])
				
        print(len(self.series))
       
        # Create dataframe
        df = pd.DataFrame(data=date)
        df.columns = ['Date']

        # Deal with data
        lenj = len(self.series)
        '''
         It looks like orig. developer used a pseudo head/tail to select first
         and last 30 lines of output. This should be adjusted to obtain
         full output for the dataframe that is returned
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

'''
       Date  ELEC.REV.AL-ALL.M  ELEC.REV.AK-ALL.M  ELEC.REV.CA-ALL.M
0    201409          768.38243           85.39040         4382.98624
1    201408          845.41194           88.35568         4321.97016
2    201407          829.54090           87.87466         4298.27509
3    201406          771.53590           84.78390         3560.25599
4    201405          645.25141           82.67122         2924.61747
5    201404          565.47932           85.64616         2283.75604
6    201403          641.26391           95.76815         2631.05805
7    201402          674.38022           92.96301         2602.03367
8    201401          791.93844          102.67423         2961.14948
9    201312          640.74098          102.63338         2878.61142
10   201311          569.24480           89.49363         2757.20088
11   201310          620.95865           82.72987         3185.77307
12   201309          749.96442           78.99774         3833.54450
13   201308          810.24360           81.35035         3907.07690
14   201307          787.77647           81.83453         4011.39757
15   201306          762.42801           77.09781         3495.79800
16   201305          607.76310           83.38545         2962.40773
17   201304          556.90272           87.18785         2503.64479
18   201303          611.10131           87.83714         2534.17011
19   201302          592.27963           85.28287         2504.46498
20   201301          642.97590           96.33537         2860.74324
21   201212          614.14860           99.77026         2577.17282
22   201211          566.07978           88.40511         2579.50180
23   201210          587.32712           83.66631         3164.14270
24   201209          715.94238           75.94608         3741.10571
25   201208          818.79811           83.50051         3987.48538
26   201207          855.94466           84.38226         3327.47889
27   201206          753.96455           76.07302         3230.37075
28   201205          644.64605           80.57236         2651.59039
29   201204          564.86306           81.83258         2344.55653
..      ...                ...                ...                ...
135  200306          434.25681           43.28150         2616.01006
136  200305          379.39696           44.23752         2218.85904
137  200304          355.90524           45.90003         2110.35462
138  200303          346.94927           47.70462         1954.89460
139  200302          380.12149           49.53765         2016.56982
140  200301          429.20504           54.78497         2301.66145
141  200212          368.26502           49.88714         2270.58793
142  200211          324.98902           47.99188         2050.95951
143  200210          385.25597           46.61964         2656.48010
144  200209          451.65138           45.36055         2581.62523
145  200208          504.51901           45.10194         2949.21135
146  200207          499.41289           44.17369         3075.21646
147  200206          425.82205           44.41843         2490.30552
148  200205          381.72727           46.46741         2254.43229
149  200204          341.96654           48.15025         2046.59426
150  200203          353.36232           49.74444         2069.15611
151  200202          317.68993           50.28615         1986.05551
152  200201          389.88061           53.66949         2249.41873
153  200112          321.72856           57.30742         2209.70314
154  200111          313.09223           51.93896         2116.90572
155  200110          328.63523           48.96076         2752.25922
156  200109          395.18199           44.04725         2704.73577
157  200108          457.32416           45.55710         3120.03468
158  200107          452.58496           43.74995         2900.29901
159  200106          398.57839           43.83628         2404.00318
160  200105          359.09236           43.88737         1949.72255
161  200104          347.18634           46.82643         1862.13954
162  200103          345.77802           48.43955         2111.17634
163  200102          321.06715           48.19988         1762.30306
164  200101          407.61261           51.96404         1893.25678

[165 rows x 4 columns]
'''
