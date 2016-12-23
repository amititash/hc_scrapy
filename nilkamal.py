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

        name = 'niklamal' 
        start_urls = ["http://www.nilkamal.com/products/living-room-furniture/centre-tables/82","http://www.nilkamal.com/products/living-room-furniture/sofa-sets/80","http://www.nilkamal.com/products/living-room-furniture/sofa-cum-beds/81","http://www.nilkamal.com/products/living-room-furniture/centre-tables/82","http://www.nilkamal.com/products/living-room-furniture/corner-tables/291","http://www.nilkamal.com/products/living-room-furniture/recliners/516","http://www.nilkamal.com/products/living-room-furniture/wall-units/83","http://www.nilkamal.com/products/living-room-furniture/tv-trolleys/84"] 
     
		
        def parse(self, response): 
            for href in response.css('.product-box a::attr(href)'): 
              full_url = response.urljoin(href.extract()) 
              logging.info(full_url)
              yield scrapy.Request(full_url, callback=self.parse_product,dont_filter = True) 

        def parse_product(self, response):
           items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('h1::text').extract_first()
           item['image'] =  response.css('.firsr-img::attr(src)').extract()
           item['desc']  = response.css('div[id="tablist1-panel1"]').extract()
           item['price'] = response.css('.cost-now span::text').extract()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('h1::text').extract_first()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 