from time import sleep
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains

url = r"https://vk.com/market-45542940"
vk_url = r"https://vk.com"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'lxml')

# get all products
for product_url in [market_row.find("a")["href"] for market_row in soup.find_all('div', class_='market_row')]:
    # wait while data loads
    market_item_description = None
    while market_item_description is None:
        driver.get(vk_url + product_url)
        sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        market_item_description = soup.find("div", id="market_item_description")

    description = market_item_description.text.strip()

    title = soup.find("div", class_="market_item_title").text

    # create folder
    if not os.path.exists(title):
        os.mkdir(title)

    with open(f'{title}/!.txt', 'wb') as handler:
        handler.write(description.encode())

    # for all image
    for number, _ in enumerate(soup.find_all("div", class_="market_item_thumb")):
        # hover cropped image, reload html and save image
        ActionChains(driver).move_to_element(driver.find_element_by_id(f'market_item_thumb{number}')).perform()
        soup = BeautifulSoup(driver.page_source, 'lxml')
        img_link = soup.find("img", id="market_item_photo")["src"].replace("amp;", "")
        img_data = requests.get(img_link).content
        with open(f'{title}/{number}.jpg', 'wb') as handler:
            handler.write(img_data)

driver.close()
