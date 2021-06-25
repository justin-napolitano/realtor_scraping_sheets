#rew_scraper.py


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
from pprint import pprint
import load_vars as lv
import html

def scrape(url,sheets_service,start,num_rows):
    #'https://www.rew.ca/agents/search/31353820'
    search_url = "https://www.rew.ca/"+ url
    spreadsheet_id = '1TBxlf0WNbAtC7j9fjS1MwQj_qcBtm0d_Hhq159V5Lro'
    #num_rows = 2
    #start = 2
    num_columns = 0
    seen_columns = {}
    request_list = []
    df = pd.DataFrame()
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Accept-Encoding': 'identity'
    }
    real_url =  search_url
    print("requesting {}".format(real_url))
    response=requests.get(real_url,headers=headers)

    #print('could not get a response from realtor.com')



    print("scraping {}".format(real_url))
    soup=BeautifulSoup(response.content,'lxml')
    soup_html = BeautifulSoup(response.content,'html.parser')
    #pprint(soup)


    #print('beauty soup could not scrape parse the content')



    print("parsing data")
    #result = soup.find_all('div', class_='agenttile')
    #data= soup.find_all('a')
    #pprint(result)
   #attrs={'data-bin' : True}
    #result_2 = soup_html.find_all(attrs={"data-agent": True})
    #[print(item['data-agent']) for item in soup_html.find_all(attrs={'data-agent' : True})]
    #normalized = pd.json_normalize(item)
    for item in soup_html.find_all(attrs={'data-agent' : True}):
        normalized = pd.json_normalize(item.attrs)
        df = df.append(normalized)
        #pprint(df)
    
    df.drop('class', axis = 1, inplace =True)
    df.set_index('data-agent',drop = False, inplace = True)


    email,social,website = about_test(df['data-profile'])
    listings = listings_test(df['data-profile'])
    df['email'] = df['data-agent'].map(email)
    df['social'] = df['data-agent'].map(social)
    df['website'] = df['data-agent'].map(website)
    df['no_listings'] = df['data-agent'].map(listings)

    df.fillna(value="", inplace=True)
    columns = df.columns

    
    #pprint(columns)
    num_rows = num_rows + len(df)
    

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


    for k,v in seen_columns.items():
        try:
            d = df[v].tolist()
            print(d)
            rnge = "'Sheet1'" + "!" + k + str(start) + ":" + k + str(num_rows) 
            print(rnge)
            print(v)
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
        #request_count = request_count + 1
        except: 
            print('the key {} is not in the df'.format(k))
            continue

    



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

    #pprint(seen_columns)
    #pprint(request_list)
    start= num_rows

    
    
    paginator_next= soup_html.find("li", class_="paginator-next_page paginator-control")
    href = paginator_next.find(attrs={'href' : True})
    if href is not None:
        nxt = href['href']
        scrape(nxt,sheets_service,start,num_rows)
    else:
        print("Done Scraping")


    #pprint(len(paginator))
    


    
    #pprint(df.columns)
    #result_3 = soup_html.find_all(data-foo="value")
    #pprint(result_2)
    #for tile in result:
    #    for email_tile in soup.find_all('div', class_ ="agentprofile-email"):
    #        for a in soup.find_all('a', class_ ='agenttile-action_btn btn btn-info btn-block'):
    #            pprint(a.find('data-agent'))
        #a in soup.find_all('a', href=True):
                #   pprint(a)
    #data = soup.find_all('script')
    #pprint(data)

    #print('the website data could not be loaded to memory')


def get_social(soup):
    #for icon in soup.select('a.socialicon'):
    #<li class="linkundecorated">
    social_list = []
    result = soup.find_all("li", {"class": "linkundecorated"})
    if result is not None:
        for li in result:
            for a in li.select('a'):
                social_list.append(a.attrs['href'])
                #pprint(a.attrs['href'])
        social_str = ','.join(social_list)
    else:
        social_str = ""
    #pprint(social_str)
    return social_str


    #pprint(soup)


def decode(cfemail):
    enc = bytes.fromhex(cfemail)
    return bytes([c ^ enc[0] for c in enc[1:]]).decode('utf8')


