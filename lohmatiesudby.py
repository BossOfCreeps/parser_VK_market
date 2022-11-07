import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = r"https://lohmatiesudby.ru/sobakeny-i-pyosiki/"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'lxml')

data = soup.find("div", class_="entry-content the-content text-column")

counter = 100
img_counter = 0
cur_text = ""
if not os.path.exists(f"{counter}"):
    os.mkdir(f"{counter}")

for a in data.find_all(True):
    if a.name == "h6":
        cur_text += a.text + "\n\n"

    if a.name == "img":
        if cur_text != "":

            counter += 1
            if not os.path.exists(f"{counter}"):
                os.mkdir(f"{counter}")

            with open(f'{counter}/!.txt', 'wb+') as handler:
                handler.write(cur_text.encode())
            cur_text = ""
            img_counter = 0

        with open(f'{counter}/{img_counter}.jpg', 'wb+') as handler:
            handler.write(requests.get(a["src"]).content)
        img_counter += 1
