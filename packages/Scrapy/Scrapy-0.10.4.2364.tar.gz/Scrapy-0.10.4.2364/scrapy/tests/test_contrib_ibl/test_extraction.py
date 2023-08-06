"""
tests for page parsing

Page parsing effectiveness is measured through the evaluation system. These
tests should focus on specific bits of functionality work correctly.
"""
from twisted.trial.unittest import TestCase, SkipTest
from scrapy.contrib.ibl.htmlpage import HtmlPage
from scrapy.contrib.ibl.descriptor import (FieldDescriptor as A, 
        ItemDescriptor)
from scrapy.contrib.ibl.extractors import (contains_any_numbers,
        image_url)

try:
    import numpy
except ImportError:
    numpy = None

if numpy:
    from scrapy.contrib.ibl.extraction import InstanceBasedLearningExtractor

# simple page with all features

ANNOTATED_PAGE1 = u"""
<html>
<h1>COMPANY - <ins 
    data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;generated&quot;: true, 
    &quot;annotations&quot;: {&quot;content&quot;: &quot;title&quot;}}" 
>Item Title</ins></h1>
<p>introduction</p>
<div>
<img data-scrapy-annotate="{&quot;variant&quot;: 0, 
    &quot;annotations&quot;: {&quot;src&quot;: &quot;image_url&quot;}}"
    src="img.jpg"/>
<p data-scrapy-annotate="{&quot;variant&quot;: 0, 
    &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">
This is such a nice item<br/> Everybody likes it.
</p>
<br/>
</div>
<p>click here for other items</p>
</html>
"""

EXTRACT_PAGE1 = u"""
<html>
<h1>Scrapy - Nice Product</h1>
<p>introduction</p>
<div>
<img src="nice_product.jpg" alt="a nice product image"/>
<p>wonderful product</p>
<br/>
</div>
</html>
"""

# single tag with multiple items extracted
ANNOTATED_PAGE2 = u"""
<a href="http://example.com/xxx" title="xxx"
    data-scrapy-annotate="{&quot;variant&quot;: 0, 
    &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;, 
        &quot;href&quot;: &quot;image_url&quot;, &quot;title&quot;: &quot;name&quot;}}"
>xx</a>
xxx
</a>
"""
EXTRACT_PAGE2 = u"""<a href='http://example.com/product1.jpg' 
    title="product 1">product 1 is great</a>"""

# matching must match the second attribute in order to find the first
ANNOTATED_PAGE3 = u"""
<p data-scrapy-annotate="{&quot;variant&quot;: 0, 
    &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">xx</p>
<div data-scrapy-annotate="{&quot;variant&quot;: 0, 
    &quot;annotations&quot;: {&quot;content&quot;: &quot;delivery&quot;}}">xx</div>
"""
EXTRACT_PAGE3 = u"""
<p>description</p>
<div>delivery</div>
<p>this is not the description</p>
"""

# test inferring repeated elements
ANNOTATED_PAGE4 = u"""
<ul>
<li data-scrapy-annotate="{&quot;variant&quot;: 0, 
    &quot;annotations&quot;: {&quot;content&quot;: &quot;features&quot;}}">feature1</li>
<li data-scrapy-annotate="{&quot;variant&quot;: 0, 
    &quot;annotations&quot;: {&quot;content&quot;: &quot;features&quot;}}">feature2</li>
</ul>
"""

EXTRACT_PAGE4 = u"""
<ul>
<li>feature1</li> ignore this
<li>feature2</li>
<li>feature3</li>
</ul>
"""

