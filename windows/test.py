from selenium import webdriver
from bs4 import BeautifulSoup
import pymysql
import pymongo
from flask import Flask
import tornado
import lxml
import scrapy


soup = BeautifulSoup('<p>Hello<p>', 'lxml')
print(soup.p.string)


# browser = webdriver.PhantomJS()
# browser.get("https://www.baidu.com")
# print(browser.current_url)

