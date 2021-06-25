#rew_scraper_about.py


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
def scrape(agent_data):
    #<a href="/cdn-cgi/l/email-protection#a2d1c3cfc9c3cfd0c3e2dbc3cacdcd8cc1cdcf"><span class="__cf_email__" data-cfemail="c2b1a3afa9a3afb0a382bba3aaadadeca1adaf">[email protected]</span></a>
    #<a href="/cdn-cgi/l/email-protection#62060711080310060b0c111007030e161b22050f030b0e4c010d0f"><span class="__cf_email__" data-cfemail="0a6e6f79606b786e636479786f6b667e734a6d676b636624696567">[email protected]</span></a>
    agent_data ="/agents/148578/ryan-allary"
    #"/agents/91546/sam-kamra"
     #'/agents/91126/danielle-desjardins'
    #"/agents/91546/sam-kamra"
    

    #from the spread sheet get the agent code 
    #then go to the about page
    #then extract them email and website.  if there
    #if not move on

    #'https://www.rew.ca/agents/search/31353820'
    about = '/about_me'
    base_url = "https://www.rew.ca"+ agent_data 
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
    #soup_html = BeautifulSoup(response.content,'html.parser')
    email = get_email3(soup)
    listings = get_no_listings(base_url,headers)
    social = get_social(soup)
    website = get_website(soup)
    pprint(email)
    pprint(social)
    pprint(website)
    pprint(listings)

def get_no_listings(base_url,headers):
    url = base_url + "/my-listings"
    print(url)
    response=requests.get(url,headers=headers)
    #print(response)
    soup=BeautifulSoup(response.content,'lxml')
    #soup = BeautifulSoup(response,content,'lxml')
    #pprint(soup)
    #results = soup.find('class',{"href", url})
    #https://www.rew.ca/agents/119923/john-dalimonte/my-listings#agentNavigation
    results = soup.find("div", {"class": "paginationtext-light text-left hidden-xs"})
    if results is not None:
        results = soup.find("div", {"class": "paginationtext-light text-left hidden-xs"}).text
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
        result = result.find(attrs={'target' : 'blank'}).attrs['href']
            #pprint(result)
            #print(li)
    else:
        result = ""
    return result


def get_social(soup):
    #for icon in soup.select('a.socialicon'):
    #<li class="linkundecorated">
    social_list = []
    result = soup.find_all("li", {"class": "linkundecorated"})
    if result is not None:
        for li in soup.find_all("li", {"class": "linkundecorated"}):
            for a in li.select('a'):
                social_list.append(a.attrs['href'])
                #pprint(a.attrs['href'])
        social_str = ','.join(social_list)
    else:
        social_str = ""
    #pprint(social_str)
    return social_str

def get_data(soup):
    
    print(cfDecodeEmail('384b59555359554a59784159505757165b5755'))
    #pprint(soup)


def decode(cfemail):
    enc = bytes.fromhex(cfemail)
    return bytes([c ^ enc[0] for c in enc[1:]]).decode('utf8')

def get_email3(soup):
    soup.find_all("div", {"class": "stylelistrow"})
    result = soup.find('ul',{'class', 'brandedagentprofile-list margin--txs'})
    
    if result is not None:
        result = result.find(attrs={'data-cfemail' : True})
        decrypted = cfDecodeEmail(result.attrs['data-cfemail'])
    else:
        decrypted = ""
    return decrypted
    #pprint(decrypted)


def get_email2(soup):
    soup.find_all("div", {"class": "stylelistrow"})
    result = soup.find('ul',{'class', 'brandedagentprofile-list margin--txs'})
    result = result.find(attrs={'data-cfemail' : True})
    decrypted = cfDecodeEmail(result.attrs['data-cfemail'])
    #pprint(decrypted)
    return(decrypted)

def get_email(soup):
    print('eamil testing')
    #data-cfemail
    result_list = []
    results = soup.find_all(attrs={'data-cfemail' : True})
    for result in results:
        #pprint(result.attrs['data-cfemail'])
        decrypted = cfDecodeEmail(result.attrs['data-cfemail'])
        if decrypted == 'support@rew.ca':
            continue
        elif decrypted is None:
            continue
        else:
            result_list.append(decrypted)
    return result_list
    
    #return decrypted
    #pprint(soup)
    for encrypted_email in soup.select('a.__cf_email__'):
        pprint(encrypted_email)
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

 


    #print('beauty soup could not scrape parse the content')



    #print("parsing data")
    #result = soup.find_all('div', class_='agenttile')
    #data= soup.find_all('a')
    #pprint(result)
   #attrs={'data-bin' : True}
    #result_2 = soup_html.find_all(attrs={"data-agent": True})
    #[print(item['data-agent']) for item in soup_html.find_all(attrs={'data-agent' : True})]

def main():
    scrape('K')
    
if __name__ == "__main__":
    main()