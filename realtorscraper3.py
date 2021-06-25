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
n_pages = 0

cwd = os.getcwd()
sep = os.sep
direct= sep.join((cwd,'data.json'))

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
'Accept-Encoding': 'identity'
}
#'Accept-Encoding': 'identity']

city_list = ['portland','salem','eugene','gresham','hillsboro','bevearton','bend','medford']
state = 'or'
pg_number = '/pg-'

# setting cities
for i in range(0,len(city_list)):
    city_list[i] = '_'.join((city_list[i],state))
    print(city_list[i])


for city in city_list:
    url = 'https://www.realtor.com/realestateagents/' + city + '/sort-activelistings' +pg_number

    for page in range(0,900):
        n_pages += 1
        suffix = '_'.join((str(page),city,'data.json'))
        direct= sep.join((cwd, suffix))
        #print(direct)
        #direct= sep.join((cwd,'data.json',str(n_pages)))
        real_url = url +str(page)
        print(real_url)
        
        #response=requests.get(url,headers=headers)
        #soup=BeautifulSoup(response.content,'lxml')
        try:
            print("requesting {}".format(real_url))
            response=requests.get(real_url,headers=headers)

            print("scraping {}".format(real_url))
            soup=BeautifulSoup(response.content,'lxml')

            print("parsing data")
            data = json.loads(soup.find('script', type='application/json').string)
            
            print("dumping_data to {}".format(direct))
            with open(direct, 'w') as outfile:
                json.dump(data, outfile)

        except:
            print("no more to people to parse.. :(")
            continue
            

        
        time.sleep(random.randint(45,60))

    print('You scraped {} pages'.format(n_pages))
        
        


    #url = 'https://www.realtor.com/realestateagents/phoenix_az/sort-activelistings/'

    #response=requests.get(url,headers=headers)

    #print(response.content)


    #x = etree.parse(response.content)
    #xtree = et.parse(response.content)
    #xroot = xtree.getroot()
    #root = ET.fromstring(response.content)
    #for child in root:
    #    print("a node:")
    ##    print(" ")
    #    print(" ")
    #    print(" ")
    #    print(child.tag, child.attrib)
        
    #print(etree.tostring(x, pretty_print=True))

    #print(soup.prettify())
    #data = json.loads(soup.find('script', type='application/json').string)
    #print(data)


    #with open(direct, 'w') as outfile:
    #    json.dump(data, outfile)


        

    #for item in soup.select('component_modalRoot'):
    #	try:
    #		print('**********')
    #		print(item)

    #	except Exception as e:
    #		#raise e
    #		print('error')

    #for item in soup:
    #    print('**********')
    #    print(item)


