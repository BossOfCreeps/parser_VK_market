from time import sleep
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains

url = r"https://vk.com/topic-144002248_40898385"
vk_url = r"https://vk.com"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

SCROLL_PAUSE_TIME = 2

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

soup = BeautifulSoup(driver.execute_script("return document.body.innerHTML;"), 'lxml')
for i, message in enumerate(soup.find_all('div', class_='bp_post clear_fix')):
    description = message.find("div", class_="bp_text").text.strip()

    if not os.path.exists(str(i)):
        os.mkdir(str(i))

    with open(f'{i}/!.txt', 'wb') as handler:
        handler.write(description.encode())

for i, message in enumerate(soup.find_all('div', class_='bp_post clear_fix')):
    url = message.find("div", class_="bp_browse_images")
    if not url:
        continue

    driver.get(f'{vk_url}{url.find("a")["href"]}')
    soup = BeautifulSoup(driver.execute_script("return document.body.innerHTML;"), 'lxml')

    for number, img in enumerate(soup.find_all("img")):
        img_data = requests.get(img["src"]).content
        with open(f'{i}/{number}.jpg', 'wb') as handler:
            handler.write(img_data)

driver.close()
