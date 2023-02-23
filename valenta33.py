import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = r"https://valenta33.ru/product-category/dogs/page/{}/"

driver = webdriver.Chrome("chromedriver.exe")

counter, page = 0, 0
while True:
    page += 1
    driver.get(url.format(page))
    soup = BeautifulSoup(driver.page_source, 'lxml')

    for animal_link in soup.find_all('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link'):
        counter += 1
        if not os.path.exists(f"{counter}"):
            os.mkdir(f"{counter}")

        driver.get(animal_link["href"])
        soup2 = BeautifulSoup(driver.page_source, 'lxml')

        description = soup2.find("div", class_="summary").text + "\n\n"
        try:
            description += soup2.find("div", class_="woocommerce-Tabs-panel").text
        except:
            print(counter, animal_link["href"])

        with open(f'{counter}/!.txt', 'wb') as handler:
            handler.write(description.encode())

        for i, img in enumerate(
                soup2.find("div", class_="woocommerce-product-gallery").find_all("img", loading="lazy")
        ):
            with open(f'{counter}/{i}.jpg', 'wb') as handler:
                handler.write(requests.get(img["src"]).content)

driver.close()
