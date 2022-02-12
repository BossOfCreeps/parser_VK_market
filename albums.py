import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains

url = r"https://vk.com/albums-130314264"
vk_url = r"https://vk.com"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)

sleep(2)
ActionChains(driver).move_to_element(driver.find_element_by_id('ui_albums_load_more')).click().perform()
SCROLL_PAUSE_TIME = 1

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

sleep(2)

soup = BeautifulSoup(driver.page_source, 'lxml')
for albums_photos_row in soup.find_all('div', class_='photo_row photos_album _photos_album'):
    driver.get(vk_url + albums_photos_row.find("a")["href"])
    sleep(2)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    try:
        name = soup.find("div", class_="photos_album_intro").find("h1").text
        description = soup.find("div", class_="photos_album_intro_desc").text

        if not os.path.exists(name):
            os.mkdir(name)

        with open(f'{name}/!.txt', 'wb') as handler:
            handler.write(description.encode())

        for number, photos_row in enumerate(soup.find_all('div', class_='photos_row')):
            driver.get(vk_url + photos_row.find("a")["href"])
            sleep(2)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            with open(f'{name}/image_{number}.jpg', 'wb') as handler:
                handler.write(requests.get(soup.find("div", id="pv_photo").find("img")["src"]).content)

    except BaseException as ex:
        print(albums_photos_row.find("a")["href"], ex)

driver.close()
