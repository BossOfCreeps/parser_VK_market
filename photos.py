import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = r"https://vk.com/album-4775134_150198141"
vk_url = r"https://vk.com"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)

SCROLL_PAUSE_TIME = 5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

sleep(2)
soup = BeautifulSoup(driver.execute_script("return document.body.innerHTML;"), 'lxml')

for number, photos_row in enumerate(soup.find_all('div', class_='photos_row')[665:], start=1000):
    try:
        folder = "dogs_"
        if not os.path.exists(str(folder)):
            os.mkdir(str(folder))

        driver.get(vk_url + photos_row.find("a")["href"])
        sleep(2)
        soup2 = BeautifulSoup(driver.execute_script("return document.body.innerHTML;"), 'lxml')
        market_item_description = soup2.find("div", class_="pv_desc_cont")
        pv_photo = soup2.find('div', id='pv_photo')

        description = market_item_description.text.strip() if market_item_description is not None else ". ."

        with open(f'{folder}/{number}.txt', 'wb') as handler:
            handler.write(description.encode())

        with open(f'{folder}/{number}.jpg', 'wb') as handler:
            handler.write(requests.get(pv_photo.find("img")["src"]).content)
    except BaseException as ex:
        print(ex)
driver.close()
