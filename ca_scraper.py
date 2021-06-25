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


def request():
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Accept-Encoding': 'identity'
    }

    real_url =  "https://www.realtor.ca/realtor-search-results#city=toronto&province=2&page=1&sort=11-A"
    print("requesting {}".format(real_url))
    response=requests.get(real_url,headers=headers)

    pprint(response.text)



    print("scraping {}".format(real_url))
    soup=BeautifulSoup(response.content,'lxml')
    soup_html = BeautifulSoup(response.content,'html.parser')
    #pprint(soup)
    data = soup.find_all("div", {"class": "realtorSearchResultCardCon"})
    #data = soup.find_all()
    print("start")
    #pprint("    {}".format(soup))
    pprint(data)
    

def main():
    request()


if __name__ == "__main__":
    main()
