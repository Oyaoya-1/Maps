from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from pymongo import MongoClient
import certifi
import requests


client = MongoClient('mongodb://coba:mencoba@ac-aza6t4b-shard-00-00.h6atr6m.mongodb.net:27017,ac-aza6t4b-shard-00-01.h6atr6m.mongodb.net:27017,ac-aza6t4b-shard-00-02.h6atr6m.mongodb.net:27017/?ssl=true&replicaSet=atlas-wiabc0-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.dbannisa

driver = webdriver.Chrome('./chromedriver.exe')
url = 'https://www.yelp.com/search?cflt=restaurants&amp;find_loc=San+Francisco%2C+CA'

driver.get(url)
sleep(5)
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
sleep(3)

access_token = "pk.eyJ1IjoibW9vbmExIiwiYSI6ImNsZnl0ZWtucTBxa3Iza21rZmE4cTN0dmYifQ.NsR-Z8cBogNeJYsanz5xwQ"
long = -122.420679
lat = 37.772537

start = 0

seen = {}

for _ in range(5): 
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    restaurants = soup.select('div[class*="arrange-unit__"]')
    for restaurant in restaurants:
        name_business = restaurant.select_one('div[class*="businessName__"]')
        if not name_business:
            continue
        name = name_business.text.split('.')[-1].strip()

        if name in seen:
            continue

        seen[name] = True

        link = name_business.select_one('a')['href']
        link = 'https://www.yelp.com' + link

        category = restaurant.select_one('div[class*="priceCategory__"]')
        spans = category.select('span')
        categories = spans[0].text.strip()
        location = spans[-1].text.strip()

        geo_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?proximity={long},{lat}&access_token={access_token}"
        geo_response = requests.get(geo_url)
        geo_json = geo_response.json()
        center = geo_json['features'][0]['center']


        print(name, ',', categories, ',', location) 

        doc = {
            'name': name,
            'categories': categories,
            'location': location,
            'link': link,
            'center': center,
        }
        db.restaurants.insert_one(doc)
    start += 10
    driver.get(f'{url}&start={start}')
    sleep(3)




driver.quit()    