# test variant handling with identical repeated variant
ANNOTATED_PAGE5 =  u"""
<p data-scrapy-annotate="{&quot;annotations&quot;:
    {&quot;content&quot;: &quot;description&quot;}}">description</p>
<table>
<tr>
<td data-scrapy-annotate="{&quot;variant&quot;: 1, &quot;annotations&quot;: 
    {&quot;content&quot;: &quot;colour&quot;}}" >colour 1</td>
<td data-scrapy-annotate="{&quot;variant&quot;: 1, &quot;annotations&quot;: 
    {&quot;content&quot;: &quot;price&quot;}}" >price 1</td>
</tr>
<tr>
<td data-scrapy-annotate="{&quot;variant&quot;: 2, &quot;annotations&quot;: 
    {&quot;content&quot;: &quot;colour&quot;}}" >colour 2</td>
<td data-scrapy-annotate="{&quot;variant&quot;: 2, &quot;annotations&quot;: 
    {&quot;content&quot;: &quot;price&quot;}}" >price 2</td>
</tr>
</table>
"""

EXTRACT_PAGE5 = u"""
<p>description</p>
<table>
<tr>
<td>colour 1</td>
<td>price 1</td>
</tr>
<tr>
<td>colour 2</td>
<td>price 2</td>
</tr>
<tr>
<td>colour 3</td>
<td>price 3</td>
</tr>
</table>
"""

# test variant handling with irregular structure and some non-variant
# attributes
ANNOTATED_PAGE6 =  u"""
<p data-scrapy-annotate="{&quot;annotations&quot;:
    {&quot;content&quot;: &quot;description&quot;}}">description</p>
<p data-scrapy-annotate="{&quot;variant&quot;: 1, &quot;annotations&quot;: 
    {&quot;content&quot;: &quot;name&quot;}}">name 1</p>
<div data-scrapy-annotate="{&quot;variant&quot;: 3, &quot;annotations&quot;: 
    {&quot;content&quot;: &quot;name&quot;}}" >name 3</div>
<p data-scrapy-annotate="{&quot;variant&quot;: 2, &quot;annotations&quot;: 
    {&quot;content&quot;: &quot;name&quot;}}" >name 2</p>
"""
EXTRACT_PAGE6 =  u"""
<p>description</p>
<p>name 1</p>
<div>name 3</div>
<p>name 2</p>
"""

# test repeating variants at the table column level
ANNOTATED_PAGE7 =  u"""
<table>
<tr>
<td data-scrapy-annotate="{&quot;variant&quot;: 1, &quot;annotations&quot;: 
    {&quot;content&quot;: &quot;colour&quot;}}" >colour 1</td>
<td data-scrapy-annotate="{&quot;variant&quot;: 2, &quot;annotations&quot;: 
    {&quot;content&quot;: &quot;colour&quot;}}" >colour 2</td>
</tr>
<tr>
<td data-scrapy-annotate="{&quot;variant&quot;: 2, &quot;annotations&quot;: 
    {&quot;content&quot;: &quot;price&quot;}}" >price 1</td>
<td data-scrapy-annotate="{&quot;variant&quot;: 2, &quot;annotations&quot;: 
    {&quot;content&quot;: &quot;price&quot;}}" >price 2</td>
</tr>
</table>
"""

EXTRACT_PAGE7 = u"""
<table>
<tr>
<td>colour 1</td>
<td>colour 2</td>
<td>colour 3</td>
</tr>
<tr>
<td>price 1</td>
<td>price 2</td>
<td>price 3</td>
</tr>
</table>
"""

ANNOTATED_PAGE8 = u"""
<html><body>
<h1>A product</h1>
<div data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">
<p>XXXX XXXX xxxxx</p>
<div data-scrapy-ignore="true">
<img scr="image.jpg" /><br/><a link="back.html">Click here to go back</a>
</div>
</div>
<div data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;price&quot;}}">
10.00<p data-scrapy-ignore="true"> 13</p>
</div>
</body></html>
"""

EXTRACT_PAGE8 = u"""
<html><body>
<h1>A product</h1>
<div>
<p>A very nice product for all intelligent people</p>
<div>
<img scr="image.jpg" /><br/><a link="back.html">Click here to go back</a>
</div>
</div>
<div>
12.00<p> ID 15</p>
(VAT exc.)</div>
</body></html>
"""

