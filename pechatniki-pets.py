from time import sleep
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://pechatniki-pets.ru/catalog")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(driver.page_source, 'lxml')
    sleep(2)
    try:
        ActionChains(driver).move_to_element(driver.find_elements(By.CLASS_NAME, 'svelte-1e2wjee')[1]).click().perform()
    except:
        break
print(len(soup.find_all('a', class_='card svelte-thhk52')))
soup = BeautifulSoup(driver.page_source, 'lxml')
for folder, animal_url in enumerate(soup.find_all('a', class_='card svelte-thhk52')):
    print(animal_url)
    driver.get(animal_url["href"])
    sleep(2)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    description = ""
    for i, el in enumerate(soup.find_all("div", class_="t396__elem")):
        description += el.text + "\n"

    if not os.path.exists(str(folder)):
        os.mkdir(str(folder))

    with open(f'{folder}/!.txt', 'wb') as handler:
        handler.write(description.encode())

    for i, div_img in enumerate(soup.find("div", class_="t-slds__container").find_all("div", class_="t-bgimg")):
        with open(f'{folder}/{i}.jpg', 'wb') as handler:
            handler.write(requests.get(div_img["data-original"]).content)

driver.close()
