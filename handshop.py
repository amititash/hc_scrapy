
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

        name = 'anhadshop' 
        start_urls = ["https://www.theanhadshop.com/collections/home-textile","https://www.theanhadshop.com/collections/tableware"] 


        def parse(self, response): 
             for href in response.css('.ci a::attr(href)'): 
               full_url = response.urljoin(href.extract()) 
               yield scrapy.Request(full_url, callback=self.parse_product) 
              
             next_page = response.css(".current a::attr('href')")
             if next_page:
               url = response.urljoin(next_page[0].extract())
               yield scrapy.Request(url, self.parse)

        def parse_product(self, response):
           items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('h1::text').extract_first()
           item['image'] =  response.css('.desktop-10 img::attr(src)').extract_first()
           item['desc']  = response.css('.rte').extract()
           item['price'] = response.css('p[id="product-price"] .product-price .money').extract()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('.rte').extract()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 