
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


class ScrapySampleItem(Item):
    title = Field()
    link = Field()
    desc = Field()
    image = Field()
    price = Field()



class purnawaSpider(scrapy.Spider): 
    name = "puranawa"
    
    start_urls = ["http://www.punarnawa.com/Home---Decor-depid-743416-page-1.html#page=1","http://www.punarnawa.com/Home---Decor-depid-743416-page-1.html#page=2",
    "http://www.punarnawa.com/Home---Decor-depid-743416-page-1.html#page=3","http://www.punarnawa.com/Home---Decor-depid-743416-page-1.html#page=4","http://www.punarnawa.com/Home---Decor-depid-743416-page-1.html#page=5","http://www.punarnawa.com/Home---Decor-depid-743416-page-1.html#page=6","http://www.punarnawa.com/Home---Decor-depid-743416-page-1.html#page=7","http://www.punarnawa.com/Home---Decor-depid-743416-page-1.html#page=8","http://www.punarnawa.com/Home---Decor-depid-743416-page-1.html#page=9","http://www.punarnawa.com/Home---Decor-depid-743416-page-1.html#page=10","http://www.punarnawa.com/Home---Decor-depid-743416-page-1.html#page=11","http://www.punarnawa.com/Home---Decor-depid-743416-page-1.html#page=12"] 
    

    def parse(self, response):              
        for href in response.css('.l5_previewBtn::attr(href)'): 
				full_url = response.urljoin(href.extract()) 
				yield scrapy.Request(full_url, callback=self.parse_product) 
				
    def parse_product(self, response):
    		
    		items = []
    		item = ScrapySampleItem()
    		
    		item['title'] =  response.css('h3::text').extract()
    		item['image'] =  response.css('div[id="largeImage"]::attr(src)').extract_first()
    		item['desc']  = response.css('div[id="l5_prodDesc"] p::text').extract()
    		item['price'] = response.css('div[id="price-section"] p::text').extract()
    		
    		if not item['desc']:
    		 logging.info("EMPTY RECIEVED")
    		 item['desc']  = response.css('h3::text').extract()
    		 
    		item['link']  = response.url
    		
    		items.append(item)
    		
		for item in items:
			 		yield item
				