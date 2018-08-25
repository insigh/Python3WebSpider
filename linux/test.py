from selenium import webdriver
import requests
import lxml
from bs4 import BeautifulSoup
import pyquery
import PIL
import pytesseract
from PIL import Image
import scrapy


image = Image.open("./image.png")
print(pytesseract.image_to_string(image ))

# soup = BeautifulSoup("<p>Hello<p>", 'lxml')
# print(soup.p.string)

# browser= webdriver.Firefox()
# browser = webdriver.Chrome()
# browser = webdriver.PhantomJS()
# browser.get("https://www.baidu.com")
# print(browser.current_url)