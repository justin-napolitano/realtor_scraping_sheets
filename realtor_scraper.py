 # -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import lxml.etree as etree
import xml.etree.ElementTree as ET
import json
import pandas as pd
import os
import time
import random
import math


#cwd = os.getcwd()

#direct= sep.join((cwd,'data.json'))


#'Accept-Encoding': 'identity']

#city_list = ['red-river','williamsburg','vaughn','lake-arthur','wagon-mound','eagle-nest','reserve','maxwell','willard','jemez-springs','roy','san-jon','elida','san-ysidro','corona','virden','des-moines','dora','floyd','grady','hope','causey','mosquero','encino','taos-ski-valley','house','folsom','grenville','kirtland','rio-communities']
#state = 'nm'



def scrape(df):
    pg_number = '/pg-'
    n_pages = 0
    sep = os.sep
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Accept-Encoding': 'identity'
    }
    


    for index, row in df.iterrows():
        city = row['city']
        state = row['state']
        url = row['realtor_url']
        direct = row['directory']

        

        url = url + pg_number
        real_url = url + str(1)
        print("requesting {}".format(real_url))
        response=requests.get(real_url,headers=headers)

        print("scraping {}".format(real_url))
        soup=BeautifulSoup(response.content,'lxml')

        print("parsing data")
        data = json.loads(soup.find('script', type='application/json').string)

        # "pageData": {"matching_rows": 2153,

        print(math.ceil(data['props']['pageProps']['pageData']['matching_rows'] / 20))
        max_it = math.ceil(data['props']['pageProps']['pageData']['matching_rows'] / 20)
        df.at[index,'searched'] = 1


        time.sleep(random.randint(45,60))

        for page in range(0,max_it):
            n_pages += 1
            suffix = '_'.join((str(page),'data.json'))
            output= sep.join((direct, suffix))

            #print(direct)
            #direct= sep.join((cwd,'data.json',str(n_pages)))
            real_url = url +str(page)
            #print(real_url)
            
            #response=requests.get(url,headers=headers)
            #soup=BeautifulSoup(response.content,'lxml')
            try:
                print("requesting {}".format(real_url))
                response=requests.get(real_url,headers=headers)

                print("scraping {}".format(real_url))
                soup=BeautifulSoup(response.content,'lxml')

                print("parsing data")
                data = json.loads(soup.find('script', type='application/json').string)

                
                data['state'] = state
                data['city'] = city

                
                try :
                    os.makedirs(direct)
                    print("made_direct at {}".format(direct))
                except: 
                    print('me no have to make direct at {}'.format(direct))
                    pass

                print("dumping_data to {}".format(output))
                with open(output, 'w') as outfile:
                    json.dump(data, outfile)

            except:
                print("no more to people to parse.. :(")
                continue
                

            
            time.sleep(random.randint(45,60))

        print('You scraped {} pages'.format(n_pages))


                

    