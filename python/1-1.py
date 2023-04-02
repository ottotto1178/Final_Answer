import time
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
headers = {"User-Agent": UA}
url = 'https://r.gnavi.co.jp/area/kagawa/rs/'

i = 1
restaurant_name_str = [] #店舗名のデータを保存するリスト
links = [] #各店舗のURLを保存するリスト

while len(restaurant_name_str) != 50: #データを50件取得するまで繰り返す
  # if len(restaurant_name_str) == 50:
  #   break
  time.sleep(3) #待機時間3秒
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  restaurant_name_tags = soup.find_all('h2', class_='style_restaurantNameWrap__wvXSR')
  contents = soup.find_all('a', class_='style_titleLink__oiHVJ')
  for x in range(len(restaurant_name_tags)):
    if len(restaurant_name_str) == 50: #データを50件集まればループ処理を終了させる
      break
    elif restaurant_name_tags[x].string == None: #PRの店舗を除外する
      continue
    elif restaurant_name_tags[x] in restaurant_name_str: #データの重複をなくす
      continue
    else:
      restaurant_name_str.append(restaurant_name_tags[x].string)
      contents_url = contents[x].get('href')
      links.append(contents_url)
  i += 1
  url = urljoin(url, f'?p={i}') #次のページのurl
  
dwellings = [] #番地までの住所を保存するリスト
buildings = [] #建物の名前を保存するリスト
phone_numbers = [] #電話番号を保存するリスト
mail_addresses = [] #メールアドレスを保存するリスト
URLs = [] #店舗の公式ページのURLを保存するリスト
SSLs = [] #SSL証明書の有無を保存するリスト

for x in range(len(links)): #50回繰り返す
  restaurant_link = links[x]
  time.sleep(3)
  response = requests.get(restaurant_link)
  soup = BeautifulSoup(response.content, 'html.parser')
  dwelling = soup.find('span', class_='region')
  building = soup.find('span', class_='locality')
  phone_number = soup.find('span', class_='number')
  mail_address = soup.find('span', class_ = 'mail') #50件検索してもメールアドレスが確認できなかったため仮のクラスで検索
  URL = soup.find('a', class_='url go-off')
  dwellings.append(dwelling.text)
  if building != None:
    buildings.append(building.text)
  else:
    buildings.append('')
  if phone_number != None:
    phone_numbers.append(phone_number.text)
  else:
     phone_numbers.append('')
  if mail_address == None:
    mail_addresses.append('')
  else:
    mail_addresses.append(mail_address.text)
  # href属性が取得できる場合は以下のコードを用いる
  # if URL != None:
  #   home_page = URL.get('href')
  #   URLs.append(home_page)
  # else:
  #   URLs.append('')  
  # if 'https:' in home_page:
  #   SSLs.append('True')
  # else:
  #   SSLs.append('False')

  #href属性が#のため全てNoneとして扱う
  home_page = None
  URLs.append('')
  SSLs.append('')

prefectures =[] #都道府県を保存するリスト
municipalities = [] #市区町村を保存するリスト
addresses = [] #番地を保存するリスト
for x in range(len(dwellings)):
  prefecture = re.match('東京都|北海道|(?:京都|大阪)府|.{2,3}県' , dwellings[x]) # 都道府県名を分割する正規表現
  address = re.search('\d.*', dwellings[x]) #番地を分割する正規表現
  municipality = re.sub(prefecture.group(), '', dwellings[x]) #住所全体から都道府県名を削除
  municipality = re.sub(address.group(), '', municipality) #上記の住所から番地を削除(市区町村のみ抽出)
  prefectures.append(prefecture.group())
  municipalities.append(municipality)
  addresses.append(address.group())

#取得した各データをデータフレームに変換しやすいように辞書型データを作成
result = {
  '店舗名' : restaurant_name_str,
  '電話番号' : phone_numbers,
  'メールアドレス' : mail_addresses,
  '都道府県' : prefectures,
  '市区町村' : municipalities,
  '番地' : addresses,
  '建物名' : buildings,
  'URL' : URLs,
  'SSL' : SSLs
}

df = pd.DataFrame(result)
df.to_csv('1-1.csv', index = False, encoding = 'utf_8_sig')