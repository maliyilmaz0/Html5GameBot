import time
import  random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import mariadb
import sys
import requests
import base64
import json
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts,NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
import collections.abc as collections
import mariadb
import sys

"""# root_div içerisindeki most-thumbnail sınıfına sahip div öğelerini bulun
root_div = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.ID, 'root'))
)
div_elements = root_div.find_elements(By.CSS_SELECTOR, 'div.most-thumbnail')

game_links = []
# Her div öğesi için a etiketinin href özniteliğini çekin
for div_element in div_elements:
    a_element = div_element.find_element(By.TAG_NAME, 'a')
    href = a_element.get_attribute('href')
    game_links.append(href)
"""

# Selenium WebDriver'ı başlatın
service = Service()  # chromedriver dosyasının yolunu belirtin

chop = webdriver.ChromeOptions()
chop.add_extension('Adblock.crx')
driver = webdriver.Chrome(service=service,options=chop)
time.sleep(5)
driver.switch_to.window(driver.window_handles[0])
# Web sitesini yükleyin
url = 'https://html5.gamedistribution.com/'
driver.get(url)

class Games:
    def __init__(self,title,category,link,description,iframecode):
        self.title = title
        self.category = category
        self.link = link
        self.description = description
        self.iframecode = iframecode

def iframeextractor(link):
    # İlk linki kullanarak içeriği çekin
        driver.get(link)
        print("LINK OPPENING")
        # İşlemlere devam edebilirsiniz
        time.sleep(5)
        # "accept" butonuna tıklayın
        try:
            accept_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler'))
            )
            accept_button.click()
        except:
            print("Belirli sınıf bulunamadı. Butona tıklanmadı.")
        try:
            accept_button2 = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, 'pluto-splash-button'))
            )
            accept_button2.click()
        except:
            print("Buton Bulunamadı")
        time.sleep(15)
        try:
            skip_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'videoAdUiSkipButtonExperimentalText'))
            )
            skip_button.click()
        except:
            print("Belirli sınıf bulunamadı. Butona tıklanmadı.")
        time.sleep(15)


        iframe_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
        )

        # İframe içeriğini çekin
        driver.switch_to.frame(iframe_element)
        iframe_content = driver.page_source
        return iframe_content

def initiategamelist(xml):
    soup = BeautifulSoup(open(xml, 'rb'), "html.parser")
    entries = soup.find_all('item')
    time.sleep(5)
    for entry in entries:
        title=entry.title.text
        category=entry.category.text
        guid=entry.guid.text
        description=entry.description.text
        link="https://html5.gamedistribution.com/"+guid
        iframecode = iframeextractor(link)
        game = Games(title,category,link,description,iframecode)
        postgame(game)
        print("DONE LISTING")

def postgame(game):
    wp = Client('https://jokeroyun.com/xmlrpc.php','jokeroyun','nurican3535')
    wp.call(GetPosts())
    wp.call(GetUserInfo())

    post = WordPressPost()
    post.title = game.title
    post.content = '<iframe id="oyun" src="{}" width="800" height="600" allow="autoplay" allowfullscreen></iframe>'.format(game.link)

    postid = wp.call(NewPost(post))

    print(postid)



xml = "3D1.xml"
initiategamelist(xml)