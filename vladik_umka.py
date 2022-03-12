import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = r"https://fondymka.ru/nashi-podopechnye"
base_url = r"https://fondymka.ru"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'lxml')

for group in [temp for temp in soup.find_all('div', class_='subCategory')]:
    group_name = group.text.strip()
    if not os.path.exists(group_name):
        os.mkdir(group_name)

    driver.get(base_url + group.find("a")["href"])
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for animal in [temp for temp in soup.find_all('span', class_='catItemImage')]:
        driver.get(base_url + animal.find("a")["href"])
        soup = BeautifulSoup(driver.page_source, 'lxml')

        title = soup.find("h2", class_="itemTitle").text.strip()
        print(title)
        description = soup.find("div", class_="info_right_animals").text.replace("\n\n\n", " ").strip()
        description += "\n\n"
        description += soup.find("div", class_="itemFullText").text

        if not os.path.exists(f"{group_name}/{title}"):
            os.mkdir(f"{group_name}/{title}")

        with open(f'{group_name}/{title}/!.txt', 'wb') as handler:
            handler.write(description.encode())

        for index, photo_url in enumerate(soup.find_all("li", class_="sigFreeThumb")[:5]):
            with open(f'{group_name}/{title}/{index}.jpg', 'wb') as handler:
                handler.write(requests.get(base_url + photo_url.find("a")["href"]).content)

driver.close()
