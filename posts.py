import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

url = r"https://vk.com/priutlaska"
vk_url = r"https://vk.com"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)

SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

sleep(2)
soup = BeautifulSoup(driver.execute_script("return document.body.innerHTML;"), 'lxml')

for post_number, post_a in enumerate(soup.find_all('a', class_='post_link')):
    try:
        print(post_number)
        driver.get(vk_url + post_a["href"])
        sleep(2)
        soup2 = BeautifulSoup(driver.page_source, 'lxml')

        description = soup2.find("div", class_="wall_post_text").text

        if "#вдобрыеруки" not in description:
            continue

        if not os.path.exists(str(post_number)):
            os.mkdir(str(post_number))

        with open(f'{post_number}/!.txt', 'wb') as handler:
            handler.write(description.encode())

        for photo_number, photo in enumerate(soup2.find_all('a', class_="page_post_thumb_wrap")):
            style = photo["style"]
            url = style[style.index("background-image: url(") + 22:style.index(');')]

            with open(f'{post_number}/{photo_number}.jpg', 'wb') as handler:
                handler.write(requests.get(url).content)

    except BaseException as ex:
        print(f"{post_number}: {ex}")
