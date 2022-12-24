import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome("chromedriver.exe")

for page in range(1, 5):
    driver.get(f"http://lis-chel.ru/all-pets/?ipg_id=160&curpage={page}#iks_top_anchor_160")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    soup = BeautifulSoup(driver.page_source, 'lxml')
    for i, animal_url in enumerate(soup.find_all('a', class_='iks-title')):
        folder = f"{page}-{i}"
        driver.get(animal_url["href"])
        sleep(2)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        title = soup.find("h1", class_="entry-title").text
        description = title + "\n\n" + soup.find("div", class_="entry-content").text
        description = soup.find("div", class_="take-status").text + "\n\n" + description

        if not os.path.exists(str(folder)):
            os.mkdir(str(folder))

        with open(f'{folder}/!.txt', 'wb') as handler:
            handler.write(description.encode())

        try:
            for j, img in enumerate(soup.find("div", class_="iks-gallery").find_all("img")):
                with open(f'{folder}/{j}.jpg', 'wb') as handler:
                    handler.write(requests.get(img["src"].replace("-150x150", "")).content)
        except:
            pass
driver.close()
