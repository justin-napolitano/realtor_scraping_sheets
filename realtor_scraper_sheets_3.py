 # -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
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
import requests




#def create_new_sheet():

#def share_spreadsheet




        


def scrape(df,sheets_service,drive_service, folder_id):
    import requests
    log_dict = {}
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
    #sheet_dict = {}

    pop_list= get_pop_list()

    drop_list = get_drop_list()

    
    #for teach riow in the cities df start a search on realtor.com
    for index, row in df.iterrows():

        #city = row['city']
        state = row['state']
        url = row['url']
        url = url + pg_number
        real_url = url + str(1)
        num_rows = 2
        start = 2
    
        
        #write a check state function.  pass spreadsheet id, num_rows, start, and state dict.. update pointer in place in memory

        #checked_state_dict = 
        #write this into a class.  I don't liek returning a tuple froma function. I feel stupid.  
        num_rows, start, spreadsheet_id= check_state_dict(drive_service,sheets_service,folder_id,state_dict, num_rows, start, spreadsheet_id,state)

   
        #write this into a class  called web_data.response/soup/data
        response = get_request(real_url,headers)
        soup = get_soup(real_url,response)
        #pprint(soup)
        data = get_web_data(soup)

        max_it = math.ceil(data['props']['pageProps']['pageData']['matching_rows'] / 20)
        print(max_it)
        
        #write update input_sheet_function here.  Will add searching, and pg_number to the input sheet
        #also use your functions below to just add this to the updates.   then start at page 2 below
        df.at[index,'searched'] = 1


        time.sleep(random.randint(45,60))
        #for every page in the data scrape it and append useful data
        for page in range(0,max_it):
            data_list = []
            requests_list = []
            request_count = 0
            #data_request_list = []
            n_pages += 1
            #print(direct)
            #direct= sep.join((cwd,'data.json',str(n_pages)))
            real_url = url +str(page)
            
            #print(real_url)

            #will write into a web_data class later
            response = get_request(real_url,headers)
            soup = get_soup(real_url,response)
            data = get_web_data(soup)
            

            #pops keys from the agent data 

            popped = pop(data,pop_list)
           
            normalized = pd.json_normalize(data['props']['pageProps']['pageData']['agents'])
            #drops keys from the normalized data frame

            dropped = drop(normalized, drop_list)
        

            #pprint(normalized)
            #normalized.drop(labels = drop_list, axis = 1, inplace=True )
            columns = normalized.columns
            normalized.fillna(value="", inplace=True)
            #pprint(columns.to_list())
            length = len(normalized.index)
            

            #iterates through columns.  Will append columns that are not in the dict and append the data to the request list.  at the end of each page it will update if necessary.
            num_columns = check_columns(columns,num_columns,seen_columns,spreadsheet_id,requests_list, data_list)
            
            
            num_rows = num_rows + len(normalized)

            #set num_rows searched in num_rows of state_dict
            state_dict['num_rows'] = num_rows

            #an unnecessary function but i will not remove it yet.  Still need to clean this shit up.  This is for post processing the normailze function
            #i found that it did not completely normalize some difficult hierarchies.  I will continue working on this in the upcoming days.  
            
            #create a new function called update collumn ranges
            for k,v in seen_columns.items():
                try:
                    d = normalized[v].tolist()
                    #print(d)
                    rnge = "'Sheet1'" + "!" + k + str(start) + ":" + k + str(num_rows) 
                    #print(rnge)
                    #print(v)
                except: 
                    print('the key {} is not in the df'.format(k))

         
                
    
                appended_data = append_to_data_list(rnge,d,data_list)
                request_count = request_count + 1
            
            #creates the request body to use for batchupdate          
            #call this create batchUpdate requests..
            appended_blank_rows = append_blank_rows(spreadsheet_id,length,requests_list)
            #appended_update_request = append_batch_update_request(spreadsheet_id,length,requests_list,data_list)
            sent_update_value_request = send_update_values_request(spreadsheet_id,data_list,sheets_service)
            sent_batch_update_request = send_batch_update_request(requests_list,spreadsheet_id,sheets_service)

            start = num_rows
            #pprint(requests_list)
            time.sleep(random.randint(45,60)) 
            

        print('You scraped {} pages'.format(n_pages))

def append_delete_duplicates_request(spreadsheet_id,requests_list,num_rows):
    {
    "range": {
        {
            "sheetId": 0,
            "startRowIndex": 0,
            "endRowIndex": num_rows,
            "startColumnIndex": integer,
            "endColumnIndex": integer
            }
        
        }
    }
   


def drop(normalized, drop_list):
    for key in drop_list:
        try:
            normalized.drop(key, axis = 1, inplace =True)
        except:
            print('....df exception: {}'.format(key))
            continue
    return True

def pop(data,pop_list):

    for agent in data['props']['pageProps']['pageData']['agents']:
        for key in pop_list:
            try:
                agent.pop(key)
            except:
                print('exception: {}'.format(key))
                continue
    return True

