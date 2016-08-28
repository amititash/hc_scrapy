
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

        name = 'anek linen' 
        start_urls = ["https://www.anekdesigns.com/collections/table-linen-1"] 
  
		
        def parse(self, response): 
            for href in response.css('.product-grid-item::attr(href)'):
              full_url = response.urljoin(href.extract()) 
              yield scrapy.Request(full_url, callback=self.parse_product) 

        def parse_product(self, response):
    		
    	   items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('h2::text').extract_first()
           item['image'] =  response.css('div[id="productPhoto"] img::attr(src)').extract()
           item['desc']  = response.css('.product-description p::text').extract()
           item['price'] = response.css('span[id="productPrice"] small::text').extract()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('h2::text').extract_first()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item  