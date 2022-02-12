import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains

url = "https://rodnyegoroda.ru/projects/all/edinaia-baza-zhivotnykh-v-priiutakh-muzzlebook"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)

ActionChains(driver).move_to_element(driver.find_element_by_id('ui_albums_load_more')).click().perform()
