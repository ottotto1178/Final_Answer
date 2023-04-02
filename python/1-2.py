from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import re
import time

url = 'https://r.gnavi.co.jp/area/kagawa/rs/?fw='
driver_path = 'D:\./chromedriver.exe'
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
headers = {"User-Agent": UA}

service = Service(executable_path = driver_path)
driver = webdriver.Chrome(service = service)
time.sleep(3) #待機時間3秒

driver.get(url)

time.sleep(3)

driver.quit()