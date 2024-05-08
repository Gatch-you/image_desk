import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import urllib
import csv
import time
import datetime
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By

from csv_database.database import Check_image_url
from download import Download_images

from bs4 import BeautifulSoup
import bs4

from selenium.webdriver.support.ui import WebDriverWait

# 検索条件
QUERY = '柴犬'
FILE_NAME = 'test_'
SAVE_DIR = '../data/downloads'
CSV_FILE_PATH = 'csv_database/test.csv'
LIMIT_DL_NUM = 5

TIMEOUT = 30
ACCESS_WAIT = 1
# selenium ver4.10.0では不要
# DRIVER_PATH = '/usr/bin/chromedriver'

# Driverの設定
options = Options()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-fullscreen')
options.add_argument('--disable-plugins')
options.add_argument('--disable-extensions')

if __name__ == "__main__":
    # Driver のタイムスタンプ
    tm_start = time.time()
    dt_now = datetime.datetime.now()
    dt_date_str = dt_now.strftime('%Y/%m/%d %H:%M')
    print(dt_date_str)

    # ドライバーの起動
    driver=webdriver.Chrome(options=options)   ##selenium 4.10.0ver
    wait = WebDriverWait(driver, TIMEOUT)

    tm_driver = time.time()
    print('WebDriver起動完了', f'{tm_driver - tm_start:.1f}s')

    BASE_URL = f'https://www.google.com/search?q={QUERY}&tbm=isch'
    driver.get(BASE_URL)

    tm_getsource = time.time()
    print('Google画像検索ページ取得', f'{tm_getsource - tm_driver:.1f}s')

    with open(CSV_FILE_PATH, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data_size = sum(1 for row in reader)
        print("現在のデータセットのサイズ:::", data_size)
    img_urls = []
    count: int = 0
    while len(img_urls) < LIMIT_DL_NUM:
        time.sleep(1)
        push_element = driver.find_elements(By.CSS_SELECTOR, "h3.ob5Hkd")
        push_element[count].click()
        time.sleep(2)

        # jsactionによるポップモーダルのhtml
        try:
            # print(count)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.sFlh5c.pT0Scc.iPVvYb")))
            new_html = driver.find_element(By.CSS_SELECTOR, "img.sFlh5c.pT0Scc.iPVvYb")

            img_url = new_html.get_attribute('src')

            checked_url = Check_image_url(img_url, CSV_FILE_PATH)
            if checked_url:
                print("new elements is this:::", checked_url)
                img_urls.append(checked_url)
                time.sleep(1)
                count += 1
            else:
                count += 1
                pass
            driver.back()
        except:
            count += 1
            continue

    driver.quit()
    print(img_urls)
    img_count = Download_images(img_urls, SAVE_DIR, FILE_NAME, data_size)
    print("----------ダウンロード完了", img_count, "枚の画像をダウンロードしました----------")



# # ここが通らない
# tmb_elems = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#islmp img')))
# tmb_alts = [tmb.get_attribute('alt') for tmb in tmb_elems]

# count = len(tmb_alts) - tmb_alts.count('')
# print(count)

# while count < LIMIT_DL_NUM:
#     driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
#     time.sleep(1)

#     tmb_elems = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#islmp img')))
#     tmb_alts = [tmb.get_attribute('alt') for tmb in tmb_elems]

#     count = len(tmb_alts) - tmb_alts.count('')
#     print(count)

# imgframe_elem = wait.until(EC.presence_of_element_located((By.ID, 'islsp')))

# os.makedirs(SAVE_DIR, exist_ok=True)
# HTTP_HEADERS = {'User-Agent': driver.execute_script('return navigator.userAgent;')}
# print(HTTP_HEADERS)

# IMG_EXTS = ('.jpg', '.jpeg', '.png', '.gif')

# def get_extension(url):
#     url_lower = url.lower()
#     for img_ext in IMG_EXTS:
#         if img_ext in url_lower:
#             extension = '.jpg' if img_ext == '.jpeg' else img_ext
#             break
#     else:
#         extension = ''
#     return extension

# def download_image(url, path, loop):
#     result = False
#     for i in range(loop):
#         try:
#             r = requests.get(url, headers=HTTP_HEADERS, stream=True, timeout=10)
#             r.raise_for_status()
#             with open(path, 'wb') as f:
#                 f.write(r.content)

#         except requests.exceptions.SSLError:
#             print('***** SSL エラー')
#             break
#         except requests.exceptions.RequestException as e:
#             print(f'***** requests エラー({e}): {i + 1}/{RETRY_NUM}')
#             time.sleep(1)
#         else:
#             result = True
#             break
#     return result

# tm_thumbnails = time.time()
# print('サムネイル画像取得', f'{tm_thumbnails - tm_geturl:.1f}s')

# EXCLUSION_URL = 'https://lh3.googleusercontent.com/'
# count = 0
# url_list = []
# for tmb_elem, tmb_alt in zip(tmb_elems, tmb_alts):

#     if tmb_alt == '':
#         continue

#     print(f'{count}: {tmb_alt}')

#     for _ in range(RETRY_NUM):
#         try:
#             tmb_elem.click()
#             break
#         except (ElementClickInterceptedException, StaleElementReferenceException):
#             driver.execute_script('arguments[0].scrollIntoView(true);', tmb_elem)
#             time.sleep(1)

#     time.sleep(ACCESS_WAIT)

#     alt = tmb_alt.replace("'", "\\'")
#     try:
#         img_elem = imgframe_elem.find_element(By.CSS_SELECTOR, f'img[alt=\'{alt}\']')

#     except NoSuchElementException:
#         print('***** img要素検索エラー')
#         print('***** キャンセル')
#         continue

#     tmb_url = tmb_elem.get_attribute('src')
#     for _ in range(RETRY_NUM):
#         url = img_elem.get_attribute('src')
#         if EXCLUSION_URL in url or url == tmb_url:
#             time.sleep(1)
#             continue
#         break

#     if not url:
#         print('***** キャンセル')
#         continue

#     ext = get_extension(url)
#     if not ext:
#         print(f'***** urlに拡張子が含まれていないのでキャンセル')
#         print(f'{url}')
#         continue

#     filename = f'{FILE_NAME}{count}{ext}'
#     path = os.path.join(SAVE_DIR, filename)
#     if download_image(url, path, RETRY_NUM):
#         url_list.append(f'{filename}: {url}')
#         count += 1
#     else:
#         print('***** キャンセル')

#     if count >= LIMIT_DL_NUM:
#         break

# tm_end = time.time()
# print('ダウンロード', f'{tm_end - tm_thumbnails:.1f}s')
# print('------------------------------------')
# total = tm_end - tm_start
# total_str = f'トータル時間: {total:.1f}s({total/60:.2f}min)'
# count_str = f'ダウンロード数: {count}'
# print(total_str)
# print(count_str)

# path = os.path.join(SAVE_DIR, 'url', '_url.txt')
# with open(path, 'w', encoding='utf-8') as f:
#     f.write(dt_date_str + '\n')
#     f.write(total_str + '\n')
#     f.write(count_str + '\n')
#     f.write('\n'.join(url_list))

# driver.quit()
