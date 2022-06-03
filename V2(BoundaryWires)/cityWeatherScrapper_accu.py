# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

URL = "https://www.accuweather.com/en/us/andover/55304/minute-weather-forecast/2248193"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')


# checking the status code of the request
if response.status_code == 200:

   temperature = soup.find("span", {"class" : "current-temp"} ).text
   state = soup.find("p", {"class" : "icon-phrase"} ).text

   print(temperature)
   print(state)
   
'''
#Selenium version
import requests ,time
import bs4
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



options = webdriver.ChromeOptions()
# options.add_argument('headless')
driver = webdriver.Chrome(executable_path=r"C:\chromedriver.exe", options=options)
driver.maximize_window()



URL = "https://www.accuweather.com/en/us/andover/55304/minute-weather-forecast/2248193"

driver.get(URL)
time.sleep(2)
soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')


# checking the status code of the request
temperature = soup.find("span", {"class" : "current-temp"} ).text
state = soup.find("p", {"class" : "icon-phrase"} ).text

print(temperature)
print(state)
'''