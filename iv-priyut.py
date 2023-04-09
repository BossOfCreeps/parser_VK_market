import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = r"https://iv-priyut.ru/v-priyute?page={}"

driver = webdriver.Chrome("chromedriver.exe")
for page in range(1, 1000):
    driver.get(url.format(page))
    sleep(2)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for animal_card_i, animal_card in enumerate(soup.find_all("div", class_="pic")):
        driver.get("https://iv-priyut.ru" + animal_card.find("a")["href"])
        sleep(2)
        soup2 = BeautifulSoup(driver.page_source, 'lxml')
        description = soup2.find("div", class_="info").text.strip() + "\n\n"
        try:
            description += soup2.find("div", class_="text").text.strip()
        except:
            pass

        folder = f"{page} {animal_card_i}"
        if not os.path.exists(f"{folder}"):
            os.mkdir(f"{folder}")

        with open(f'{folder}/!.txt', 'wb') as handler:
            handler.write(description.encode())

        with open(f'{folder}/-.jpg', 'wb') as handler:
            handler.write(requests.get(
                soup2.find("div", class_="material_card").find("div", class_="pic").find("img")["src"]
            ).content)

        try:
            for img_i, img in enumerate(soup2.find("div", class_="galery").find_all("a")):
                with open(f'{folder}/{img_i}.jpg', 'wb') as handler:
                    handler.write(requests.get(img["href"]).content)
        except:
            pass

driver.close()
