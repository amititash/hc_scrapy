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

        name = 'postbox' 
        start_urls = ["https://www.thepostbox.in/collections/vibrant-funky-india-cotton-cushion-covers","https://www.thepostbox.in/collections/wall-art","https://www.thepostbox.in/collections/trays-by-kalakaari-haath","https://www.thepostbox.in/collections/terracotta-mugs","https://www.thepostbox.in/collections/handpainted-blue-pottery-the-postbox","https://www.thepostbox.in/collections/coasters-cork-board-city-themes-graphic-art","https://www.thepostbox.in/collections/vibrant-printed-ceramic-mugs-the-postbox"] 
     
		
        def parse(self, response): 
            for href in response.css('.ci a::attr(href)'): 
              full_url = response.urljoin(href.extract()) 
              logging.info(full_url)
              yield scrapy.Request(full_url, callback=self.parse_product,dont_filter = True) 

        def parse_product(self, response):
           items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('.section-title h1::text').extract_first()
           item['image'] =  response.css('.main-product-image img::attr(src)').extract_first()
           item['desc']  = response.css('.rte').extract()
           item['price'] = response.css('.product-price .money::text').extract_first()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('.section-title h1::text').extract_first()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 