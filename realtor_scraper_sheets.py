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
import df_filter as df_f
from pprint import pprint
import load_vars as lv
import google_drive as drive

#cwd = os.getcwd()

#direct= sep.join((cwd,'data.json'))


#'Accept-Encoding': 'identity']

#city_list = ['red-river','williamsburg','vaughn','lake-arthur','wagon-mound','eagle-nest','reserve','maxwell','willard','jemez-springs','roy','san-jon','elida','san-ysidro','corona','virden','des-moines','dora','floyd','grady','hope','causey','mosquero','encino','taos-ski-valley','house','folsom','grenville','kirtland','rio-communities']
#state = 'nm'





def scrape(df,sheets_service,drive_service, folder_id):
    state_dict = {}
    pg_number = '/pg-'
    n_pages = 0
    sep = os.sep
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Accept-Encoding': 'identity'
    }
    
    requests_per_100 = 100
    spreadsheet_id = ''
    seen_columns = {}
    num_columns = 0
    num_rows = 2
    start = 2
    sheet_dict = {}


    #lists of collumns and keys to drop from memory
    pop_list=[
        'office',
        'mls',
        'served_areas',
        'user_languages',
        'zips',
        'marketing_area_cities',
        'languages',
        'designations',
        'advertiser_id',
        'agent_rating',
        'description',
        'first_month',
        'first_year',
        'has_photo',
        'id',
        'is_realtor',
        'nar_only',
        'nrds_id',
        'party_id',
        'photo',
        'last_updated',
        'settings',
        'recommendations_count',
        'review_count',
        'lang',
        'raw_products',
        'data_flags',
        'product_code',
        'products',
        'video',
        'role',
        'slogan',
        'specializations',
        'types',
        'recently_sold',
        'broker',
        'agent_team_details',
        'agent_type',
        'areas_of_business',
        'mls_history',
        'phones']

    drop_list = [
        'office.mls',
        'office.photo.href',
        'background_photo.href',
        'office.video',
        'office.slogan',
        'office.fulfillment_id',
        'office.nrds_id',
        'office.party_id',
        'office.phones']
    #for teach riow in the cities df start a search on realtor.com
    for index, row in df.iterrows():
        #city = row['city']
        state = row['state']
        url = row['url']
        url = url + pg_number
        real_url = url + str(1)
        
        if state in state_dict.keys():
            pprint("state already in the dict bitch")
            spreadsheet_id = state_dict['state']

        else:
            pprint("creating Spreadsheet for {}".format(state))
            spreadsheet= drive.add_spreadsheet_to_folder(drive_service,folder_id,state)
            spreadsheet_id = (spreadsheet['id'])
            #spreadsheet_id = spreadsheet.get('spreadsheetId')
            #pprint(spreadsheet_id)
            state_dict[state] = spreadsheet_id



        try:

            print("requesting {}".format(real_url))
            response=requests.get(real_url,headers=headers)
        except:
            print('could not get a response from realtor.com')

        try:

            print("scraping {}".format(real_url))
            soup=BeautifulSoup(response.content,'lxml')

        except:
            print('beauty soup could not scrape parse the content')

        try:

            print("parsing data")
            data = json.loads(soup.find('script', type='application/json').string)
            #pprint(data['props']['pageProps']['pageData']['agents'])
        except:
            print('the website data could not be loaded to memory')

        max_it = math.ceil(data['props']['pageProps']['pageData']['matching_rows'] / 20)
        print(math.ceil(max_it))
        
        df.at[index,'searched'] = 1


        time.sleep(random.randint(45,60))
        #for every page in the data scrape it and append useful data
        for page in range(0,max_it):
            request_count = 0
            request_list = []
            n_pages += 1
            #print(direct)
            #direct= sep.join((cwd,'data.json',str(n_pages)))
            real_url = url +str(page)
            
            #print(real_url)
            try:

                print("requesting {}".format(real_url))
                response=requests.get(real_url,headers=headers)
            except:
                print('could not get a response from realtor.com')

            try:

                print("scraping {}".format(real_url))
                soup=BeautifulSoup(response.content,'lxml')

            except:
                print('beauty soup could not scrape parse the content')

            try:

                print("parsing data")
                data = json.loads(soup.find('script', type='application/json').string)
                #pprint(data['props']['pageProps']['pageData']['agents'])
            except:
                print('the website data could not be loaded to memory')
            

            #pops keys from the agent data 
            for agent in data['props']['pageProps']['pageData']['agents']:
                for key in pop_list:
                    try:
                        agent.pop(key)
                    except:
                        print('exception: {}'.format(key))
                        continue


            normalized = pd.json_normalize(data['props']['pageProps']['pageData']['agents'])
            #drops keys from the normalized data frame
            for key in drop_list:
                try:
                    normalized.drop(key, axis = 1, inplace =True)
                except:
                    print('....df exception: {}'.format(key))
                    continue

            pprint(normalized)
            #normalized.drop(labels = drop_list, axis = 1, inplace=True )
            columns = normalized.columns
            normalized.fillna(value="", inplace=True)
            pprint(columns.to_list())
            length = len(normalized.index)

            #append_blank_rows(spreadsheet_id,length, request_list)
            #iterates through columns.  Will append columns that are not in the dict and append the data to the request list.  at the end of each page it will update if necessary.
            for column in columns:
                if column not in seen_columns.values():
                    num_columns = num_columns + 1
                    column_key = lv.colnum_string(num_columns)
                    seen_columns[column_key] = column
                    rnge = "'Sheet1'" + "!" + column_key + str(1)
                    majorDimension = 'COLUMNS'
                    values = [[column]]

                    request_body_tmp = {
                        'range' : rnge,
                        'majorDimension' : majorDimension,
                        'values': values
                        }
                    request_list.append(request_body_tmp)
                    #body = {
                    #    "majorDimension": "COLUMNS",
                    #    "values": [[column]]
                    #}
                    #request = sheets_service.values().update(spreadsheetId=spreadsheet_id, range=rnge, valueInputOption="RAW", body=body)
                    #respie = request.execute()
                    #request_count = request_count + 1
                
                    #pprint(respie)
                    #time.sleep(10)

                else:
                    continue

            num_rows = num_rows + len(normalized)

            #an unnecessary function but i will not remove it yet.  Still need to clean this shit up
            for k,v in seen_columns.items():
                try:
                    d = normalized[v].tolist()
                    print(d)
                    rnge = "'Sheet1'" + "!" + k + str(start) + ":" + k + str(num_rows) 
                    print(rnge)
                    print(v)
                except: 
                    print('the key {} is not in the df'.format(k))

                for i in range(len(d)): 
                    if type(d[i]) is dict:
                        print("you have a dict")
                        string = ''
                        lst = d.values()
                        string = ','.join(lst)
                        index = string
                        pprint('joined the indexes in d..  Hopefull it looks like {}'.format(d))
                    elif type(d[i]) is list:
                        print("you have a list")
                        print(d[i])
                        for j in range(len(d[i])):
                            if type(d[i][j]) is dict:
                                normal = pd.json_normalize(d[i][j])
                                print(normal)
                                print('     you have a dict in the lst')
                                lst = d[i][j].values()
                                string = ','.join(lst)
                                d[i][j] = string
                        d[i] = ','.join(d[i])
                        print(d[i])

                                
                    else:
                        print('you have a {}'.format(type(index)))
                
    
                #print(d)
                #a tmp variable for the request ot be appended to the request list
                request_body_tmp = {
                    'range': rnge,
                    "majorDimension": "COLUMNS",
                    "values": [d]
                }
                #appends another instance to the request_list list
                request_list.append(request_body_tmp)
                #rnge = rnge    
                #valueInputOption="USER_ENTERED"
                #print(v)
                request_count = request_count + 1
            
            #creates the request body to use for batchupdate          
            request_body = {
                'valueInputOption': "RAW",
                'data' :[
                    request_list
                ]
            }

            
            #after each page send a request to google sheets to update the data sheets
            
            request = sheets_service.values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
            response = request.execute()
            pprint(response)
            pprint(seen_columns)
            print(num_rows)
            start = num_rows
            time.sleep(random.randint(45,60)) 

        print('You scraped {} pages'.format(n_pages))



def append_blank_rows(spreadsheet_id,length):
    request_body_tmp = {
        "appendDimension": 
        {
            "sheetId": spreadsheet_id,
            "dimension": "ROWS",
            "length": length

        }
    }
    

    return request_body_tmp


                

    
            
            
           # time.sleep(random.randint(45,60))

            