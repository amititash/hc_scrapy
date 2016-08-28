
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


URL = 'http://www.kilishop.com/in/c/All-Products/13/{page}'





class ScrapySampleItem(Item):
    title = Field()
    link = Field()
    desc = Field()
    image = Field()
    price = Field()



class purnawaSpider(scrapy.Spider): 
    handle_httpstatus_list = [404]
    name = "kilishop"
    
    
    def start_requests(self):
        index = 1
        while (index < 17):
            yield Request(URL.format(page=index))
            index +=1

    def parse(self, response):              
        for href in response.css('.prodimage::attr(href)'): 
				full_url = response.urljoin(href.extract()) 
				yield scrapy.Request(full_url, callback=self.parse_product) 
				
    def parse_product(self, response):
    		
    		items = []
    		item = ScrapySampleItem()
    		
    		item['title'] =  response.css('h1::text').extract()
    		item['image'] =  response.css('.photo::attr(src)').extract_first()
    		item['desc']  = response.css('.resetcss	::text').extract()
    		item['price'] = response.css('.main-price::text').extract()
    		
    		if not item['desc']:
    		 logging.info("EMPTY RECIEVED")
    		 item['desc']  = response.css('h1::text').extract()
    		 
    		item['link']  = response.url
    		
    		items.append(item)
    		
		for item in items:
			 		yield item
				