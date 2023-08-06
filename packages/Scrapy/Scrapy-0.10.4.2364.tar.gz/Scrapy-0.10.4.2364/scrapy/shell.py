"""
Scrapy Shell

See documentation in docs/topics/shell.rst
"""

import signal

from twisted.internet import reactor, threads
from twisted.python.failure import Failure

from scrapy import log
from scrapy.item import BaseItem
from scrapy.spider import BaseSpider
from scrapy.selector import XPathSelector, XmlXPathSelector, HtmlXPathSelector
from scrapy.utils.spider import create_spider_for_request
from scrapy.utils.misc import load_object
from scrapy.utils.response import open_in_browser
from scrapy.utils.url import any_to_uri
from scrapy.utils.console import start_python_console
from scrapy.conf import settings, Settings
from scrapy.http import Request, Response, TextResponse

class Shell(object):

    relevant_classes = (BaseSpider, Request, Response, BaseItem, \
        XPathSelector, Settings)

    def __init__(self, crawler, update_vars=None, inthread=False):
        self.crawler = crawler
        self.vars = {}
        self.update_vars = update_vars or (lambda x: None)
        self.item_class = load_object(settings['DEFAULT_ITEM_CLASS'])
        self.inthread = inthread

    def start(self, *a, **kw):
        # disable accidental Ctrl-C key press from shutting down the engine
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        if self.inthread:
            return threads.deferToThread(self._start, *a, **kw)
        else:
            self._start(*a, **kw)

    def _start(self, url=None, request=None, response=None, spider=None):
        if url:
            self.fetch(url, spider)
        elif request:
            self.fetch(request, spider)
        elif response:
            request = response.request
            self.populate_vars(request.url, response, request, spider)
        start_python_console(self.vars)

    def _schedule(self, request, spider):
        if spider is None:
            spider = create_spider_for_request(self.crawler.spiders, request, \
                BaseSpider('default'), log_multiple=True)
        self.crawler.engine.open_spider(spider)
        return self.crawler.engine.schedule(request, spider)

    def fetch(self, request_or_url, spider=None):
        if isinstance(request_or_url, Request):
            request = request_or_url
            url = request.url
        else:
            url = any_to_uri(request_or_url)
            request = Request(url, dont_filter=True)
        response = None
        try:
            response = threads.blockingCallFromThread(reactor, \
                self._schedule, request, spider)
        except:
            log.err(Failure(), "Error fetching response", spider=spider)
        self.populate_vars(url, response, request, spider)

    def populate_vars(self, url=None, response=None, request=None, spider=None):
        item = self.item_class()
        self.vars['item'] = item
        self.vars['settings'] = settings
        if url:
            if isinstance(response, TextResponse):
                self.vars['xxs'] = XmlXPathSelector(response)
                self.vars['hxs'] = HtmlXPathSelector(response)
            self.vars['response'] = response
            self.vars['request'] = request
            self.vars['spider'] = spider
        if self.inthread:
            self.vars['fetch'] = self.fetch
        self.vars['view'] = open_in_browser
        self.vars['shelp'] = self.print_help
        self.update_vars(self.vars)
        self.print_help()

    def print_help(self):
        self.p("Available Scrapy objects:")
        for k, v in sorted(self.vars.iteritems()):
            if self._is_relevant(v):
                self.p("  %-10s %s" % (k, v))
        self.p("Useful shortcuts:")
        self.p("  shelp()           Shell help (print this help)")
        if self.inthread:
            self.p("  fetch(req_or_url) Fetch request (or URL) and update local objects")
        self.p("  view(response)    View response in a browser")

    def p(self, line=''):
        print "[s] %s" % line

    def _is_relevant(self, value):
        return isinstance(value, self.relevant_classes)


def inspect_response(response, spider=None):
    """Open a shell to inspect the given response"""
    from scrapy.project import crawler
    Shell(crawler).start(response=response, spider=spider)
