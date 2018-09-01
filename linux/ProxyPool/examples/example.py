import os
import sys
import requests
from bs4 import BeautifulSoup

dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, dir)


def get_proxy():
    r = requests.get('http://0.0.0.0:5555/random', timeout=5)
    proxy = BeautifulSoup(r.text, "lxml").get_text()
    return proxy


def crawl(url, proxy):
    proxies = {'http': proxy}
    r = requests.get(url, proxies=proxies)
    return r.text


def main():
    try:
        proxy = get_proxy()
        print(proxy)
        html = crawl('http://docs.jinkan.org/docs/flask/', proxy)
        print(html)
    except Exception:
        print('代理无效！')
        main()

if __name__ == '__main__':
    main()

