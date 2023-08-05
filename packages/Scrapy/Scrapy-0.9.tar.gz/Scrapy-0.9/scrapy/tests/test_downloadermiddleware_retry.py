import unittest

from twisted.internet.error import TimeoutError as ServerTimeoutError, DNSLookupError, \
                                   ConnectionRefusedError, ConnectionDone, ConnectError, \
                                   ConnectionLost

from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from scrapy.spider import BaseSpider
from scrapy.http import Request, Response

class RetryTest(unittest.TestCase):
    def setUp(self):
        self.spider = BaseSpider('foo')
        self.mw = RetryMiddleware()
        self.mw.max_retry_times = 2

    def test_priority_adjust(self):
        req = Request('http://www.scrapytest.org/503')
        rsp = Response('http://www.scrapytest.org/503', body='', status=503)
        req2 = self.mw.process_response(req, rsp, self.spider)
        assert req2.priority < req.priority

    def test_404(self):
        req = Request('http://www.scrapytest.org/404')
        rsp = Response('http://www.scrapytest.org/404', body='', status=404)

        # dont retry 404s
        assert self.mw.process_response(req, rsp, self.spider) is rsp

    def test_503(self):
        req = Request('http://www.scrapytest.org/503')
        rsp = Response('http://www.scrapytest.org/503', body='', status=503)

        # first retry
        req = self.mw.process_response(req, rsp, self.spider)
        assert isinstance(req, Request)
        self.assertEqual(req.meta['retry_times'], 1)

        # second retry
        req = self.mw.process_response(req, rsp, self.spider)
        assert isinstance(req, Request)
        self.assertEqual(req.meta['retry_times'], 2)

        # discard it
        assert self.mw.process_response(req, rsp, self.spider) is rsp

    def test_twistederrors(self):
        for exc in (ServerTimeoutError, DNSLookupError, ConnectionRefusedError, ConnectionDone, ConnectError, ConnectionLost):
            req = Request('http://www.scrapytest.org/%s' % exc.__name__)
            self._test_retry_exception(req, exc())

    def _test_retry_exception(self, req, exception):
        # first retry
        req = self.mw.process_exception(req, exception, self.spider)
        assert isinstance(req, Request)
        self.assertEqual(req.meta['retry_times'], 1)

        # second retry
        req = self.mw.process_exception(req, exception, self.spider)
        assert isinstance(req, Request)
        self.assertEqual(req.meta['retry_times'], 2)

        # discard it
        req = self.mw.process_exception(req, exception, self.spider)
        self.assertEqual(req, None)


if __name__ == "__main__":
    unittest.main()
