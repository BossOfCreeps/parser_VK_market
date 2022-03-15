import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = r"http://pesikot65.ru/cat.php"
base_url = r"http://pesikot65.ru/"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'lxml')

for animal_div in [temp for temp in soup.find_all('div', class_='animal')]:
    title = animal_div.find("h1", class_="name").text.strip()
    description = animal_div.find("div", class_="animaldescription").text.strip()

    if not os.path.exists(f"{title}"):
        os.mkdir(f"{title}")

    with open(f'{title}/!.txt', 'wb') as handler:
        handler.write(description.encode())

    with open(f'{title}/image.jpg', 'wb') as handler:
        handler.write(requests.get(base_url + animal_div.find("img")["src"]).content)

driver.close()
