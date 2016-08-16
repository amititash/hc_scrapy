
import scrapy
import logging
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from scrapy import Request, Spider
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector


from scrapy.item import Item, Field


URL = 'http://kcwalldecals.com/20-quotes-decals?p={page}'



class ScrapySampleItem(Item):
    title = Field()
    link = Field()
    desc = Field()
    image = Field()



class StackOverflowSpider(scrapy.Spider): 
    handle_httpstatus_list = [404]
    name = "kwaldecal"
    
    
    def start_requests(self):
        index = 1
        while (index < 9):
            yield Request(URL.format(page=index))
            index +=1

    def parse(self, response):

        for href in response.css('.product_img_link::attr(href)'): 
				full_url = response.urljoin(href.extract()) 
				yield scrapy.Request(full_url, callback=self.parse_product) 
				
    def parse_product(self, response):
    		
    		items = []
    		item = ScrapySampleItem()
    		
    		item['title'] =  response.css('h1::text').extract_first()
    		item['image'] =  response.css('img[id="bigpic"]::attr(src)').extract_first()
    		item['desc']  = response.css('div[id="short_description_content"] p').extract()
    		
    		if not item['desc']:
    		 logging.info("EMPTY RECIEVED")
    		 
    		item['link']  = response.url
    		
    		items.append(item)
    		
		for item in items:
			 		yield item
				