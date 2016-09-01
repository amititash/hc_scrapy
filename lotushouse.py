
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

        name = 'lotushouse' 
        start_urls = ["http://thelotushouse.com/paintings-wall-hangings.html","http://thelotushouse.com/showpieces-figurines.html","http://thelotushouse.com/fashion-accessories.html","http://thelotushouse.com/home-furnishings.html"] 


        def parse(self, response): 
             for href in response.css('.product-image::attr(href)'): 
               full_url = response.urljoin(href.extract()) 
               yield scrapy.Request(full_url, callback=self.parse_product) 
              
             next_page = response.css(".next::attr('href')")
             if next_page:
               url = response.urljoin(next_page[0].extract())
               yield scrapy.Request(url, self.parse)

        def parse_product(self, response):
           items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('.product-name h1::text').extract_first()
           item['image'] =  response.css('img[id="image"]::attr(src)').extract_first()
           item['desc']  = response.css('.product-collateral').extract()
           item['price'] = response.css('.add_to_cart .add-to-box .price_box .price-box .regular-price .price::text').extract()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('h1::text').extract_first()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 