"""
Unit tests for pageparsing
"""
import os
from cStringIO import StringIO                                                                                                    
from gzip import GzipFile

from twisted.trial.unittest import TestCase, SkipTest
from scrapy.utils.python import str_to_unicode
from scrapy.utils.py26 import json

from scrapy.contrib.ibl.htmlpage import HtmlPage
from scrapy.tests.test_contrib_ibl import path

try:
    import numpy
except ImportError:
    numpy = None

if numpy:
    from scrapy.contrib.ibl.extraction.pageparsing import (
        InstanceLearningParser, TemplatePageParser, ExtractionPageParser)
    from scrapy.contrib.ibl.extraction.pageobjects import TokenDict, TokenType


SIMPLE_PAGE = u"""
<html> <p some-attr="foo">this is a test</p> </html>
"""

LABELLED_PAGE1 = u"""
<html>
<h1 data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;name&quot;}}">Some Product</h1>
<p> some stuff</p>
<p data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">
This is such a nice item<br/>
Everybody likes it.
</p>
<p data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;common_prefix&quot;: true, &quot;annotations&quot;: {&quot;content&quot;: &quot;price&quot;}}"/>
\xa310.00
<br/>
<p data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;short_description&quot;}}">
Old fashioned product
<p data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;short_description&quot;}}">
For exigent individuals
<p>click here for other items</p>
</html>
"""

BROKEN_PAGE = u"""
<html> <p class="ruleb"align="center">html parser cannot parse this</p></html>
"""

LABELLED_PAGE2 = u"""
<html><body>
<h1>A product</h1>
<div data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">
<p>A very nice product for all intelligent people</p>
<div data-scrapy-ignore="true">
<img scr="image.jpg" /><br/><a link="back.html">Click here to go back</a>
</div>
</div>
<div data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;price&quot;}}">
\xa310.00<p data-scrapy-ignore="true"> 13 <br></p>
</div>
<table data-scrapy-ignore="true">
<tr><td data-scrapy-ignore="true"></td></tr>
<tr></tr>
</table>
<img data-scrapy-ignore="true" src="image2.jpg"> 
<img data-scrapy-ignore="true" src="image3.jpg" />
<img data-scrapy-ignore-beneath="true" src="image2.jpg">
<img data-scrapy-ignore-beneath="true" src="image3.jpg" />
</body></html>

"""

LABELLED_PAGE3 = u"""
<html><body>
<h1>A product</h1>
<div data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">
<p>A very nice product for all intelligent people</p>
<div data-scrapy-ignore="true">
<img scr="image.jpg" /><br/><a link="back.html">Click here to go back</a>
</div>
</div>
<div data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">
\xa310.00<p data-scrapy-ignore="true"> 13 <br></p>
<table><tr>
<td>Description 1</td>
<td data-scrapy-ignore-beneath="true">Description 2</td>
<td>Description 3</td>
<td>Description 4</td>
</tr></table>
</div>
</body></html>
"""

LABELLED_PAGE4 = u"""
<html><body>
<h1>A product</h1>
<div>
<p>A very nice product for all intelligent people</p>
<div>
<img scr="image.jpg" /><br/><a link="back.html">Click here to go back</a>
</div>
</div>
<div data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">
\xa310.00<p data-scrapy-ignore="true"> 13 <br></p>
<table><tr>
<td>Description 1</td>
<td data-scrapy-ignore-beneath="true">Description 2</td>
<td>Description 3</td>
<td data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;price&quot;}}">
Price \xa310.00</td>
</tr></table>
</div>
</body></html>
"""

LABELLED_PAGE5 = u"""
<html><body>
<ul data-scrapy-replacement='select'>
<li data-scrapy-replacement='option'>Option A</li>
<li>Option I</li>
<li data-scrapy-replacement='option'>Option B</li>
</ul>
</body></html>
"""

LABELLED_PAGE6 = u"""
<html><body>
Text A
<p><ins data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;generated&quot;: true, &quot;annotations&quot;: {&quot;content&quot;: &quot;price&quot;}}">
65.00</ins>pounds</p>
<p>Description: <ins data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;generated&quot;: true, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">
Text B</ins></p>
Text C
</body></html>
"""

LABELLED_PAGE7 = u"""
<html><body>
<div data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">
<ins data-scrapy-ignore="true" data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;generated&quot;: true, &quot;annotations&quot;: {&quot;content&quot;: &quot;site_id&quot;}}">Item Id</ins>
Description
</div>
</body></html>
"""

LABELLED_PAGE8 = u"""
<html><body>
<div data-scrapy-annotate="{&quot;required&quot;: [&quot;description&quot;], &quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">
<ins data-scrapy-ignore="true" data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;generated&quot;: true, &quot;annotations&quot;: {&quot;content&quot;: &quot;site_id&quot;}}">Item Id</ins>
Description
</div>
</body></html>
"""

def _parse_page(parser_class, pagetext):
    htmlpage = HtmlPage(None, {}, pagetext)
    parser = parser_class(TokenDict())
    parser.feed(htmlpage)
    return parser

def _tags(pp, predicate):
    return [pp.token_dict.token_string(s) for s in pp.token_list \
            if predicate(s)]

