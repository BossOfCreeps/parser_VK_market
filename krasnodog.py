import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = r"https://krasnodog.ru/zhivotnyie/?page={}&status%5B0%5D=Можно+забрать"

driver = webdriver.Chrome("chromedriver.exe")
for page in range(1, 16):
    driver.get(url.format(page))
    sleep(2)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for animal_card_i, animal_card in enumerate(soup.find_all("a", class_="animal-card__img")):
        driver.get(animal_card["href"])
        sleep(2)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        description = soup.find("h1", class_="animal__content-title").text.strip() + "\n\n"
        description += soup.find("div", class_="animal__info clear").text.strip() + "\n\n"
        description += soup.find("div", class_="animal__about-text").text.strip()

        folder = f"{page} {animal_card_i}"
        if not os.path.exists(f"{folder}"):
            os.mkdir(f"{folder}")

        with open(f'{folder}/!.txt', 'wb') as handler:
            handler.write(description.encode())

        for img_i, img in enumerate(soup.find_all("a", class_="animal__gallery-slide")):
            with open(f'{folder}/{img_i}.jpg', 'wb') as handler:
                handler.write(requests.get("https://krasnodog.ru" + img["href"]).content)

driver.close()
