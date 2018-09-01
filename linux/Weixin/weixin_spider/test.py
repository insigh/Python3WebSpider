import requests
import re
from urllib.parse import urlencode

headers = {
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh - CN, zh;q = 0.9, en;q = 0.8',
        'Cache-Control': 'max - age = 0',
        'Connection': 'keep - alive',
        'Host': 'weixin.sogou.com',
        'Cookie': 'SUV=0021271767582E3E5AEFC2DB3AFEE888; ABTEST=0|1535789254|v1; IPLOC=CN1100; SUID=4DB66ADA232C940A000000005B8A48C6; SUID=4DB66ADA2213940A000000005B8A48C6; weixinIndexVisited=1; JSESSIONID=aaaH5vt1Cy3YF7ZR7SBvw; ppinf=5|1535789325|1536998925|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTUlQkMlQTAlRTglQjYlODUlRTYlOUQlQjB8Y3J0OjEwOjE1MzU3ODkzMjV8cmVmbmljazoyNzolRTUlQkMlQTAlRTglQjYlODUlRTYlOUQlQjB8dXNlcmlkOjQ0Om85dDJsdVBJSy0wSEo0dDBuZUdZbGp4V3JISkFAd2VpeGluLnNvaHUuY29tfA; pprdig=rhOfX5Gbfo7ynR3KgN8zLx4KfcDNIZN9c_7wq4WeCrHIWMveKXPBXlJmG45_0ZTP_93N1tnfQrCfukkbbxvNbA8UtPtNqaXoAo1irgPQ7OujPc4OrLtR5ykw6FcMFAFmxPUzSY_cZXPxuhm8iXHhZzK99z8pd6BzzNx_Qy1Twxc; sgid=15-36913821-AVuKSQ1njKsKRpFsrQJND9M; sct=3; ppmdig=1535808957000000e191c2955bf9c633a2674c2838ec0e93; PHPSESSID=2fsh60hu6d0g2c8kn2fg0l1fk2; SUIR=E812CE7EA5A0D06E68C216D1A5EE8C41; SNUID=A75C8131EBEF9F243FF920AFEB973B5A; seccodeRight=success; successCount=1|Sat, 01 Sep 2018 14:12:29 GMT; refresh=1',
        'Referer': 'http://weixin.sogou.com/weixin?query=%E6%8B%9B%E8%81%98&type=2&page=100&ie=utf8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
query = 'NBA'
base_url = "http://weixin.sogou.com/weixin?"
PROXY_POOL_URL = 'http://0.0.0.0:5555/random'

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
    res = []
    data = {
        'query':query,
        'type': 2,
        'page':page,
        'ie':'utf8'
    }
    url = base_url+urlencode(data)
    try:
        proxy = get_proxy()
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10).text
        urls = re.findall('<h3>.*?<a target="_blank" href="(http://.*?)".*?</a>.*?</h3>', response, re.S)
        print(urls)
        for url in urls:
            url = re.sub("amp;", "", url)
            res.append(url)
    except Exception as e:
        print(e.args)
        get_index_urls(page)
    return res


def main():
    with open('urls_res.txt', 'a+') as f:
        for page in range(1, 10):
            res = get_index_urls(page)
            print(page)
            for url in res:
                f.write(url + '\n')
    f.close()


if __name__ == '__main__':
    main()


