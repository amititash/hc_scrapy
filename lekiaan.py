#single page crawl
import scrapy
import logging
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from scrapy import Request, Spider
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector


from scrapy.item import Item, Field

class ScrapySampleItem(Item):
    title = Field()
    link = Field()
    desc = Field()
    price =  Field()
    image = Field()
    
    
class StackOverflowSpider(scrapy.Spider): 

        name = 'lekian others' 
        start_urls = ["http://www.lekiaan.com/categories/storage/cid-CU00204280.aspx", "http://www.lekiaan.com/categories/display/cid-CU00204288.aspx","http://www.lekiaan.com/categories/mirrors/cid-CU00204296.aspx","http://www.lekiaan.com/categories/accessories/cid-CU00204298.aspx","http://www.lekiaan.com/categories/television-units/cid-CU00262438.aspx","http://www.lekiaan.com/categories/chairs/cid-CU00273640.aspx"] 
     
		
        def parse(self, response): 
            for href in response.css('.bucket_left a::attr(href)'): 
              full_url = response.urljoin(href.extract()) 
              logging.info(full_url)
              yield scrapy.Request(full_url, callback=self.parse_product,dont_filter = True) 

        def parse_product(self, response):
           items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('h1::text').extract_first()
           item['image'] =  response.css('.product-largimg::attr(src)').extract_first()
           item['desc']  = response.css('.product_desc p::text').extract()
           item['price'] = response.css('.sp_amt::text').extract_first()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('h1::text').extract_first()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 