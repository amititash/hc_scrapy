
#paginated crawl
import scrapy
import logging
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from scrapy import Request, Spider
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector


from scrapy.item import Item, Field


URL = 'http://www.artisera.com/collections/rugs?page={page}'


class ScrapySampleItem(Item):
    title = Field()
    link = Field()
    desc = Field()
    image = Field()
    price = Field()



class artiseraFurnitureSpider(scrapy.Spider): 
    handle_httpstatus_list = [404]
    name = "artisera funrniter"
    
    
    def start_requests(self):
        index = 1
        while (index < 3):
            yield Request(URL.format(page=index))
            index +=1

    def parse(self, response):
                 
        for href in response.css('.product-name a::attr(href)'): 
				full_url = response.urljoin(href.extract()) 
				yield scrapy.Request(full_url, callback=self.parse_product) 
				
    def parse_product(self, response):
    		
    	   items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('.product-name h1::text').extract_first()
           item['image'] =  response.css('.easyzoom a::attr(href)').extract_first()
           item['desc']  = response.css('.pr_dis').extract()
           item['price'] = response.css('.money::text').extract_first()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('h1::text').extract_first()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 
				