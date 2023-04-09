import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://kotolend.ru/need-help"
base_url = "https://kotolend.ru"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(url.format(url))
soup = BeautifulSoup(driver.page_source, 'lxml')

for counter, animal_link in enumerate(el.find('a') for el in soup.find_all("div", class_="page-header")):
    if not os.path.exists(f"{counter}"):
        os.mkdir(f"{counter}")

    driver.get(base_url + animal_link["href"])
    soup2 = BeautifulSoup(driver.page_source, 'lxml')

    description = soup2.find("div", itemprop="articleBody").text + "\n\n"

    with open(f'{counter}/!.txt', 'wb') as handler:
        handler.write(description.encode())

    for i, img in enumerate(soup2.find_all("a", class_="sigFreeLink")):
        with open(f'{counter}/{i}.jpg', 'wb') as handler:
            handler.write(requests.get(base_url + img["href"]).content)

driver.close()