ANNOTATED_PAGE9 = ANNOTATED_PAGE8

EXTRACT_PAGE9 = u"""
<html><body>
<img src="logo.jpg" />
<h1>A product</h1>
<div>
<p>A very nice product for all intelligent people</p>
<div>
<img scr="image.jpg" /><br/><a link="back.html">Click here to go back</a>
</div>
</div>
<div>
12.00<p> ID 16</p>
(VAT exc.)</div>
</body></html>
"""

ANNOTATED_PAGE10a = u"""
<html><body>
<table><tbody>
<tr data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;common_prefix&quot;: true, &quot;annotations&quot;: {&quot;content&quot;: &quot;site_id&quot;}}">
<td>SKU</td><td>L345</td>
</tr>
<tr data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;common_prefix&quot;: true, &quot;annotations&quot;: {&quot;content&quot;: &quot;dimensions&quot;}}">
<td>Size</td><td>10cmx20cm</td>
</tr>
<tr data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;common_prefix&quot;: true, &quot;annotations&quot;: {&quot;content&quot;: &quot;price&quot;}}">
<td>Price</td><td>&pounds;99.00</td>
</tr>
</tbody></table>
</body></html>
"""

ANNOTATED_PAGE10b = u"""
<html><body>
<table><tbody>
<tr data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;common_prefix&quot;: true, &quot;annotations&quot;: {&quot;content&quot;: &quot;site_id&quot;}}">
<td>SKU</td><td>S220</td>
</tr>
<tr data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;common_prefix&quot;: true, &quot;annotations&quot;: {&quot;content&quot;: &quot;dimensions&quot;}}">
<td>Size</td><td>20cmx20cm</td>
</tr>
<tr data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;common_prefix&quot;: true, &quot;annotations&quot;: {&quot;content&quot;: &quot;price&quot;}}">
<td>Price</td><td>&pounds;85.00</td>
</tr>
</tbody></table>
</body></html>
"""

EXTRACT_PAGE10a = u"""
<html><body>
<table><tbody>
<tr>
<td>Offer</td><td>From $2500.00</td>
</tr>
<tr>
<td>Description</td><td>Electrorheological Cyborgs</td>
</tr>
<tr>
<td>Series:</td><td>T2000</td>
</tr>
</tbody></table>
</body></html>
"""

EXTRACT_PAGE10b = u"""
<html><body>
<table><tbody>
<tr>
<td>SKU</td><td>K80</td>
</tr>
<tr>
<td>Size</td><td>50cm</td>
</tr>
<tr>
<td>Price</td><td>&euros;85.00</td>
</tr>
</tbody></table>
</body></html>
"""

ANNOTATED_PAGE11 = u"""
<html><body>
<p data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">
<ins data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;generated&quot;: true,
    &quot;annotations&quot;: {&quot;content&quot;: &quot;name&quot;}}">
SL342
</ins>
<br/>
Nice product for ladies
<br/><ins data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;generated&quot;: true,
     &quot;annotations&quot;: {&quot;content&quot;: &quot;price&quot;}}">
&pounds;85.00
</ins>
</p>
<ins data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;generated&quot;: true,
     &quot;annotations&quot;: {&quot;content&quot;: &quot;price_before_discount&quot;}}">
&pounds;100.00
</ins>
</body></html>
"""

EXTRACT_PAGE11 = u"""
<html><body>
<p>
SL342
<br/>
Nice product for ladies
<br/>
&pounds;85.00
</p>
&pounds;100.00
</body></html>
"""

ANNOTATED_PAGE12 = u"""
<html><body>
<h1 data-scrapy-ignore-beneath="true">A product</h1>
<div data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">
<p>XXXX XXXX xxxxx</p>
<div data-scrapy-ignore-beneath="true">
<img scr="image.jpg" /><br/><a link="back.html">Click here to go back</a>
</div>
<div>
10.00<p> 13</p>
</div>
</div>
</body></html>
"""

