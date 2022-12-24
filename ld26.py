import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = r"http://ld26.ru/nashi-zhivotnye/index.php"
base_url = r"http://ld26.ru"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'lxml')

for i, animal_div in enumerate([a for a in soup.find("div", class_="CatalogSection").find_all('div', class_='Image')]):
    driver.get(base_url + animal_div.find("a")["href"])
    soup = BeautifulSoup(driver.page_source, 'lxml')

    content = soup.find("div", class_="Content")
    title = content.find("h2").text.strip()
    try:
        description = content.find("div", class_="DetailText").text.strip()
    except:
        description = ""

    if not os.path.exists(str(i)):
        os.mkdir(str(i))

    with open(f'{i}/!.txt', 'wb') as handler:
        handler.write((title + "\n\n" + description).encode())

    for j, img in enumerate(content.find_all("img")):
        with open(f'{i}/{j}.jpg', 'wb') as handler:
            handler.write(requests.get(base_url + img["src"]).content)

driver.close()
