
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

        name = 'zansaar' 
        start_urls = ["http://www.zansaar.com/furniture/home-office-furniture/desks-tables","http://www.zansaar.com/furniture/home-office-furniture/office-chairs","http://www.zansaar.com/furniture/dining-room-furniture/dining-sets","http://www.zansaar.com/furniture/dining-room-furniture/dining-chairs-benches","http://www.zansaar.com/furniture/dining-room-furniture/dining-tables","http://www.zansaar.com/furniture/storage-shelves/drawers","http://www.zansaar.com/furniture/storage-shelves/wall-units","http://www.zansaar.com/furniture/storage-shelves/bookshelf-bookcases","http://www.zansaar.com/furniture/storage-shelves/shoe-cabinets","http://www.zansaar.com/furniture/storage-shelves/storage"] 


        def parse(self, response): 
             for href in response.css('.quick-look a::attr(href)'): 
               full_url = response.urljoin(href.extract()) 
               yield scrapy.Request(full_url, callback=self.parse_product) 
              
             next_page = response.css(".next a::attr('href')")
             if next_page:
               url = response.urljoin(next_page[0].extract())
               yield scrapy.Request(url, self.parse)

        def parse_product(self, response):
           items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('h1::text').extract_first()
           item['image'] =  response.css('img[id="pdpMainImg"]::attr(src)').extract_first()
           item['desc']  = response.css('.feature_desc  p::text').extract()
           item['price'] = response.css('.price h2 strong::text').extract()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('h1::text').extract_first()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 