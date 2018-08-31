import re

from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome()

browser.close()
#J_SearchForm > button
#J_SearchForm > button
#mainsrp-pager > div > div > div > div.total
# TimeouException
try :
    pass
except TimeoutException:
    pass

re.compile(pattern='.*?(\d+)')