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

        name = 'homestop' 
        start_urls = ["http://www.homeshop18.com/home-decor/category:3553/"] 
     
		
        def parse(self, response): 
            for href in response.css('.productTitle::attr(href)'): 
              full_url = response.urljoin(href.extract()) 
              logging.info(full_url)
              yield scrapy.Request(full_url, callback=self.parse_product,dont_filter = True) 

        def parse_product(self, response):
           items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('h1 span::text').extract_first()
           item['image'] =  response.css('cloudzoom-default img::attr(src)').extract()
           item['desc']  = response.css('.keyfeaturesBoxDiv').extract()
           item['price'] = response.css('.cost-now span::text').extract()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('h1 span::text').extract_first()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 