def get_email2(soup):
    #soup.find_all("div", {"class": "stylelistrow"})
    result = soup.find('ul',{'class', 'brandedagentprofile-list margin--txs'})
    
    if result is not None:
        result = result.find(attrs={'data-cfemail' : True})
        decrypted = cfDecodeEmail(result.attrs['data-cfemail'])
    else:
        decrypted = ""
    return decrypted

def get_no_listings(soup):
    results = soup.find("div", {"class": "paginationtext-light text-left hidden-xs"})
    if results is not None:
        results = results.text
        return results
    else:
        results = ""
    #for li in soup.find_all("li", {"class": "linkundecorated"}):
    #pprint(results)
    return results

def get_website(soup):
    #result = soup.find_all(attrs={'target' : 'blank'})
    #pprint(result)
    result = soup.find("ul", {"class": "brandedagentprofile-list margin--txs"})
    if result is not None:
        pprint(result)
        result = result.find(attrs={'target' : 'blank'})
        if result is not None:
            result = result.attrs['href']
            #pprint(result)
            #print(li)
        else:
            result = ""
    else:
        result = ""
    return result
    

def get_email(soup):
    for encrypted_email in soup.select('a.__cf_email__'):
        #pprint(encrypted_email)
        decrypted = cfDecodeEmail(encrypted_email['data-cfemail'])
        #pprint(decrypted)
        return decrypted
        # remove the <script> tag from the tree
        #script_tag = encrypted_email.find_next_sibling('script')
        #pprint(script_tag)
        #script_tag.decompose()
        # replace the <a class="__cf_email__"> tag with the decoded result
        #encrypted_email.replace_with(decrypted)


def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email


def listings_test(agent_column):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Accept-Encoding': 'identity'
    }
    listings_dictionary = {}
    lsting = "/my-listings"
    for k,v in agent_column.to_dict().items():
        time.sleep(random.randint(5,15)) 
        print(k,v)
        search_url = "https://www.rew.ca"+ v + lsting
        
        print("requesting {}".format(search_url))
        response=requests.get(search_url,headers=headers)

        print("scraping {}".format(search_url))
        soup=BeautifulSoup(response.content,'lxml')

        listings_dictionary[k] = get_no_listings(soup)

    return listings_dictionary



def about_test(agent_column):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Accept-Encoding': 'identity'
    }
    #pprint(agent_column)
    email_dictionary = {}
    social_dictionary = {}
    website_dictionary = {}
    about = '/about_me'
    #soup = search_url = "https://www.rew.ca"+ agent_data + about
    for k,v in agent_column.to_dict().items():
        time.sleep(random.randint(5,15)) 
        print(k,v)
        search_url = "https://www.rew.ca"+ v + about
        
        print("requesting {}".format(search_url))
        response=requests.get(search_url,headers=headers)

    #print('could not get a response from realtor.com')


        print("scraping {}".format(search_url))
        soup=BeautifulSoup(response.content,'lxml')
        #soup_html = BeautifulSoup(response.content,'html.parser')
        email_dictionary[k] = get_email2(soup)
        social_dictionary[k] = get_social(soup)
        website_dictionary[k] = get_website(soup)
    #pprint(email_dictionary)
    #pprint(social_dictionary)
    return (email_dictionary,social_dictionary,website_dictionary)
        
        
    


def about(agent_column):
    email_dictionary ={}
    agent_dictionary = {}
   
    agent_data = '/agents/91546/sam-kamra'

    #from the spread sheet get the agent code 
    #then go to the about page
    #then extract them email and website.  if there
    #if not move on

    #'https://www.rew.ca/agents/search/31353820'
    about = '/about_me'
    search_url = "https://www.rew.ca"+ agent_data + about
    spreadsheet_id = '1TBxlf0WNbAtC7j9fjS1MwQj_qcBtm0d_Hhq159V5Lro'
    #num_rows = 2
    #start = 2
    num_columns = 0
    seen_columns = {}
    request_list = []
    df = pd.DataFrame()
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Accept-Encoding': 'identity'
    }
    real_url =  search_url
    print("requesting {}".format(real_url))
    response=requests.get(real_url,headers=headers)

    #print('could not get a response from realtor.com')



    print("scraping {}".format(real_url))
    soup=BeautifulSoup(response.content,'lxml')
    soup_html = BeautifulSoup(response.content,'html.parser')
    email = get_email(soup)
    social = get_social(soup)



def main():
    scrape()

if __name__ == "__main__":
    main()