
from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from pprint import pprint
import sys
from pprint import pprint
import strings as string
import datetime
import pandas as pd

def create_spreadsheet(title,service):

    title = title + str(datetime.datetime)
    

    spreadsheet_body = {'properties': {
        'title': '{}'.format(title),
        'parents': ['1EU57r3Le1w6FI-eIuGOucQitxKvsn51X?ths']
        }
    }

    request = service.create(body=spreadsheet_body)
    response = request.execute()    
    return(response)
    
    
def batch_download(spreadsheet_properties: dict,spread_service, header):
    
    #pprint(spreadsheet_properties)

    #for spreadsheet_key, spreadsheet_value in spreadsheet_properties.items():
    
    #print(spreadsheet_key)
    #pprint(spreadsheet_value)
    header = True
    
    spreadsheet_id = spreadsheet_properties['spreadsheetId']
    for sheet in spreadsheet_properties['sheets']:
        if header == True:
            df = pd.DataFrame(columns = [])
            header_range = sheet['properties']['ranges']['header']
            request_data = "spreadsheetId={}, range={}".format(spreadsheet_id,header_range)
            print("requestion {}".format(request_data))
            header_request = spread_service.values().get(spreadsheetId=spreadsheet_id, range=header_range)
            header_response= header_request.execute()
            pprint(header_response['values'][0])
            columns = header_response['values'][0]
            df = pd.DataFrame(columns = columns)
           #print(df)

        for i in range(len(sheet['properties']['ranges'])-1):
            rnge = sheet['properties']['ranges'][str(i)]
            request_data = "spreadsheetId={}, range={}".format(spreadsheet_id,rnge)
            print("requestion {}".format(request_data))
            request = spread_service.values().get(spreadsheetId=spreadsheet_id, range=rnge)
            response= request.execute()
            #pprint(response)
            data = response['values']
            pprint(data)
            tmp_df = pd.DataFrame(columns= columns,data=data)
            #pprint(tmp_df)
            #pd.concat(df,tmp_df)
            df = df.append(tmp_df,ignore_index=True)
            pprint(df)
    return df
            

        #   pprint(sheet['properties']['ranges'])
    #    for key,rnge in sheet['properties']['ranges'].items():
    #        request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=rnge)
    #        pprint(request)

    #spreasheet_list = []
    #spreadsheet_id = spreadsheet['spreadsheetID']
    #request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, ranges=A0:, valueRenderOption=value_render_option, dateTimeRenderOption=date_time_render_option)
    
    #print(end_column)
    #for data_sheet in spreadsheet_value['sheets']:
    #        pprint(data_sheet)
            

def get_sheet_service(creds):
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()

def confirm_sheet_ids(sheets_list,service):
    results =   {}

    SAMPLE_SPREADSHEET_ID = '1ILDcpuA1gn6mI3-7g8FPbA1MjXUXULI5hX8NC4Qbh64'
    SAMPLE_RANGE_NAME = 'virginia!A1:F'

    #service = build('sheets', 'v4', credentials=creds)

    
    # Call the Sheets API
    
    for k,v in sheets_list.items():
        if v is None:
            continue
            
        else: 
            try:
                print('trying: {}'.format(v))
                results[k] = service.get(spreadsheetId=v).execute()
            except:
                e = sys.exc_info()[0]
                print(e)
                break

    #pprint(results)
    return results



    

def download_search_criteria(service):

    range=SAMPLE_RANGE_NAME
    result = 'd'
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        pprint(result)
#        print('Name, Major:')
#        for row in values:
#            # Print columns A and E, which correspond to indices 0 and 4.
#            print('%s, %s' % (row[0], row[4]))