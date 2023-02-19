import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = r"https://www.instagram.com/vikka_sochi/"
base_url = r"https://www.instagram.com"

driver = webdriver.Chrome("chromedriver.exe")
input("Введите текст после авторизации")
driver.get(url)

input("Введите текст после авторизации")
img_url_set = set()

# Scroll down
SCROLL_PAUSE_TIME = 3
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

    soup = BeautifulSoup(driver.execute_script("return document.body.innerHTML;"), 'lxml')
    for div in soup.find_all('div', class_='_aabd _aa8k _aanf'):
        img_url_set.add(f"{base_url}{div.find('a')['href']}")

    if len(img_url_set) > 300:
        break

sleep(2)

soup = BeautifulSoup(driver.execute_script("return document.body.innerHTML;"), 'lxml')
for post_number, img_url in enumerate(img_url_set):
    try:
        driver.get(img_url)
        sleep(2)
        soup2 = BeautifulSoup(driver.page_source, 'lxml')

        if not os.path.exists(str(post_number)):
            os.mkdir(str(post_number))

        with open(f'{post_number}/1.jpg', 'wb') as handler:
            handler.write(requests.get(soup2.find("div", class_="_aa06").find("img")["srcset"].split(" ")[0]).content)

        description = soup2.find_all("div", class_="_a9zr")[0].text
        with open(f'{post_number}/!.txt', 'wb') as handler:
            handler.write(description.encode())

    except BaseException as ex:
        print(f"{post_number}: {ex}")
