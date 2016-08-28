
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


URL = 'http://www.postergully.com/collections/50-amazing-artworks-added-last-week?page={page}&view=json&_=1471526160348'


class ScrapySampleItem(Item):
    title = Field()
    link = Field()
    desc = Field()
    image = Field()
    price = Field()



class posterGullySpider(scrapy.Spider): 
    handle_httpstatus_list = [404]
    name = "postergully"
    
    
    def start_requests(self):
        index = 1
        while (index < 3):
            yield Request(URL.format(page=index))
            index +=1

    def parse(self, response):
                 
        for href in response.css('.main a::attr(href)'): 
				full_url = response.urljoin(href.extract()) 
				yield scrapy.Request(full_url, callback=self.parse_product) 
				
    def parse_product(self, response):
    		
    	   items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('h1::text').extract_first()
           item['image'] =  response.css('.MagicZoomPlus::attr(href)').extract_first()
           item['desc']  = response.css('.tags a::text').extract()
           item['price'] = ""
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('h1::text').extract_first()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 
				