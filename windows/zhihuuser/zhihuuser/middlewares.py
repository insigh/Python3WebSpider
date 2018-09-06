# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import requests
from requests.exceptions import ConnectionError
from scrapy.exceptions import IgnoreRequest

from scrapy import signals


class ZhihuSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    # def _get_random_proxy(self):
    #     try:
    #         response = requests.get("http://10.77.40.60:5555/random")
    #         self.logger.debug('----------------------------------------------------------------------------')
    #         if response.status_code == 200:
    #             return json.loads(response.text)
    #     except ConnectionError:
    #         self.logger.debug("-----------------------------No Proxy---------------------------")
    #         return None
    #
    # def process_request(self, request, spider):
    #     print(request.proxy_)
    #     proxy = self._get_random_proxy()
    #     proxies = {
    #         'http': 'http://' + proxy,
    #         'https': 'https://' + proxy
    #     }
    #     if proxy:
    #         request.proxy_ = proxies
    #         self.logger.debug('Using Proxies ' + json.dumps(proxies))
    #     else:
    #         self.logger.debug('No Valid Proxies')


class zhihuProxyMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def process_request(self, request, spider):
        # if 'start' in request.meta.keys() and request.meta['start'] == 'True':
        #     pro_addr = requests.get('http://10.77.40.60:5555/random').text
        #     request.meta['proxy'] = 'http://' + pro_addr
        #     request.meta['start'] = 'False'
        #     return request
        # else:
        pro_addr = requests.get('http://10.77.40.60:5555/random').text
        request.meta['proxy'] = 'http://' + pro_addr
        return None

    # def process_exception(self, request, exception, spider):
    #     self.logger.debug('Failed to request url %s with proxy %s with exception %s' % (
    #     request.url, request.meta['proxy'], str(exception)))
    #     # retry again.
    #     return request

    def process_response(self, request, response, spider):
        if response.status in [200]:
            return response
        elif response.status in [500, 503, 504, 400, 403, 404, 408, 301, 302, 303, 406, 407]:
            pro_addr = requests.get('http://10.77.40.60:5555/random').text
            request.meta['proxy'] = 'http://' + pro_addr
            self.logger.debug("Using Proxy: " + pro_addr)
            return request