EXTRACT_PAGE12a = u"""
<html><body>
<h1>A product</h1>
<div>
<p>A very nice product for all intelligent people</p>
<div>
<img scr="image.jpg" /><br/><a link="back.html">Click here to go back</a>
</div>
<div>
12.00<p> ID 15</p>
(VAT exc.)
</div></div>
</body></html>
"""

EXTRACT_PAGE12b = u"""
<html><body>
<h1>A product</h1>
<div>
<p>A very nice product for all intelligent people</p>
<div>
<img scr="image.jpg" /><br/><a link="back.html">Click here to go back</a>
</div>
<div>
12.00<p> ID 15</p>
(VAT exc.)
</div>
<ul>
Features
<li>Feature A</li>
<li>Feature B</li>
</ul>
</div>
</body></html>
"""

# Ex1: nested annotation with token sequence replica outside exterior annotation
# and a possible sequence pattern can be extracted only with
# correct handling of nested annotations
ANNOTATED_PAGE13a = u"""
<html><body>
<span>
<p data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">
<hr/>
<h3 data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;name&quot;}}">A product</h3>
<b data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;price&quot;}}">$50.00</b>
This product is excelent. Buy it!
</p>
</span>
<span>
<p>
<h3>See other products:</h3>
<b>Product b</b>
</p>
</span>
<hr/>
</body></html>
"""

EXTRACT_PAGE13a = u"""
<html><body>
<span>
<p>
<h3>A product</h3>
<b>$50.00</b>
This product is excelent. Buy it!
<hr/>
</p>
</span>
<span>
<p>
<h3>See other products:</h3>
<b>Product B</b>
</p>
</span>
</body></html>
"""

# Ex2: annotation with token sequence replica inside a previous nested annotation
# and a possible sequence pattern can be extracted only with
# correct handling of nested annotations
ANNOTATED_PAGE13b = u"""
<html><body>
<span>
<p data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">
<h3 data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;name&quot;}}">A product</h3>
<b>Previous price: $50.00</b>
This product is excelent. Buy it!
</p>
</span>
<span>
<p>
<h3>Save 10%!!</h3>
<b data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;price&quot;}}">$45.00</b>
</p>
</span>
</body></html>
"""

EXTRACT_PAGE13b = u"""
<html><body>
<span>
<p>
<h3>A product</h3>
<b>$50.00</b>
This product is excelent. Buy it!
</p>
</span>
<span>
<hr/>
<p>
<h3>Save 10%!!</h3>
<b>$45.00</b>
</p>
</span>
<hr/>
</body></html>
"""

ANNOTATED_PAGE14 = u"""
<html><body>
<b data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}"></b>
<p data-scrapy-ignore="true"></p>
</body></html>
"""

EXTRACT_PAGE14 = u"""
<html><body>
</body></html>
"""

ANNOTATED_PAGE15 = u"""
<html><body>
<div data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;short_description&quot;}}">Short
<div data-scrapy-ignore="true" data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;site_id&quot;}}">892342</div>
</div>
<hr/>
<p data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">Description
<b data-scrapy-ignore="true" data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;price&quot;}}">90.00</b>
</p>
</body></html>
"""

EXTRACT_PAGE15 = u"""
<html><body>
<hr/>
<p>Description
<b>80.00</b>
</p>
</body></html>
"""

ANNOTATED_PAGE16 = u"""
<html><body>
<div data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">
Description
<p data-scrapy-ignore="true" data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;name&quot;}}">
name</p>
<p data-scrapy-ignore="true" data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;price&quot;}}">
80.00</p>
</div>
</body></html>
"""

EXTRACT_PAGE16 = u"""
<html><body>
<p>product name</p>
<p>90.00</p>
</body></html>
"""

