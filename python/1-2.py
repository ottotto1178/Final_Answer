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
contents_links = [] #各店舗のURLを保存するリスト
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
time.sleep(3)

# 50件データが集まるまで繰り返す
while len(restaurant_name) != 50:
  # PR以外の各店舗URLを取得する
  restaurant_name_tags = driver.find_elements(By.CLASS_NAME, 'style_restaurantNameWrap__wvXSR')
  contents = driver.find_elements(By.CLASS_NAME, 'style_titleLink__oiHVJ')
  for x in range(len(restaurant_name_tags)):
    if len(restaurant_name) == 50: #データが50件集まればループ処理を終了させる
      break
    elif 'PR' in restaurant_name_tags[x].text: #PRの店舗を除外する
      continue
    elif restaurant_name_tags[x].text in restaurant_name: #データの重複をなくす
      continue
    else:
      restaurant_name.append(restaurant_name_tags[x].text) #「店舗名」を取得する
      contents_url = contents[x].get_attribute('href')
      contents_links.append(contents_url)
      
  # ページ内の全てのURLを取得したら「>」ボタンをクリックしてページ遷移を行う    
  next_btn = driver.find_element(By.CLASS_NAME, 'style_nextIcon__M_Me_')
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #画面内にボタンを表示させる必要があるので一度画面を一番下までスクロールする
  next_btn.click()
  time.sleep(3)
      
# 各店舗のURLにアクセスし「電話番号」「メールアドレス」「住所」「建物名」を取得する
for x in range(len(contents_links)):
  url = contents_links[x]
  driver.get(url)
  time.sleep(3)
  confirmation_dwelling = driver.find_elements(By.CLASS_NAME, 'region')
  confirmation_building = driver.find_elements(By.CLASS_NAME, 'locality')
  confirmation_phone_number = driver.find_elements(By.CLASS_NAME, 'number')
  confirmation_mail_address = driver.find_elements(By.CLASS_NAME, 'mail') #50件検索してもメールアドレスが確認できなかったため仮のクラスで検索
  if len(confirmation_phone_number) >= 1:
    phone_number = driver.find_element(By.CLASS_NAME, 'number')
    phone_numbers.append(phone_number.text)
  else:
    phone_numbers.append('')
  if len(confirmation_mail_address) >= 1:
    mail_address = driver.find_element(By.CLASS_NAME, 'mail')
    mail_addresses.append(mail_address.text)
  else:
    mail_addresses.append('')
  if len(confirmation_dwelling) >= 1:
    dwelling = driver.find_element(By.CLASS_NAME, 'region')
    dwellings.append(dwelling.text)
  else:
    dwellings.append('')
  if len(confirmation_building) >=1:
    building = driver.find_element(By.CLASS_NAME, 'locality')
    buildings.append(building.text)
  else:
    buildings.append('')
  # 「お店のホームページ」があればアクセスし、そのサイトのURLを取得する
  confirmation_home_page = driver.find_elements(By.LINK_TEXT, 'お店のホームページ')
  if len(confirmation_home_page) >= 1:
    home_page_url = driver.find_element(By.LINK_TEXT, 'お店のホームページ')
    home_page_url.click()
    handle_array = driver.window_handles
    driver.switch_to.window(handle_array[-1])
    URL = driver.current_url
    URLs.append(URL)
  else:
    URLs.append('')
  # 取得したURLのSSL証明書の有無を確認する
  if len(confirmation_home_page) >= 1:
    if 'https:' in URL:
      SSLs.append('True')
    else:
      SSLs.append('False')
  else:
    SSLs.append('')

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
  '店舗名' : restaurant_name,
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
df.to_csv('1-2.csv', index = False, encoding = 'utf_8_sig')

#ブラウザを閉じる
driver.quit()