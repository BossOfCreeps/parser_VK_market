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
for number, animal in enumerate(soup.find_all('div', class_='js-product')):
    try:
        folder = number
        if not os.path.exists(str(folder)):
            os.mkdir(str(folder))

        driver.get(animal.find("a")["href"])
        print(animal.find("a")["href"])
        sleep(2)
        soup2 = BeautifulSoup(driver.execute_script("return document.body.innerHTML;"), 'lxml')

        description = soup2.find("div", class_="t-store__prod-popup__info").text.strip()
        with open(f'{folder}/{number}.txt', 'wb') as handler:
            handler.write(description.encode())

        for i, photo in enumerate(soup2.find_all("div", class_="t-slds__thumbsbullet")):
            with open(f'{folder}/{i}.jpg', 'wb') as handler:
                handler.write(requests.get(photo.find("div", class_="loaded")["data-original"]).content)
    except:
        pass
driver.close()
