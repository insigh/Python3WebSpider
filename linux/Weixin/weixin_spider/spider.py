from weixin_spider.config import *
from weixin_spider.request import WeixinRequest
from weixin_spider.mysql import MySQL
from weixin_spider.db import  RedisQueue
from requests import Session
import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from requests import ReadTimeout, ConnectionError



class Spider():
    # def __init__(self):
    headers = {
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh - CN, zh;q = 0.9, en;q = 0.8',
        'Cache-Control': 'max - age = 0',
        'Connection': 'keep - alive',
        'Cookie': 'SUV=0021271767582E3E5AEFC2DB3AFEE888; ABTEST=0|1535789254|v1; IPLOC=CN1100; SUID=4DB66ADA232C940A000000005B8A48C6; SUID=4DB66ADA2213940A000000005B8A48C6; weixinIndexVisited=1; SNUID=E812CE7EA5A0D06E68C216D1A5EE8C41; JSESSIONID=aaaH5vt1Cy3YF7ZR7SBvw; ppinf=5|1535789325|1536998925|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTUlQkMlQTAlRTglQjYlODUlRTYlOUQlQjB8Y3J0OjEwOjE1MzU3ODkzMjV8cmVmbmljazoyNzolRTUlQkMlQTAlRTglQjYlODUlRTYlOUQlQjB8dXNlcmlkOjQ0Om85dDJsdVBJSy0wSEo0dDBuZUdZbGp4V3JISkFAd2VpeGluLnNvaHUuY29tfA; pprdig=rhOfX5Gbfo7ynR3KgN8zLx4KfcDNIZN9c_7wq4WeCrHIWMveKXPBXlJmG45_0ZTP_93N1tnfQrCfukkbbxvNbA8UtPtNqaXoAo1irgPQ7OujPc4OrLtR5ykw6FcMFAFmxPUzSY_cZXPxuhm8iXHhZzK99z8pd6BzzNx_Qy1Twxc; sgid=15-36913821-AVuKSQ1njKsKRpFsrQJND9M; ppmdig=1535802476000000026808799edc8d3a263911fdcee925fd; sct=3',
        'Host': 'weixin.sogou.com',
        'Referer': 'http://weixin.sogou.com/weixin?query=%E6%8B%9B%E8%81%98&type=2&page=100&ie=utf8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    base_url = BASE_URL
    key_word = KEY_WORD
    headers = headers
    session = Session()
    queue = RedisQueue()
    mysql = MySQL()


    def get_proxy(self):
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

    def start(self):
        """
        初始化工作
        :return:
        """
        # 全局更新Headers
        self.session.headers.update(self.headers)
        start_url = BASE_URL+'?'+urlencode({'query': "NBA", 'type': 2})
        weixin_request = WeixinRequest(url=start_url, callback=self.parse_index, need_proxy=False)
        #调度第一个请求
        self.queue.add(weixin_request)

    def parse_index(self, response):
        """
        解析索引页
        :param response:
        :return:
        """
        doc = pq(response.text)
        # print(doc)
        items = doc('.news-box .news-list li .txt-box h3 a').items()
        print(len(list(items)))
        for item in items:
            url = item.attr('href')
            print(url)
            weixin_request = WeixinRequest(url=url, callback=self.parse_detail)
            yield weixin_request
        next = doc('#sogou_next').attr('href')
        if next:
            url = BASE_URL+str(next)
            print(url)
            weixin_request = WeixinRequest(url=next, callback=self.parse_index, need_proxy=False)
            yield weixin_request

    def parse_detail(self, response):
        """
        解析详情页
        :param response:
        :return: 微信公众号文章
        """
        doc = pq(response.text)
        data = {
            'title': doc('.rich_media_title').text(),
            'content': doc('.rich_media_content').text(),
            'date': doc('#post-date').text(),
            'nickname': doc('#js_profile_qrcode > div > strong').text(),
            'wechat': doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        }
        yield data

    def request(self, weixin_request):
        """
        执行请求
        :param weixin_request:
        :return: 响应
        """
        try:
            if weixin_request.need_proxy:
                proxy = self.get_proxy()
                if proxy:
                    proxies = {
                        'http': 'http://'+proxy,
                        'https': 'https://'+proxy
                    }
                    return self.session.send(weixin_request.prepare(), timeout=weixin_request.time_out, allow_redirects=False, proxies=proxies)
            return self.session.send(weixin_request.prepare(), timeout=weixin_request.time_out, allow_redirects=False)
        except (ConnectionError, ReadTimeout) as e:
            print(e.args)
            print()
            return False

    def error(self, weixin_request):
        weixin_request.fail_time = weixin_request.fail_time + 1
        # print("Request Failed", weixin_request.fail_time, "Times", weixin_request.url)
        if weixin_request.fail_time < MAX_FAILED_TIME:
            self.queue.add(weixin_request)

    def schedule(self):
        """
        调度请求
        :return:
        """
        while not self.queue.empty():
            weixin_request = self.queue.pop()
            callback = weixin_request.callback
            # print(callback)
            # print("Schedule", weixin_request.url)
            response = self.request(weixin_request=weixin_request)
            print(response.text)
            if response and response.status_code in VALID_STATUSES:
                results = list(callback(response))
                if results:
                    for result in results:
                        print("New Result", type(result))
                        if isinstance(result, WeixinRequest):
                            self.queue.add(weixin_request)
                        if isinstance(result, dict):
                            self.mysql.insert("weixin", result)
                else:
                    self.error(weixin_request)
            else:
                self.error(weixin_request=weixin_request)

    def run(self):
        """
        入口
        :return:
        """
        self.start()
        self.schedule()


if __name__ == "__main__":
    spider = Spider()
    spider.run()