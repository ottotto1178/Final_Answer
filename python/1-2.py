from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import re
import time

url = 'https://r.gnavi.co.jp/area/kagawa/rs/?fw='
driver_path = './chromedriver.exe'
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
options = webdriver.ChromeOptions()
options.add_argument(UA)
options.add_experimental_option("excludeSwitches", ['enable-automation'])

service = Service(executable_path = driver_path)
driver = webdriver.Chrome(chrome_options = options, service = service)

restaurant_name = [] #店舗名のデータを保存するリスト
links = [] #各店舗のURLを保存するリスト
phone_numbers = [] #電話番号を保存するリスト
mail_addresses = [] #メールアドレスを保存するリスト
dwellings = [] #番地までの住所を保存するリスト
prefectures =[] #都道府県を保存するリスト
municipalities = [] #市区町村を保存するリスト
addresses = [] #番地を保存するリスト
buildings = [] #建物の名前を保存するリスト
URLs = [] #店舗の公式ページのURLを保存するリスト
SSLs = [] #SSL証明書の有無を保存するリスト

#ブラウザを開く
driver.get(url)

# 50件データが集まるまで繰り返す
while restaurant_name_str != 50:
  # PR以外の各店舗のページにアクセスする
  driver.implicitly_wait(3) #待機時間
  restaurant_name_tags = driver.find_elements(By.CLASS_NAME, 'style_restaurantNameWrap__wvXSR')
  for x in range(len(restaurant_name_tags)):
    if len(restaurant_name) == 50: #データが50件集まればループ処理を終了させる
      break
    elif 'PR' in restaurant_name_tags[x].text: #PRの店舗を除外する
      continue
    elif restaurant_name_tags[x].text in restaurant_name:
      continue
    else:
      restaurant_name_.append(restaurant_name_tags[x].text) #「店舗名」を取得する
      
  # 「電話番号」「メールアドレス」「住所」「建物名」を取得する

  # 「お店のホームページ」があればアクセスし、そのサイトのURLを取得する

  # 取得したURLのSSL証明書の有無を確認する

  # ページ全てにアクセスしたら「>」ボタンをクリックしてページ遷移を行う

#ブラウザを閉じる
test = driver.find_elements(By.CLASS_NAME, 'style_restaurantNameWrap__wvXSR')
test_list = []
for i in range(len(test)):
  if 'PR' in test[i].text:
    pass
  else:
    test_list.append(test[i].text)
print(test_list)
print(len(test_list))
driver.quit()