ANNOTATED_PAGE17 = u"""
<html><body>
<span>
<p data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">
This product is excelent. Buy it!
</p>
</span>
<table></table>
<img src="line.jpg" data-scrapy-ignore-beneath="true"/>
<span>
<h3>See other products:</h3>
<p>Product b
</p>
</span>
</body></html>
"""

EXTRACT_PAGE17 = u"""
<html><body>
<span>
<p>
This product is excelent. Buy it!
</p>
</span>
<img src="line.jpg"/>
<span>
<h3>See other products:</h3>
<p>Product B
</p>
</span>
</body></html>
"""

ANNOTATED_PAGE18 = u"""
<html><body>
<div data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">
<ins data-scrapy-ignore="true" data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;generated&quot;: true, &quot;annotations&quot;: {&quot;content&quot;: &quot;site_id&quot;}}">Item Id</ins>
<br>
Description
</div>
</body></html>
"""

EXTRACT_PAGE18 = u"""
<html><body>
<div>
Item Id
<br>
Description
</div>
</body></html>
"""

ANNOTATED_PAGE19 = u"""
<html><body>
<div>
<p data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;name&quot;}}">Product name</p>
<p data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;content&quot;: &quot;price&quot;}}">60.00</p>
<img data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;annotations&quot;: {&quot;src&quot;: &quot;image_urls&quot;}}"src="image.jpg" />
<p data-scrapy-annotate="{&quot;variant&quot;: 0, &quot;required&quot;: [&quot;description&quot;], &quot;annotations&quot;: {&quot;content&quot;: &quot;description&quot;}}">description</p>
</div>
</body></html>
"""

EXTRACT_PAGE19a = u"""
<html><body>
<div>
<p>Product name</p>
<p>60.00</p>
<img src="http://example.com/image.jpg" />
<p>description</p>
</div>
</body></html>
"""

EXTRACT_PAGE19b = u"""
<html><body>
<div>
<p>Range</p>
<p>from 20.00</p>
<img src="http://example.com/image1.jpg" />
<p>
<br/>
</div>
</body></html>
"""

SAMPLE_DESCRIPTOR1 = ItemDescriptor('test', 'product test', [
    A('name', "Product name", required=True),
    A('price', "Product price, including any discounts and tax or vat", 
        contains_any_numbers, True),    
    A('image_urls', "URLs for one or more images", image_url, True),
    A('description', "The full description of the product", allow_markup=True),
    ]
)

