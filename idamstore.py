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

        name = 'idamstore' 
        start_urls = ["https://www.idamstore.com/collections/all?page=1","https://www.idamstore.com/collections/all?page=2","https://www.idamstore.com/collections/all?page=3"] 
     
		
        def parse(self, response): 
            for href in response.css('.ci a::attr(href)'): 
              full_url = response.urljoin(href.extract()) 
              logging.info(full_url)
              yield scrapy.Request(full_url, callback=self.parse_product,dont_filter = True) 

        def parse_product(self, response):
           items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('.section-title h1::text').extract_first()
           item['image'] =  response.css('.thumbnail::attr(src)').extract_first()
           item['desc']  = response.css('.rte span::text').extract()
           item['price'] = response.css('p[id="product-price"] .product-price::text').extract_first()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('.section-title h1::text').extract_first()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 