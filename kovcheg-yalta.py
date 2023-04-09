import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = r"http://kovcheg-yalta.ru/dogs?count={}"

driver = webdriver.Chrome("chromedriver.exe")
for page in range(1, 1000):
    driver.get(url.format(page))
    sleep(2)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for animal_card_i, animal_card in enumerate(soup.find_all("div", class_="cat-dog")):
        folder = f"{page} {animal_card_i}"
        if not os.path.exists(f"{folder}"):
            os.mkdir(f"{folder}")

        description = animal_card.text.strip() + "\n\n"
        with open(f'{folder}/!.txt', 'wb') as handler:
            handler.write(description.encode())

        with open(f'{folder}/.jpg', 'wb') as handler:
            handler.write(requests.get(animal_card.find("a")["href"]).content)

driver.close()
