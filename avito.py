import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = r"file:///C:/Users/seva-/Documents/GitHub/some_parsers/1.html"
base_url = r"https://www.avito.ru"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)
sleep(2)

soup = BeautifulSoup(driver.execute_script("return document.body.innerHTML;"), 'lxml')
for number, animal in enumerate(soup.find_all('div', class_='ItemsGrid-item-_aFbT')):
    folder = number
    if not os.path.exists(str(folder)):
        os.mkdir(str(folder))

    driver.get(base_url + animal.find("a")["href"])
    sleep(2)
    soup2 = BeautifulSoup(driver.execute_script("return document.body.innerHTML;"), 'lxml')

    description = soup2.find("div", class_="style-item-description-text-mc3G6").text.strip()
    with open(f'{folder}/{number}.txt', 'wb') as handler:
        handler.write(description.encode())

    photo = soup2.find('div', class_='image-frame-wrapper-_NvbY')
    with open(f'{folder}/{number}.jpg', 'wb') as handler:
        handler.write(requests.get(photo.find("img")["src"]).content)

driver.close()
