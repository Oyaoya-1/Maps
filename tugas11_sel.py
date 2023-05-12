from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep 

driver = webdriver.Chrome('./chromedriver.exe')
url = "https://www.spacex.com/launches/"
driver.get(url)
sleep(5)

req = driver.page_source

driver.quit()

soup = BeautifulSoup(req, 'html.parser')

space = soup.select('.item')
for item in space:
    date = item.select_one('.date').text.strip()
    title = item.select_one('.label').text.strip()
    print(date, title)