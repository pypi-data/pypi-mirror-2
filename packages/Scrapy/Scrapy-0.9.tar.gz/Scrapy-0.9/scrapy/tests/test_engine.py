"""
Scrapy engine tests
"""

import sys, os, re, urlparse, unittest

from twisted.internet import reactor
from twisted.web import server, resource, static, util

from scrapy.core import signals
from scrapy.core.manager import scrapymanager
from scrapy.xlib.pydispatch import dispatcher
from scrapy.tests import tests_datadir
from scrapy.spider import BaseSpider
from scrapy.item import Item, Field
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request

class TestItem(Item):
    name = Field()
    url = Field()
    price = Field()

class TestSpider(BaseSpider):
    name = "scrapytest.org"
    allowed_domains = ["scrapytest.org", "localhost"]
    start_urls = ['http://localhost']

    itemurl_re = re.compile("item\d+.html")
    name_re = re.compile("<h1>(.*?)</h1>", re.M)
    price_re = re.compile(">Price: \$(.*?)<", re.M)

    def parse(self, response):
        xlink = SgmlLinkExtractor()
        itemre = re.compile(self.itemurl_re)
        for link in xlink.extract_links(response):
            if itemre.search(link.url):
                yield Request(url=link.url, callback=self.parse_item)

    def parse_item(self, response):
        item = TestItem()
        m = self.name_re.search(response.body)
        if m:
            item['name'] = m.group(1)
        item['url'] = response.url
        m = self.price_re.search(response.body)
        if m:
            item['price'] = m.group(1)
        return item

#class TestResource(resource.Resource):
#    isLeaf = True
#
#    def render_GET(self, request):
#        return "hello world!"

def start_test_site():
    root_dir = os.path.join(tests_datadir, "test_site")
    r = static.File(root_dir)
#    r.putChild("test", TestResource())
    r.putChild("redirect", util.Redirect("/redirected"))
    r.putChild("redirected", static.Data("Redirected here", "text/plain"))

    port = reactor.listenTCP(0, server.Site(r), interface="127.0.0.1")
    return port


class CrawlingSession(object):

    def __init__(self):
        self.name = 'scrapytest.org'
        self.spider = None
        self.respplug = []
        self.reqplug = []
        self.itemresp = []
        self.signals_catched = {}
        self.wasrun = False

    def run(self):
        self.port = start_test_site()
        self.portno = self.port.getHost().port

        self.spider = TestSpider()
        if self.spider:
            self.spider.start_urls = [
                self.geturl("/"),
                self.geturl("/redirect"),
                ]

            dispatcher.connect(self.record_signal, signals.engine_started)
            dispatcher.connect(self.record_signal, signals.engine_stopped)
            dispatcher.connect(self.record_signal, signals.spider_opened)
            dispatcher.connect(self.record_signal, signals.spider_idle)
            dispatcher.connect(self.record_signal, signals.spider_closed)
            dispatcher.connect(self.item_scraped, signals.item_scraped)
            dispatcher.connect(self.request_received, signals.request_received)
            dispatcher.connect(self.response_downloaded, signals.response_downloaded)

            scrapymanager.configure()
            scrapymanager.queue.append_spider(self.spider)
            scrapymanager.start()
            self.port.stopListening()
            self.wasrun = True

    def geturl(self, path):
        return "http://localhost:%s%s" % (self.portno, path)

    def getpath(self, url):
        u = urlparse.urlparse(url)
        return u.path

    def item_scraped(self, item, spider, response):
        self.itemresp.append((item, response))

    def request_received(self, request, spider):
        self.reqplug.append((request, spider))

    def response_downloaded(self, response, spider):
        self.respplug.append((response, spider))

    def record_signal(self, *args, **kwargs):
        """Record a signal and its parameters"""
        signalargs = kwargs.copy()
        sig = signalargs.pop('signal')
        signalargs.pop('sender', None)
        self.signals_catched[sig] = signalargs

session = CrawlingSession()


class EngineTest(unittest.TestCase):

    def setUp(self):
        if not session.wasrun:
            session.run()

    def test_spider_locator(self):
        """
        Check the spider is loaded and located properly via the SpiderLocator
        """
        assert session.spider is not None
        self.assertEqual(session.spider.name, session.name)

    def test_visited_urls(self):
        """
        Make sure certain URls were actually visited
        """
        # expected urls that should be visited
        must_be_visited = ["/", "/redirect", "/redirected", 
                           "/item1.html", "/item2.html", "/item999.html"]

        urls_visited = set([rp[0].url for rp in session.respplug])
        urls_expected = set([session.geturl(p) for p in must_be_visited])
        assert urls_expected <= urls_visited, "URLs not visited: %s" % list(urls_expected - urls_visited)

    def test_requests_received(self):
        """
        Check requests received
        """
        # 3 requests should be received from the spider. start_urls and redirects don't count
        self.assertEqual(3, len(session.reqplug))

        paths_expected = ['/item999.html', '/item2.html', '/item1.html']

        urls_requested = set([rq[0].url for rq in session.reqplug])
        urls_expected = set([session.geturl(p) for p in paths_expected])
        assert urls_expected <= urls_requested

    def test_responses_downloaded(self):
        """
        Check responses downloaded
        """
        # response tests
        self.assertEqual(6, len(session.respplug))

        for response, spider in session.respplug:
            if session.getpath(response.url) == '/item999.html':
                self.assertEqual(404, response.status)
            if session.getpath(response.url) == '/redirect':
                self.assertEqual(302, response.status)

    def test_item_data(self):
        """
        Check item data
        """
        # item tests
        self.assertEqual(2, len(session.itemresp))
        for item, response in session.itemresp:
            self.assertEqual(item['url'], response.url)
            if 'item1.html' in item['url']:
                self.assertEqual('Item 1 name', item['name'])
                self.assertEqual('100', item['price'])
            if 'item2.html' in item['url']:
                self.assertEqual('Item 2 name', item['name'])
                self.assertEqual('200', item['price'])

    def test_signals(self):
        """
        Check signals were sent properly
        """
        from scrapy.core import signals

        assert signals.engine_started in session.signals_catched
        assert signals.engine_stopped in session.signals_catched
        assert signals.spider_opened in session.signals_catched
        assert signals.spider_idle in session.signals_catched
        assert signals.spider_closed in session.signals_catched

        self.assertEqual({'spider': session.spider},
                         session.signals_catched[signals.spider_opened])
        self.assertEqual({'spider': session.spider},
                         session.signals_catched[signals.spider_idle])
        self.assertEqual({'spider': session.spider, 'reason': 'finished'},
                         session.signals_catched[signals.spider_closed])

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        port = start_test_site()
        print "Test server running at http://localhost:%d/ - hit Ctrl-C to finish." % port.getHost().port
        reactor.run()
    else:
        unittest.main()
