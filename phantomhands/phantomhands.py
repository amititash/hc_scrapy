
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

        name = 'phantomhands' 
        start_urls = ["http://phantomhands.in/"] 
     
		
        def parse(self, response): 
            for href in response.css('.image a::attr(href)'): 
              full_url = response.urljoin(href.extract()) 
              yield scrapy.Request(full_url, callback=self.parse_product) 

        def parse_product(self, response):
           items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('h1::text').extract_first()
           item['image'] =  response.css('.zoomImg::attr(src)').extract_first()
           item['desc']  = response.css('.description').extract()
           item['price'] = response.css('.money::text').extract_first()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('h1::text').extract_first()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 