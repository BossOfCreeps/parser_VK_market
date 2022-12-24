import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

url = r"https://vk.com/koshkindom_tlt"
vk_url = r"https://vk.com"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)
SCROLL_PAUSE_TIME = 5

input("НАЖИМИТЕ ЧТО-НИБУДЬ")

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    soup = BeautifulSoup(driver.execute_script("return document.body.innerHTML;"), 'lxml')
    if len(soup.find_all('a', class_='post_link')) > 2000:
        break

sleep(2)
soup = BeautifulSoup(driver.execute_script("return document.body.innerHTML;"), 'lxml')

for post_number, post_a in enumerate(soup.find_all('a', class_='post_link')):
    try:
        print(post_number)
        driver.get(vk_url + post_a["href"])
        sleep(2)
        soup2 = BeautifulSoup(driver.page_source, 'lxml')

        description = soup2.find("div", class_="wall_post_text").text

        if not os.path.exists(str(post_number)):
            os.mkdir(str(post_number))

        with open(f'{post_number}/!.txt', 'wb') as handler:
            handler.write(description.encode())

        photos_0 = driver.find_elements(By.CLASS_NAME, 'MediaGrid__imageElement')
        photos_1 = driver.find_elements(By.CLASS_NAME, 'MediaGrid__imageOld')
        photos_2 = driver.find_elements(By.CLASS_NAME, 'page_post_thumb_wrap')

        for photo_number, el in enumerate(photos_0 + photos_1 + photos_2):
            ActionChains(driver).move_to_element(el).click().perform()
            sleep(1)
            ActionChains(driver).move_to_element(
                driver.find_element(By.CLASS_NAME, "UnauthActionBox__close")).click().perform()
            sleep(1)
            soup3 = BeautifulSoup(driver.page_source, 'lxml')
            url = soup3.find("div", class_="pv_photo_wrap").find("img")["src"]
            with open(f'{post_number}/{photo_number}.jpg', 'wb') as handler:
                handler.write(requests.get(url).content)

            ActionChains(driver).move_to_element(driver.find_element(By.CLASS_NAME, "pv_close_btn")).click().perform()
            sleep(2)

    except BaseException as ex:
        print(f"{post_number}: {ex}")
