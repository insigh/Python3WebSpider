import selenium
import requests
from selenium.common.exceptions import ElementNotSelectableException
from selenium import webdriver

query = 'NBA'
start_url = "http://weixin.sogou.com/weixin?"
PROXY_POOL_URL = 'http://10.77.40.60:5555/random'


def get_proxy():
    """
    从代理池获取代理
    :return:
    """
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            print('Get Proxy', response.text)
            return response.text
        return None

    except requests.ConnectionError:
        return None


def get_index_urls(page):
    pass


browser = webdriver.Chrome()
browser.get(url="", proxies="")






