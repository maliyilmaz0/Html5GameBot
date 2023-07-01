###https://catalog.api.gamedistribution.com/api/v2.0/rss/All/?collection=All&categories=All&tags=All&subType=All&type=All&mobile=All&rewarded=all&amount=10&page=1&format=xml
###


import requests
import xml.etree.cElementTree as ET

keywords=["Racing","Girls","Soccer","Adventure","Shooting","3D","Cooking"]
offsets=[1,2,3,4,5]
importlist=[]


for word in keywords:
    for offset in offsets:
        response = requests.get("https://catalog.api.gamedistribution.com/api/v2.0/rss/All/?collection=All&categories={}&tags=All&subType=All&type=All&mobile=All&rewarded=all&amount=40&page={}&format=xml".format(word,offset))
        importlist.append('{}{}.xml'.format(word,offset))
        with open('{}{}.xml'.format(word,offset), 'wb') as file:
            file.write(response.content)

"print(importlist)"
