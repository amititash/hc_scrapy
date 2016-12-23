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

        name = 'darzi' 
        start_urls = ["http://www.darzzi.com/products.cfm?type=1","http://www.darzzi.com/products.cfm?type=1261","http://www.darzzi.com/products.cfm?type=2"] 
     
		
        def parse(self, response): 
            for href in response.css('.boxLink::attr(href)'): 
              full_url = response.urljoin(href.extract()) 
              logging.info(full_url)
              yield scrapy.Request(full_url, callback=self.parse_product,dont_filter = True) 

        def parse_product(self, response):
           items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('.productSpecs h4::text').extract_first()
           item['image'] =  response.css('.cloud-zoom img::attr(src)').extract_first()
           item['desc']  = response.css('.productSpecs dl::text').extract()
           item['price'] = response.css('.regular-price .price::text').extract_first()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('.product-name h1::text').extract_first()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 