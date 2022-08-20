import os
from selenium import webdriver
import requests
import urllib.request
import time
import re
from bs4 import BeautifulSoup
import lxml.html
from tkinter import *
from tkinter import ttk
import sys

def prize_URL(soup, n):  # 0が1位、1が2位、2が3位
    prize_images = soup.find_all('li', class_='js-ps_lead_thumbnail')
    return prize_images[n].get('data-image-url')

def processing_URL(url):  # 画像のURLの末尾を抽出
    return re.search(r'\?+.+', url).group()


def create_URL(url):  # 画像のURLからレシピのURLを作成する
    url2 = re.search(r'recipes/\d+', url).group()
    return "https://cookpad.com/recipe" + url2[7:]

def creat_next_page(url,page):#次のURLを作成する
    return url + "?order=date&page=" + str(page)

def creare_elements(url):#recipe_imagesをURLから作成する関数
    res = requests.get(url)
    # res.raise_for_status()
    soup_pc = BeautifulSoup(res.text, "lxml")
    recipe_images = soup_pc.find_all('div', class_='recipe-image wide')
    print(url)
    return recipe_images

#変更
def get_page_number(driver):  # ページ数取得
    page_element = driver.find_element_by_css_selector(
        "#contents_holder > div.card_ui.search_result > div.center.paginate > span")
    number_slash = re.search(r'/\d+', page_element.text).group()  # /222
    return int(number_slash.lstrip("/"))

#exe用
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def main():
    #フレーム作成
    root = Tk()
    root.title('クックパッド自動検索')
    frame1 = ttk.Frame(root, padding=16)
    label1 = ttk.Label(frame1, text='検索ワード')
    keyword_str_var = StringVar()
    entry1 = ttk.Entry(frame1, textvariable=keyword_str_var, width = 100)
    entry1.configure(font=("", 14, ""))
    frame2 = ttk.Frame(root, padding=16)
    button1 = ttk.Button(
        frame2,
        text='OK',
        command=lambda: root.destroy())
    frame1.pack(side=TOP, anchor=NW)
    frame2.pack(side=TOP, anchor=NW)
    label1.pack(fill=X)
    entry1.pack(fill=X)
    button1.pack(fill=X)
    # ウィンドウの表示開始
    root.mainloop()

    keyword = keyword_str_var.get()
    #url = 'https://cookpad.com/search/%E3%83%9E%E3%82%AB%E3%83%AD%E3%83%B3'
    url_cookpad = 'https://cookpad.com/'
    driver = webdriver.Chrome(resource_path('./driver/chromedriver.exe'))#exe仕様
    #driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(url_cookpad)
    search_element = driver.find_element_by_css_selector('#keyword')
    search_element.send_keys(keyword)
    enter_element = driver.find_element_by_css_selector('#submit_button')
    enter_element.click()
    url = driver.current_url
    driver.execute_script("window.open()")
    driver.execute_script("window.open()")

    #soup
    headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) > > AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            }
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, "lxml")

    # 1,2,3位の画像のURL取得
    print("1位" + processing_URL(prize_URL(soup, 0)))
    print("2位" + processing_URL(prize_URL(soup, 1)))
    print("3位" + processing_URL(prize_URL(soup, 2)))

    bool_search_first = True
    bool_search_second = True
    bool_search_third = True

    page = 1

    # for image_url in recipe_images:#31回のみfor回す
    while bool_search_first or bool_search_second or bool_search_third:
        print('次' + str(page) + 'ページへ')

        time.sleep(1)

        for i, image_url in enumerate(creare_elements(creat_next_page(url,page)), 1):
            if i > 12:
                break
            try:
                image_tag = image_url.find('a')
                image_tag2 = image_tag.find('img')
                print(str(i) + "番目" + processing_URL(image_tag2.get('src')))
                if (processing_URL(image_tag2.get('src')) == processing_URL(prize_URL(soup, 0))):
                    print('1位発見')
                    URL_1st = create_URL(image_tag2.get('src'))
                    #img_tag.click()
                    #1位のURLをseleniumで開く
                    bool_search_first = False
                    #1位のサイト開く
                    driver.switch_to.window(driver.window_handles[0])
                    driver.get(URL_1st)
                    # 他の順位も検索するため、breakいらない
                    #break

                if (processing_URL(image_tag2.get('src')) == processing_URL(prize_URL(soup, 1))):
                    print('2位発見')
                    URL_2nd = create_URL(image_tag2.get('src'))
                    #img_tag.click()
                    #2位のURLをseleniumで開く
                    bool_search_second = False
                    #2位のサイト開く
                    driver.switch_to.window(driver.window_handles[2])
                    driver.get(URL_2nd)

                if (processing_URL(image_tag2.get('src')) == processing_URL(prize_URL(soup, 2))):
                    print('3位発見')
                    URL_3rd = create_URL(image_tag2.get('src'))
                    bool_search_third = False
                    # 3位のサイト開く
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(URL_3rd)
            except:
                print('タグなし')
        #if not bool_search_first:
            #break
        # 次のページ移行
        page = page + 1

    time.sleep(3600)
    print("終了")

if __name__ == "__main__":
    main()
