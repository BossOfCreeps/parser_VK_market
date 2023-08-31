from time import sleep
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

url = r"https://vk.com/market-213409010"
vk_url = r"https://vk.com"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)

#input()
soup = BeautifulSoup(driver.page_source, 'lxml')

# get all products
for i, product_url in enumerate([row.find("a")["href"] for row in soup.find_all('div', class_='market_row')]):
    # wait while data loads
    driver.get(vk_url + product_url)
    print(vk_url + product_url)
    sleep(5)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    title = soup.find("h1", class_="ItemName").text.strip()
    market_item_description = soup.find("div", class_="ItemDescription")
    description = f"{title}\n{market_item_description.text.strip()}" if market_item_description else ""

    print(title)
    print(description)

    # create folder
    if not os.path.exists(str(i)):
        os.mkdir(str(i))

    with open(f'{i}/!.txt', 'wb') as handler:
        handler.write(description.encode())

    # for all image
    for number, _ in enumerate(soup.find_all("div", class_="ItemGallery__thumb")):
        ActionChains(driver).move_to_element(driver.find_elements(By.CLASS_NAME, 'ItemGallery__thumb')[number]).perform()
        sleep(5)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        img_link = soup.find("img", class_="ItemGallery__image")["src"].replace("amp;", "")
        img_data = requests.get(img_link).content
        with open(f'{i}/{number}.jpg', 'wb') as handler:
            handler.write(img_data)

driver.close()
