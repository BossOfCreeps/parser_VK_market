import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = r"https://vk.com/albums-39576505"
vk_url = r"https://vk.com"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)

input()

soup = BeautifulSoup(driver.page_source, 'lxml')
for i, albums_photos_row in enumerate(soup.find_all('div', class_='photo_row photos_album _photos_album')):
    driver.get(vk_url + albums_photos_row.find("a")["href"])
    sleep(2)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    try:
        name = soup.find("div", class_="photos_album_intro").find("h1").text

        if "ищет дом" not in name.lower():
            continue

        description = name + "\n\n" + soup.find("div", class_="photos_album_intro_desc").text

        if not os.path.exists(str(i)):
            os.mkdir(str(i))

        with open(f'{i}/!.txt', 'wb') as handler:
            handler.write(description.encode())

        for number, photos_row in enumerate(soup.find_all('div', class_='photos_row')):
            driver.get(vk_url + photos_row.find("a")["href"])
            sleep(2)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            with open(f'{i}/image_{number}.jpg', 'wb') as handler:
                handler.write(requests.get(soup.find("div", id="pv_photo").find("img")["src"]).content)

    except BaseException as ex:
        print(albums_photos_row.find("a")["href"], ex)

driver.close()
