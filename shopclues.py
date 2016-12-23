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

        name = 'shopclues' 
        start_urls = ["http://www.shopclues.com/home-garden/new-arrivals-9.html","http://www.shopclues.com/home-garden/bed-special-1.html","http://www.shopclues.com/home-garden/kitchen-and-dining-special-4/storage-organization.html","http://www.shopclues.com/home-garden/sofa-special.html"] 
     
		
        def parse(self, response): 
            for href in response.css('.details .name::attr(href)'): 
              full_url = response.urljoin(href.extract()) 
              logging.info(full_url)
              yield scrapy.Request(full_url, callback=self.parse_product,dont_filter = True) 

        def parse_product(self, response):
           items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('h1::text').extract_first()
           item['image'] =  response.css('.jqzoom::attr(href)').extract_first()
           item['desc']  = response.css('.product-details-list').extract()
           item['price'] = response.css('.price::text').extract_first()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('h1::text').extract_first()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 