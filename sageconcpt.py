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

        name = 'sageconcept' 
        start_urls = ["http://sagekoncpt.com/index.php?route=product/category&path=79_92","http://sagekoncpt.com/index.php?route=product/category&path=79_92&page=2","http://sagekoncpt.com/index.php?route=product/category&path=59","http://sagekoncpt.com/index.php?route=product/category&path=59&page=2","http://sagekoncpt.com/index.php?route=product/category&path=59&page=3","http://sagekoncpt.com/index.php?route=product/category&path=59&page=4"] 
     
		
        def parse(self, response): 
            for href in response.css('.image a::attr(href)'): 
              full_url = response.urljoin(href.extract()) 
              logging.info(full_url)
              yield scrapy.Request(full_url, callback=self.parse_product,dont_filter = True) 

        def parse_product(self, response):
           items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('.product-title::text').extract_first()
           item['image'] =  response.css('.thumbnail img::attr(src)').extract_first()
           item['desc']  = response.css('div[id="tab-description"]').extract()
           item['price'] = response.css('.product-price::text').extract_first()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('.product-title::text').extract_first()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 