# A list of (test name, [templates], page, extractors, expected_result)
TEST_DATA = [
    # extract from a similar page
    ('similar page extraction', [ANNOTATED_PAGE1], EXTRACT_PAGE1, None,
        {u'title': [u'Nice Product'], u'description': [u'wonderful product'], 
            u'image_url': [u'nice_product.jpg']}
    ),
    # strip the first 5 characters from the title
    ('extractor test', [ANNOTATED_PAGE1], EXTRACT_PAGE1,
        ItemDescriptor('test', 'product test', 
            [A('title', "something about a title", lambda x: x[5:])]),
        {u'title': [u'Product'], u'description': [u'wonderful product'], 
            u'image_url': [u'nice_product.jpg']}
    ),
    # compilicated tag (multiple attributes and annotation)
    ('multiple attributes and annotation', [ANNOTATED_PAGE2], EXTRACT_PAGE2, None,
        {'name': [u'product 1'], 'image_url': [u'http://example.com/product1.jpg'],
            'description': [u'product 1 is great']}
    ),
    # can only work out correct placement by matching the second attribute first
    ('ambiguous description', [ANNOTATED_PAGE3], EXTRACT_PAGE3, None,
        {'description': [u'description'], 'delivery': [u'delivery']}
    ),
    # infer a repeated structure
    ('repeated elements', [ANNOTATED_PAGE4], EXTRACT_PAGE4, None,
        {'features': [u'feature1', u'feature2', u'feature3']}
    ),
    # identical variants with a repeated structure
    ('repeated identical variants', [ANNOTATED_PAGE5], EXTRACT_PAGE5, None,
         {
             'description': [u'description'],
             'variants': [
                 {u'colour': [u'colour 1'], u'price': [u'price 1']}, 
                 {u'colour': [u'colour 2'], u'price': [u'price 2']}, 
                 {u'colour': [u'colour 3'], u'price': [u'price 3']} 
             ]
         }
    ),
    # variants with an irregular structure
    ('irregular variants', [ANNOTATED_PAGE6], EXTRACT_PAGE6, None,
         {
             'description': [u'description'],
             'variants': [
                 {u'name': [u'name 1']}, 
                 {u'name': [u'name 3']}, 
                 {u'name': [u'name 2']}
             ]
         }
    ),

    # discovering repeated variants in table columns
#    ('variants in table columns', [ANNOTATED_PAGE7], EXTRACT_PAGE7, None,
#         {'variants': [
#             {u'colour': [u'colour 1'], u'price': [u'price 1']}, 
#             {u'colour': [u'colour 2'], u'price': [u'price 2']}, 
#             {u'colour': [u'colour 3'], u'price': [u'price 3']}
#         ]}
#    ),
    
    
    # ignored regions
    (
    'ignored_regions', [ANNOTATED_PAGE8], EXTRACT_PAGE8, None,
          {
             'description': [u'\n A very nice product for all intelligent people \n\n'],
             'price': [u'\n12.00\n(VAT exc.)'],
          }
    ),
    # shifted ignored regions (detected by region similarity)
    (
    'shifted_ignored_regions', [ANNOTATED_PAGE9], EXTRACT_PAGE9, None,
          {
             'description': [u'\n A very nice product for all intelligent people \n\n'],
             'price': [u'\n12.00\n(VAT exc.)'],
          }
    ),
    # detection of common prefixes across templates, all templates marked
    (# wrong extraction
    'without_match_common_prefix', [ANNOTATED_PAGE10a], EXTRACT_PAGE10a, None,
          {
             'price': [u'\n Series:  T2000 \n'],
             'dimensions': [u'\n Description  Electrorheological Cyborgs \n'],
             'site_id': [u'\n Offer  From $2500.00 \n'],
          }
    ),
    (# right extraction
    'with_match_common_prefix', [ANNOTATED_PAGE10a, ANNOTATED_PAGE10b], EXTRACT_PAGE10a, None,
          {}
    ),
    (# another example
    'match_common_prefix', [ANNOTATED_PAGE10a, ANNOTATED_PAGE10b], EXTRACT_PAGE10b, None,
          {
             'dimensions': [u'50cm'],
             'site_id': [u'K80'],
          }
    ),
    (# common_prefix with allow_markup attribute
    'common_prefix_allow_markup', [ANNOTATED_PAGE10a, ANNOTATED_PAGE10b], EXTRACT_PAGE10b,
        ItemDescriptor('test', 'product test',
            [A('dimensions', "something about dimensions", allow_markup=True)]),
          {
             'dimensions': [u'50cm</td>'],
             'site_id': [u'K80'],
          }
    ),
    (# special case with partial annotations
    'special_partial_annotation', [ANNOTATED_PAGE11], EXTRACT_PAGE11, None,
          {
            'name': [u'SL342'],
            'description': [u'\nSL342\n \nNice product for ladies\n \n&pounds;85.00\n'],
            'price': [u'&pounds;85.00'],
            'price_before_discount': [u'&pounds;100.00'],
          }
    ),
    (# with ignore-beneath feature
    'ignore-beneath', [ANNOTATED_PAGE12], EXTRACT_PAGE12a, None,
          {
            'description': [u'\n A very nice product for all intelligent people \n'],
          }
    ),
    (# ignore-beneath with extra tags
    'ignore-beneath with extra tags', [ANNOTATED_PAGE12], EXTRACT_PAGE12b, None,
          {
            'description': [u'\n A very nice product for all intelligent people \n'],
          }
    ),
    ('nested annotation with replica outside', [ANNOTATED_PAGE13a], EXTRACT_PAGE13a, None,
          {'description': [u'\n A product \n $50.00 \nThis product is excelent. Buy it!\n \n'],
           'price': ["$50.00"],
           'name': [u'A product']}
    ),
    ('outside annotation with nested replica', [ANNOTATED_PAGE13b], EXTRACT_PAGE13b, None,
          {'description': [u'\n A product \n $50.00 \nThis product is excelent. Buy it!\n'],
           'price': ["$45.00"],
           'name': [u'A product']}
    ),
    ('consistency check', [ANNOTATED_PAGE14], EXTRACT_PAGE14, None,
          {},
    ),
    ('consecutive nesting', [ANNOTATED_PAGE15], EXTRACT_PAGE15, None,
          {'description': [u'Description\n\n'],
           'price': [u'80.00']},
    ),
    ('nested inside not found', [ANNOTATED_PAGE16], EXTRACT_PAGE16, None,
          {'price': [u'90.00'],
           'name': [u'product name']},
    ),
    ('ignored region helps to find attributes', [ANNOTATED_PAGE17], EXTRACT_PAGE17, None,
          {'description': [u'\nThis product is excelent. Buy it!\n']},
    ),
    ('ignored region in partial annotation', [ANNOTATED_PAGE18], EXTRACT_PAGE18, None,
          {u'site_id': [u'Item Id'],
           u'description': [u'\nDescription\n']},
    ),
    ('extra required attribute product', [ANNOTATED_PAGE19], EXTRACT_PAGE19a,
         SAMPLE_DESCRIPTOR1,
         {u'price': [u'60.00'],
          u'description': [u'description'],
          u'image_urls': [['http://example.com/image.jpg']],
          u'name': [u'Product name']},
    ),
    ('extra required attribute no product', [ANNOTATED_PAGE19], EXTRACT_PAGE19b,
         SAMPLE_DESCRIPTOR1,
         None,
    ),
]

