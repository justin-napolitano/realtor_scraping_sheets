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
n_pages = 0

cwd = os.getcwd()
sep = os.sep
direct= sep.join((cwd,'data.json'))

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
'Accept-Encoding': 'identity'
}
#'Accept-Encoding': 'identity']

city_list = ['red-river','williamsburg','vaughn','lake-arthur','wagon-mound','eagle-nest','reserve','maxwell','willard','jemez-springs','roy','san-jon','elida','san-ysidro','corona','virden','des-moines','dora','floyd','grady','hope','causey','mosquero','encino','taos-ski-valley','house','folsom','grenville','kirtland','rio-communities']
state = 'nm'
pg_number = '/pg-'


def scrape(dictionary):

    df =  dictionary['universal_vars']['dfs']['zip_df']

    for index, row in df.iterrows():
        print(row['c1'], row['c2'])

    