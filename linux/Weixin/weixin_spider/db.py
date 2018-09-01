from redis import StrictRedis
from weixin_spider.config import *
from pickle import loads, dumps
from weixin_spider.request import WeixinRequest


class RedisQueue():
    def __init__(self):

        self.db = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)


    def add(self, request):
        if isinstance(request, WeixinRequest):
            return self.db.rpush(REDIS_KEY, dumps(request))
        return False


    def pop(self):
        if self.db.llen(REDIS_KEY):
            return loads(self.db.lpop(REDIS_KEY))
        return False


    def clear(self):
        self.db.delete(REDIS_KEY)


    def empty(self):
        return self.db.llen(REDIS_KEY) == 0


if __name__ == '__main__':
    db = RedisQueue()
    start_url = 'https://www.baidu.com'
    weixin_request = WeixinRequest(url=start_url, callback='hello', need_proxy=True)
    db.add(weixin_request)
    request = db.pop()
    db.clear()
    print(request)
    print(request.callback, request.need_proxy)