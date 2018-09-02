import json

import requests
import re
from urllib.parse import urlencode
import time
import numpy as np
from pyquery import PyQuery as pq
headers = {
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh - CN, zh;q = 0.9, en;q = 0.8',
        'Cache-Control': 'max - age = 0',
        'Connection': 'keep - alive',
        'Host': 'weixin.sogou.com',
        'Cookie': 'SUV=005B436DDA6B84CD593D3CE5EEDBD285; ssuid=7795656980; dt_ssuid=3416084972; _ga=GA1.2.2088121334.1501526998; GOTO=; SUID=53D5786A4D238B0A59165B6E00097365; pex=C864C03270DED3DD8A06887A372DA219231FFAC25A9D64AE09E82AED12E416AC; usid=4SAwKqYSbh3YlKzr; LSTMV=420%2C149; LCLKINT=5793; CXID=8F977B45EDE554196397E9A9A04FAA1B; ad=t0lmSlllll2bU@f5lllllVH@szDlllllzX0qtlllll9lllllpj7ll5@@@@@@@@@@; ABTEST=0|1535812609|v1; IPLOC=CN1100; weixinIndexVisited=1; sct=18; JSESSIONID=aaavAiEnOUvVG52THQBvw; PHPSESSID=if7rm14b9326spgp7kvkjs3837; SUIR=E1B468D8030677D23E74D06B03AA8EDC; SNUID=0F5B8636ECE9993E1F2C3C61ED27C2E3; ppinf=5|1535860607|1537070207|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTUlQkMlQTAlRTglQjYlODUlRTYlOUQlQjB8Y3J0OjEwOjE1MzU4NjA2MDd8cmVmbmljazoyNzolRTUlQkMlQTAlRTglQjYlODUlRTYlOUQlQjB8dXNlcmlkOjQ0Om85dDJsdVBJSy0wSEo0dDBuZUdZbGp4V3JISkFAd2VpeGluLnNvaHUuY29tfA; pprdig=F8TDsUMG0C4Ljt4qplfRkFWLUZym5QiF98KJuPyRETZDEqaw61Lulyt7vXzidytxLHvXgORFZUa-_67vb_XPRW548aITmZ8KoHCLXne6HJUcByjk0gO2d4JMhnEM71QLa1_oNueDhvnTer9sQXSxJ9MjtWim81WwfFfGFF95go0; sgid=15-36913821-AVuLX38konjQm1spjmDZyzg; ppmdig=15358605980000002768fb9edfd4fcc10d30ddbcc58ad77e',
        'Referer': 'http://weixin.sogou.com/weixin?query=%E6%8B%9B%E8%81%98&type=2&page=100&ie=utf8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
COOKIES_POOL_URL = ""
query = 'NBA'
base_url = "http://weixin.sogou.com/weixin?"
PROXY_POOL_URL = 'http://10.77.40.60:5555/random'
valid_status = [200]


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


def get_cookies():
    try:
        response = requests.get(COOKIES_POOL_URL)
        if response.status_code == 200:
            return response.text
        else:
            return get_cookies()
    except Exception as e:
        print(e.args)
        return get_cookies()

def get_index_urls(page):
    res = []
    data = {
        'query': query,
        'type': 2,
        'page': page,
        'ie': 'utf8'
    }
    url = base_url+urlencode(data)
    try:
        proxy = get_proxy()
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
        response = requests.get(url, headers=headers, proxies=proxies, allow_redirects=False, timeout=10)
        print(response.status_code)
        if response.status_code == 302:
            return get_index_urls(page)
        doc = response.text
        urls = re.findall('<h3>.*?<a target="_blank" href="(http://.*?)".*?</a>.*?</h3>', doc, re.S)
        print(len(urls))
        print(urls)
        for url in urls:
            url = re.sub("amp;", "", url)
            res.append(url)
        print(res)
        return res
    except Exception as e:
        print(e.args)
        return get_index_urls(page)


def parse_detail_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        doc = pq(response.text)
        title = doc('#activity-name').text().strip()
        wechat = doc('#js_name').text().strip()
        wechat_id = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        wechat_description = doc('#js_profile_qrcode > div > p:nth-child(4) > span').text()
        items = doc('#js_content p').items()
        text = '\n'.join([ item.text() for item in items])
        data = {
            'title': title,
            'wechat': wechat,
            'wechat_id':wechat_id,
            'wechat_description':wechat_description,
            'text':text
        }
        yield data




def main():
    for page in range(1, 101):
        print("-------------"+ str(page) +"------------")
        with open('urls_res.txt', 'a+', encoding='utf8') as f:
            res = get_index_urls(page)
            print(len(res))
            for url in res:
                f.write(url + '\n')
                for item in parse_detail_page(url=url):
                    f.write(json.dumps(item, ensure_ascii=False)+'\n')

        time.sleep(np.random.randint(36, 120))
        if page%10 == 0:
            time.sleep(np.random.randint(200, 300))



if __name__ == '__main__':
    main()

