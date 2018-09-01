from weixin_spider.config import *
from requests import Request


class WeixinRequest(Request):
    def __init__(self, url, callback, method='GET', headers=None, need_proxy=False, fail_time=0, timeout=TIMEOUT):
        Request.__init__(self, method=method, url=url, headers=headers)
        self.callback = callback
        self.need_proxy = need_proxy
        self.fail_time = fail_time
        self.time_out = TIMEOUT

