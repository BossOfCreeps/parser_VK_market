from time import sleep
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains

url = r"file:///C:/Users/Seva/Downloads/Друг.html"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'lxml')

# get all products
for product_url in [market_row.find("a")["href"] for market_row in soup.find_all('h2', class_='uk-margin-remove')]:
    # wait while data loads
    driver.get(product_url)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    title = soup.find("h1", class_="uk-article-title").text
    description = soup.find("dl", class_="uk-description-list-horizontal uk-margin-remove").text.strip()

    # create folder
    if not os.path.exists(title):
        os.mkdir(title)

    with open(f'{title}/!.txt', 'wb') as handler:
        handler.write(description.encode())

    with open(f'{title}/image.jpg', 'wb') as handler:
        handler.write(requests.get(f"https://dog-omsk.ru" + soup.find("a", class_="uk-thumbnail")["href"]).content)

driver.close()
