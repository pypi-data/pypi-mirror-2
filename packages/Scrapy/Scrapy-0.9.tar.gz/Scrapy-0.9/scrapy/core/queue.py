from twisted.internet import defer

from scrapy.http import Request
from scrapy.utils.misc import arg_to_iter
from scrapy import log
from scrapy.spider import spiders


class ExecutionQueue(object):

    polling_delay = 5

    def __init__(self, _spiders=spiders):
        self.spider_requests = []
        self._spiders = _spiders

    def _append_next(self):
        """Called when there are no more items left in self.spider_requests.
        This method is meant to be overriden in subclasses to add new (spider,
        requests) tuples to self.spider_requests. It can return a Deferred.
        """
        pass

    def get_next(self):
        """Return a tuple (spider, requests) containing a list of Requests and
        the Spider which will be used to crawl those Requests. If there aren't
        any more spiders to crawl it must return (None, []).

        This method can return a deferred.
        """
        if self.spider_requests:
            return self._get_next_now()
        d = defer.maybeDeferred(self._append_next)
        d.addCallback(lambda _: self._get_next_now())
        return d

    def _get_next_now(self):
        try:
            return self.spider_requests.pop(0)
        except IndexError:
            return (None, [])

    def is_finished(self):
        """Return True if the queue is empty and there won't be any more
        spiders to crawl (this is for one-shot runs). If it returns ``False``
        Scrapy will keep polling this queue for new requests to scrape
        """
        return not bool(self.spider_requests)

    def append_spider(self, spider):
        """Append a Spider to crawl"""
        requests = spider.start_requests()
        self.spider_requests.append((spider, requests))

    def append_request(self, request, spider=None, **kwargs):
        if spider is None:
            spider = self._spiders.create_for_request(request, **kwargs)
        if spider:
            self.spider_requests.append((spider, [request]))

    def append_url(self, url, spider=None, **kwargs):
        """Append a URL to crawl with the given spider. If the spider is not
        given, a spider will be looked up based on the URL
        """
        if spider is None:
            spider = self._spiders.create_for_request(Request(url), **kwargs)
        if spider:
            requests = arg_to_iter(spider.make_requests_from_url(url))
            self.spider_requests.append((spider, requests))

    def append_spider_name(self, spider_name, **spider_kwargs):
        """Append a spider to crawl given its name and optional arguments,
        which are used to instantiate it. The SpiderManager is used to lookup
        the spider
        """
        try:
            spider = self._spiders.create(spider_name, **spider_kwargs)
        except KeyError:
            log.msg('Unable to find spider: %s' % spider_name, log.ERROR)
        else:
            self.append_spider(spider)


class KeepAliveExecutionQueue(ExecutionQueue):

    def is_finished(self):
        return False
