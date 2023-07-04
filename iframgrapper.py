import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from googletrans import Translator
from bs4 import BeautifulSoup
import requests
import os
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
url = 'https://jokeroyun.com/admin'
driver.get(url)
time.sleep(3)
id = driver.find_element(By.XPATH,'//*[@id="user_login"]')
id.send_keys('jokeroyun')
password = driver.find_element(By.XPATH,'//*[@id="user_pass"]')
password.send_keys('nurican+3535')
loginbutton = driver.find_element(By.XPATH,'//*[@id="wp-submit"]')
driver.execute_script("arguments[0].click();",loginbutton)
time.sleep(3)
postsbutton = driver.find_element(By.XPATH, '//*[@id="menu-posts"]/a')
driver.execute_script("arguments[0].click();", postsbutton)
time.sleep(3)

class Games:
    def __init__(self,title,category,link,description,guid):
        self.title = title
        self.category = category
        self.link = link
        self.description = description
        self.guid = guid

def categoryselector(category):
    print(category)
    word = ''
    if category == "ZD" or "Bulmaca":
        word = '//*[@id="inspector-checkbox-control-5"]'
        return word
    elif category == "Yarışma":
        word = '//*[@id="inspector-checkbox-control-3"]'
        return  word
    elif category == "Kızlar":
        word = '//*[@id="inspector-checkbox-control-4"]'
        return word
    elif category == "Futbol" or "Spor":
        word = '//*[@id="inspector-checkbox-control-6"]'
        return word
    elif category == "Macera" or "Aksiyon":
        word = '//*[@id="inspector-checkbox-control-8"]'
        return word
    elif category == "Silah" or "Erkekler":
        word = '//*[@id="inspector-checkbox-control-10"]'
        return word
    elif category == 'Yemek Yapma':
        word = '//*[@id="inspector-checkbox-control-13"]'
        return word
    else:
        word = '//*[@id="inspector-checkbox-control-11"]'
        return word




def initiategamelist(xml):
    soup = BeautifulSoup(open(xml, 'rb'), "html.parser")
    entries = soup.find_all('item')
    time.sleep(5)
    for entry in entries:
        title=entry.title.text
        category=entry.category.text
        print(category)
        guid=entry.guid.text
        description=entry.description.text
        link="https://html5.gamedistribution.com/"+guid
        game = Games(title,category,link,description,guid)
        postgame(game)
        print("DONE LISTING")

def postgame(game):
    """'<iframe id="oyun" src="{}" width="800" height="600" allow="autoplay" allowfullscreen></iframe>'.format(game.link)"""

    newpostbutton = driver.find_element(By.XPATH,'//*[@id="wpbody-content"]/div[3]/a')
    driver.execute_script("arguments[0].click();", newpostbutton)
    time.sleep(3)
    gamesettingsbutton = driver.find_element(By.XPATH,'//*[@id="ui-id-2"]')
    driver.execute_script("arguments[0].click();", gamesettingsbutton)
    time.sleep(3)
    select = Select(driver.find_element(By.XPATH,'//*[@id="game_type"]'))
    select.select_by_visible_text('HTML5')
    time.sleep(3)
    gamecode = driver.find_element(By.XPATH, '//*[@id="html5code"]')
    gamecode.send_keys('<iframe id="oyun" src="{}" width="800" height="600" allow="autoplay" allowfullscreen></iframe>'.format(game.link))
    time.sleep(3)
    translator = Translator()
    for i in range(len(game.category)-1):
        translatedcategory = translator.translate(game.category, dest='tr')
        "print('WOOORDDDD', translatedcategory.text)"
        word = categoryselector(translatedcategory.text)
        driver.find_element(By.XPATH, word).click()
    time.sleep(3)
    with open('{}.jpg'.format(game.guid), 'wb') as handle:
        response = requests.get("https://img.gamedistribution.com/{}-512x384.jpeg".format(game.guid),stream=True)
        if not response.ok:
            "print(response)"
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

    imageupload = driver.find_element(By.XPATH,'//*[@id="editor"]/div/div[1]/div[1]/div[2]/div[3]/div/div[3]/div[4]/div/div/button')
    driver.execute_script("arguments[0].click();",imageupload)
    time.sleep(1)
    imageuploadin = driver.find_element(By.XPATH,'//*[@id="menu-item-upload"]')
    driver.execute_script("arguments[0].click();", imageuploadin)
    upload = driver.find_element(By.XPATH,"/html/body/div[4]/div[1]/div/div/div[6]/input")
    upload.send_keys(os.getcwd()+"/{}.jpg".format(game.guid))
    time.sleep(5)
    selectthispic = driver.find_element(By.XPATH, '//*[@id="__wp-uploader-id-0"]/div[4]/div/div[2]/button')
    driver.execute_script("arguments[0].click();", selectthispic)


    time.sleep(3)
    translateddesc = translator.translate(game.description, dest='tr')
    desc = driver.find_element(By.XPATH,'//*[@id="editor"]/div/div[1]/div[1]/div[2]/div[2]/div[3]/div[2]/div/div[2]/div[2]/div/div/p')
    desc.send_keys(translateddesc.text)
    title = driver.find_element(By.XPATH,'//*[@id="editor"]/div/div[1]/div[1]/div[2]/div[2]/div[3]/div[2]/div/div[2]/div[1]/h1')
    title.send_keys(game.title)
    time.sleep(10)


    share = driver.find_element(By.XPATH,'//*[@id="editor"]/div/div[1]/div[1]/div[1]/div/div[3]/button[2]')
    driver.execute_script("arguments[0].click();",share)
    sharecorrection = driver.find_element(By.XPATH,'//*[@id="editor"]/div/div[1]/div[1]/div[2]/div[4]/div[2]/div/div/div[1]/div[1]/button')
    driver.execute_script("arguments[0].click();", sharecorrection)
    time.sleep(3)

    returnhome = driver.find_element(By.XPATH,'//*[@id="editor"]/div/div[1]/div[1]/div[1]/div/div[1]/div/a')
    driver.execute_script("arguments[0].click();", returnhome)
    time.sleep(3)


def startbot():
    keywords = []
    print("Kategori seç = Araba Giydirme Futbol Macera Savaş Beceri Yemek Pişirme")
    keyword = input()
    if keyword == "Araba":
        keywords.append("Racing")
    elif keyword == "Giydirme":
        keywords.append("Girls")
    elif keyword == "Futbol":
        keywords.append("Soccer")
    elif keyword == "Macera":
        keywords.append("Adventure")
    elif keyword == "Savaş":
        keywords.append("Shooting")
    elif keyword == "Yemek Pişirme":
        keywords.append("Cooking")
    else:
        print("Geçerli değer giriniz !!!")
        exit()

    offsets=[1,2,3,4,5]
    importlist=[]


    for word in keywords:
        for offset in offsets:
            response = requests.get("https://catalog.api.gamedistribution.com/api/v2.0/rss/All/?collection=All&categories={}&tags=All&subType=All&type=All&mobile=All&rewarded=all&amount=40&page={}&format=xml".format(word,offset))
            importlist.append('{}{}.xml'.format(word,offset))
            print(importlist)
            with open('{}{}.xml'.format(word,offset), 'wb') as file:
                file.write(response.content)

    for f in importlist:
        initiategamelist(f)


startbot()