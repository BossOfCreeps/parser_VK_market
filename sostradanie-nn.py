import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome("chromedriver.exe")

for folder in os.listdir():
    if not folder.isnumeric():
        continue

    if not os.path.exists(f"{folder}/!.txt"):
        continue

    with open(f"{folder}/!.txt", encoding="utf-8") as txt_file:
        txt_file_data = txt_file.read()
        start = txt_file_data.find("http://forum.sostradanie-nn.ru/topic/")
        if start == -1:
            continue

    driver.get(txt_file_data[start:])
    soup = BeautifulSoup(driver.page_source, 'lxml')
    text = ""
    img_counter = 0
    for div in soup.find_all("div", class_="post"):
        for br in soup.find_all("br"):
            br.replace_with("\n\n")

        text += div.text + "\n\n"

        for img in div.find_all("img"):
            with open(f'{folder}/{img_counter}.jpg', 'wb+') as handler:
                handler.write(requests.get("http://forum.sostradanie-nn.ru/" + img["src"]).content)
            img_counter += 1

    with open(f'{folder}/text.txt', 'wb+') as handler:
        handler.write(text.encode())
