#download.py
from urllib.request import Request, urlopen 
import requests  

def download_pdf(df):
    #print(df)
    for pdf in df['pdf']:
        print(pdf)
    #url="https://realpython.com/python-tricks-sample-pdf"  
    
    #req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})  
    #r = requests.get(url)

    #with open("<location to dump pdf>/<name of file>.pdf", "wb") as code:
    #    code.write(r.content)
