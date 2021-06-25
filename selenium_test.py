#selenium_test.py

from selenium import webdriver
import time
import os
from pprint import pprint

cwd = os.getcwd()
exec_path = os.sep.join([cwd,'chromedriver'])

def attempt_1():
    url = "https://www.realtor.ca/realtor-search-results#city=toronto&province=2&page=1&sort=11-A"
    #url = 'https://stackoverflow.com/questions/57941221/how-can-i-use-jquery-with-selenium-execute-script-method'
    driver = webdriver.Chrome(executable_path=exec_path)
    driver.get(url)

    driver.execute_script("""var jquery_script = document.createElement('script'); 
    jquery_script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js';
    // jquery_script.onload = function(){var $ = window.jQuery; $("h1").wrap("<i></i>");};
    jquery_script.onload = function(){
    var $ = window.jQuery; 
    $("h1").wrap("<i></i>");
    };""")

    header = driver.execute_script('return document.getElementById("realtorSearchResultsCardsCon")')
        #('return document.getElementsByTagName("head")[0];')

    pprint(header)

def attempt_2():
    url = "https://www.realtor.ca/realtor-search-results#city=toronto&province=2&page=1&sort=11-A"
    #url = 'https://stackoverflow.com/questions/57941221/how-can-i-use-jquery-with-selenium-execute-script-method'
    driver = webdriver.Chrome(executable_path=exec_path)
    driver.get(url)
    with open('jquery_script.js', errors='ignore') as f:
        driver.execute_script(f.read())

    time.sleep(20)

    title = driver.execute_script('return document.getElementById("realtorSearchResultsCardsCon").text()') 
    #driver.execute_script('document.getElementById("realtorSearchResultsCardsCon")')

    pprint(title)


def main():
    #attempt_1()
    attempt_2()


if __name__ == "__main__":
    main()