def get_soup(real_url,response):
    try:
        print("scraping {}".format(real_url))
        soup=BeautifulSoup(response.content,'lxml')

    except:
        print('beauty soup could not scrape parse the content')
    
    return soup
    
def get_web_data(soup):
    try:
        print("parsing data")
        data = json.loads(soup.find('script', type='application/json').string)
        #pprint(data['props']['pageProps']['pageData']['agents'])
    except:
        print('the website data could not be loaded to memory')

    return data

def get_request(real_url,headers):
    try:
        print("requesting {}".format(real_url))
        response = requests.get(real_url,headers=headers)
        #pprint(response)
    except:
        print('could not get a response from realtor.com')
    return response

def send_batch_update_request(requests,spreadsheet_id,sheets_service):
    body = {
    'requests': requests
    }
    pprint(body)
    response = sheets_service.batchUpdate(spreadsheetId=spreadsheet_id,body=body).execute()
    #pprint(response)
    #request = sheets_service.values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
    return True

def append_blank_rows(spreadsheet_id,length,requests_list): 
    request_body_tmp = {
        "appendDimension": 
        {
            "sheetId": 0,
            "dimension": "ROWS",
            "length": length

        }
    }

    requests_list.append(request_body_tmp)
    return True

def append_blank_columns(spreadsheet_id,length,requests_list): 
    request_body_tmp = {
        "appendDimension": 
        {
            "sheetId": 0,
            "dimension": "COLUMNS",
            "length": length

        }
    }

    requests_list.append(request_body_tmp)
    return True
    #data_request_list.append(request_body_tmp)

def append_columns_to_data_list(seen_columns,noramlized,data_list):
    for k,v in seen_columns.items():
        try:
            d = normalized[v].tolist()
            #print(d)
            rnge = "'Sheet1'" + "!" + k + str(start) + ":" + k + str(num_rows) 
            #print(rnge)
            #print(v)
        except: 
            print('the key {} is not in the df'.format(k))
    return True

def append_to_data_list(rnge,d,data_list):#rename to _data_list
    request_body_tmp = {
        'range': rnge,
        "majorDimension": "COLUMNS",
        "values": [d]
    }
    data_list.append(request_body_tmp)

def send_update_values_request(spreadsheet_id,data_list,sheets_service):
    request_body = {
        'valueInputOption': "RAW",
        'data' :[
            data_list
        ]
    }
    print("a;dkfj;adkfja;ldskjf;akdsjf;akdsjf;akjds;fkajsdf")
    pprint(request_body)
    
    request = sheets_service.values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
    response = request.execute()
    print("a;lkdjf;akljsd;fiajeif;alkdsn;aklsdjfp;oiadsupfadjs;lkansd;lkajs;dfkj")
    pprint(response)
    #requests_list.append(request_body)
    return True

def create_spreadsheet(title,sheets_service):
    spreadsheet = {
        'properties': {
            'title': title
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                    fields='spreadsheetId').execute()
    print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))
    return spreadsheet.get('spreadsheetId')

def get_drop_list():
    drop_list = [
        'office.mls',
        'office.photo.href',
        'background_photo.href',
        'office.video',
        'office.slogan',
        'office.fulfillment_id',
        'office.nrds_id',
        'office.party_id',
        'office.phones',
        'social_media.facebook'}]
    return drop_list

def get_pop_list():
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

    return pop_list

def check_state_dict(drive_service, sheets_service, folder_id, state_dict, num_rows, start, spreadsheet_id,state):
    # make this into a class... 
    #the class will return all of these value in a pythonic way.  Right now you are writing in c you cookoo bird

    if state in state_dict.keys():
        pprint("state already in the dict, asshole!")
        spreadsheet_id = state_dict[state]
        num_rows = state_dict['num_rows']
        start = num_rows

    else:
        pprint("creating Spreadsheet for {}".format(state))
        spreadsheet= drive.add_spreadsheet_to_folder(drive_service,folder_id,state)
        spreadsheet_id = spreadsheet['id']
        #spreadsheet_id = spreadsheet.get('spreadsheetId')
        #pprint(spreadsheet_id)
        state_dict[state] = spreadsheet_id
        num_rows = 2
        start = 2

    return num_rows, start, spreadsheet_id
    


                

    
            
            
           # time.sleep(random.randint(45,60))
#could probs rewrite this into a class that would also fix all of my problems.  Return the class with all of the important data.  Call it a day.  
def check_columns(columns,num_columns,seen_columns,spreadsheet_id, requests_list, data_list):

    for column in columns:
        if column not in seen_columns.values():
            num_columns = num_columns + 1
            column_key = lv.colnum_string(num_columns)
            seen_columns[column_key] = column
            rnge = "'Sheet1'" + "!" + column_key + str(1)
            majorDimension = 'COLUMNS'
            values = [column]
            appended_blank_columns = append_blank_columns(spreadsheet_id,1,requests_list)
            appended_data = append_to_data_list(rnge,values,data_list)
            pprint(seen_columns)


        else:
            continue       
    return num_columns