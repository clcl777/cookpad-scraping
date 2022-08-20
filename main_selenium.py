import os
from selenium import webdriver
import requests,bs4
import urllib.request
import shutil
import time
import re
#本物

def first_prize_URL(driver):#一位URL取得
    first_prize_image = driver.find_element_by_class_name("js-ps_lead_thumbnail")
    return first_prize_image.get_attribute("data-image-url")

def processing_URL(url):#URL加工
    return re.search(r'\?+.+', url).group()

def get_page_number(driver):#ページ数取得
    page_element = driver.find_element_by_css_selector("#contents_holder > div.card_ui.search_result > div.center.paginate > span")
    number_slash = re.search(r'/\d+', page_element.text).group()#/222
    return int(number_slash.lstrip("/"))
    
url = 'https://cookpad.com/search/%E7%94%9F%E3%83%81%E3%83%A7%E3%82%B3'
options = webdriver.ChromeOptions()
options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C92 Safari/602.1')
#options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)
driver.get(url)
driver.maximize_window()
driver.implicitly_wait(10)
#1位の画像のURL取得
print("一位"+processing_URL(first_prize_URL(driver)))

#スクロール
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(1)
#elementsでサムネ画像を複数リストで取得
recipe_images = driver.find_elements_by_class_name("card_image")
bool_search_first = True
page = 1
#for image_url in recipe_images:#31回のみfor回す
while bool_search_first:
    for i,image_url in enumerate(recipe_images,1):
        if i>31:
            break
        try:
            img_tag = image_url.find_element_by_tag_name("img")
            print(processing_URL(img_tag.get_attribute("src")))
            if(processing_URL(img_tag.get_attribute("src")) == processing_URL(first_prize_URL(driver))):
                print('一位発見')
                img_tag.click()
                bool_search_first = False
                break
        except:
            print('タグなし')
    if not bool_search_first:
        break
    #次のページ移行
    if page==1:
        next_page_element = driver.find_element_by_css_selector("#contents_holder > div.card_ui.search_result > div.center.paginate > a")
        next_page_element.click()
    else:
        next_page_element = driver.find_element_by_css_selector("#contents_holder > div.card_ui.search_result > div.center.paginate > a:nth-child(3)")
        next_page_element.click()
    print("次のページへ" + str(page))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #time.sleep(1)
    recipe_images = driver.find_elements_by_class_name("card_image")
    page = page + 1

time.sleep(300)
print("終了")