class TestExtraction(TestCase):

    def setUp(self):
        if not numpy:
            raise SkipTest("numpy not available")

    def _run_extraction(self, name, templates, page, extractors, expected_output):
        self.trace = None
        template_pages = [HtmlPage(None, {}, t) for t in templates]
        extractor = InstanceBasedLearningExtractor(template_pages, extractors, True)
        actual_output, _ = extractor.extract(HtmlPage(None, {}, page))
        if not actual_output:
            if expected_output is None:
                return
            assert False, "failed to extract data for test '%s'" % name
        actual_output = actual_output[0]
        self.trace = ["Extractor:\n%s" % extractor] + actual_output.pop('trace', [])
        expected_names = set(expected_output.keys())
        actual_names = set(actual_output.keys())
        
        missing_in_output = filter(None, expected_names - actual_names)
        error = "attributes '%s' were expected but were not present in test '%s'" % \
                ("', '".join(missing_in_output), name)
        assert len(missing_in_output) == 0, error

        unexpected = actual_names - expected_names
        error = "unexpected attributes %s in test '%s'" % \
                (', '.join(unexpected), name)
        assert len(unexpected) == 0, error

        for k, v in expected_output.items():
            extracted = actual_output[k]
            assert v == extracted, "in test '%s' for attribute '%s', " \
                "expected value '%s' but got '%s'" % (name, k, v, extracted)

    def test_expected_outputs(self):
        try:
            for data in TEST_DATA:
                self._run_extraction(*data)
        except AssertionError:
            if self.trace:
                print "Trace:"
                for line in self.trace:
                    print "\n---\n%s" % line
            raise
