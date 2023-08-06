from unittest import TestCase

from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware


class UserAgentMiddlewareTest(TestCase):

    def setUp(self):
        self.spider = BaseSpider('foo')
        self.mw = UserAgentMiddleware()

    def tearDown(self):
        del self.mw

    def test_default_agent(self):
        self.mw.default_useragent = 'default_useragent'
        req = Request('http://scrapytest.org/')
        assert self.mw.process_request(req, self.spider) is None
        self.assertEquals(req.headers['User-Agent'], 'default_useragent')

        # None or not present user_agent attribute is the same
        self.spider.user_agent = None
        req = Request('http://scrapytest.org/')
        assert self.mw.process_request(req, self.spider) is None
        self.assertEquals(req.headers['User-Agent'], 'default_useragent')

    def test_spider_agent(self):
        self.mw.default_useragent = 'default_useragent'
        self.spider.user_agent = 'spider_useragent'
        req = Request('http://scrapytest.org/')
        assert self.mw.process_request(req, self.spider) is None
        self.assertEquals(req.headers['User-Agent'], 'spider_useragent')

    def test_header_agent(self):
        self.mw.default_useragent = 'default_useragent'
        self.spider.user_agent = 'spider_useragent'
        req = Request('http://scrapytest.org/', headers={'User-Agent': 'header_useragent'})
        assert self.mw.process_request(req, self.spider) is None
        self.assertEquals(req.headers['User-Agent'], 'header_useragent')

    def test_no_agent(self):
        self.mw.default_useragent = None
        self.spider.user_agent = None
        req = Request('http://scrapytest.org/')
        assert self.mw.process_request(req, self.spider) is None
        assert 'User-Agent' not in req.headers

