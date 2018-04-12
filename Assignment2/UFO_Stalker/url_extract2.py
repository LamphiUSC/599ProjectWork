# -*- coding: utf-8 -*-
import re
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementNotVisibleException
)

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

url = 'http://www.ufostalker.com/tag/photo'

def init_driver():
    driver = webdriver.Chrome('/Users/d3admin/Desktop/BigData/599ProjectWork/Assignment2/chromedriver')
    driver.wait = WebDriverWait(driver, 5)
    return driver
driver = init_driver()
driver.get(url)

f = open('urls_images3.txt', 'a',0)
for i in range(40000,60000):
    try:
        url = "http://www.ufostalker.com/event/"+str(i)
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, 'event-detail-title')))
        matches = re.findall(r'(?:http\:|https\:)?\/\/www\.mufoncms\.com.*\.(?:png|jpg|jpeg)', driver.page_source, re.IGNORECASE)
        if len(matches) > 0:
            for match in matches:
                f.write(match+"\n")
                f.flush()
                os.fsync(f)
    except:
        print i






        
    