class TestPageParsing(TestCase):

    def setUp(self):
        if not numpy:
            raise SkipTest("numpy not available")

    def test_instance_parsing(self):
        pp = _parse_page(InstanceLearningParser, SIMPLE_PAGE)
        # all tags
        self.assertEqual(_tags(pp, bool), ['<html>', '<p>', '</p>', '</html>'])

        # open/closing tag handling
        openp = lambda x: pp.token_dict.token_type(x) == TokenType.OPEN_TAG
        self.assertEqual(_tags(pp, openp), ['<html>', '<p>'])
        closep = lambda x: pp.token_dict.token_type(x) == TokenType.CLOSE_TAG
        self.assertEqual(_tags(pp, closep), ['</p>', '</html>'])
    
    def _validate_annotation(self, parser, lable_region, name, start_tag, end_tag):
        assert lable_region.surrounds_attribute == name
        start_token = parser.token_list[lable_region.start_index]
        assert parser.token_dict.token_string(start_token) == start_tag
        end_token = parser.token_list[lable_region.end_index]
        assert parser.token_dict.token_string(end_token) == end_tag

    def test_template_parsing(self):
        lp = _parse_page(TemplatePageParser, LABELLED_PAGE1)
        self.assertEqual(len(lp.annotations), 5)
        self._validate_annotation(lp, lp.annotations[0], 
                'name', '<h1>', '</h1>')
        self.assertEqual(lp.annotations[0].match_common_prefix, False)
        self._validate_annotation(lp, lp.annotations[1], 
                'description', '<p>', '</p>')
        self.assertEqual(lp.annotations[1].match_common_prefix, False)
        self._validate_annotation(lp, lp.annotations[2],
                'price', '<p/>', '<p>')
        self.assertEqual(lp.annotations[2].match_common_prefix, True)
        self._validate_annotation(lp, lp.annotations[3],
                'short_description', '<p>', '<p>')
        self.assertEqual(lp.annotations[3].match_common_prefix, False)
        self._validate_annotation(lp, lp.annotations[4],
                'short_description', '<p>', '<p>')
        self.assertEqual(lp.annotations[4].match_common_prefix, False)
        
        # all tags were closed
        self.assertEqual(len(lp.labelled_tag_stacks), 0)
    
    def test_extraction_page_parsing(self):
        epp = _parse_page(ExtractionPageParser, SIMPLE_PAGE)
        ep = epp.to_extraction_page()
        assert len(ep.page_tokens) == 4
        assert ep.token_html(0) == '<html>'
        assert ep.token_html(1) == '<p some-attr="foo">'
        
        assert ep.html_between_tokens(1, 2) == 'this is a test'
        assert ep.html_between_tokens(1, 3) == 'this is a test</p> '

    def test_invalid_html(self):
        p = _parse_page(InstanceLearningParser, BROKEN_PAGE)
        assert p
        
    def test_ignore_region(self):
        """Test ignored regions"""
        p = _parse_page(TemplatePageParser, LABELLED_PAGE2)
        self.assertEqual(p.ignored_regions, [(7,12),(15,17),(19,26),(21,22),(27,28),(28,29),(29,None),(30,None)])
        self.assertEqual(len(p.ignored_tag_stacks), 0)

    def test_ignore_regions2(self):
        """Test ignore-beneath regions"""
        p = _parse_page(TemplatePageParser, LABELLED_PAGE3)
        self.assertEqual(p.ignored_regions, [(7,12),(15,17),(22,None)])
        self.assertEqual(len(p.ignored_tag_stacks), 0)
        
    def test_ignore_regions3(self):
        """Test ignore-beneath with annotation inside region"""
        p = _parse_page(TemplatePageParser, LABELLED_PAGE4)
        self.assertEqual(p.ignored_regions, [(15,17),(22,None)])
        self.assertEqual(len(p.ignored_tag_stacks), 0)
        
    def test_replacement(self):
        """Test parsing of replacement tags"""
        p = _parse_page(TemplatePageParser, LABELLED_PAGE5)
        self.assertEqual(_tags(p, bool), ['<html>', '<body>', '<select>', '<option>',
                    '</option>', '<li>', '</li>', '<option>', '</option>', '</select>', '</body>', '</html>'])
        
    def test_partial(self):
        """Test partial annotation parsing"""
        p = _parse_page(TemplatePageParser, LABELLED_PAGE6)
        text = p.annotations[0].annotation_text
        self.assertEqual(text.start_text, '')
        self.assertEqual(text.follow_text, 'pounds')
        text = p.annotations[1].annotation_text
        self.assertEqual(text.start_text, "Description: ")
        self.assertEqual(text.follow_text, '')
        
    def test_ignored_partial(self):
        """Test ignored region declared on partial annotation"""
        p = _parse_page(TemplatePageParser, LABELLED_PAGE7)
        self.assertEqual(p.ignored_regions, [(2, 3)])
        
    def test_extra_required(self):
        """Test parsing of extra required attributes"""
        p = _parse_page(TemplatePageParser, LABELLED_PAGE8)
        self.assertEqual(p.extra_required_attrs, ["description"])
        
    def test_site_pages(self):
        """
        Tests from real pages. More reliable and easy to build for more complicated structures
        """
        samples_file = open(os.path.join(path, "samples_pageparsing.json.gz"), "rb")
        samples = []
        for line in GzipFile(fileobj=StringIO(samples_file.read())).readlines():
            samples.append(json.loads(line))
        for sample in samples:
            source = sample["annotated"]
            annotations = sample["annotations"]
            template = HtmlPage(body=str_to_unicode(source))
            parser = TemplatePageParser(TokenDict())
            parser.feed(template)
            for annotation in parser.annotations:
                test_annotation = annotations.pop(0)
                for s in annotation.__slots__:
                    if s == "tag_attributes":
                        for pair in getattr(annotation, s):
                            self.assertEqual(list(pair), test_annotation[s].pop(0))
                    else:
                        self.assertEqual(getattr(annotation, s), test_annotation[s])
            self.assertEqual(annotations, [])
