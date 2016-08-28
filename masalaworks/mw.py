
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


URL = 'http://www.masalaworks.com/collections/cushions-may-2013?page={page}'

#http://www.masalaworks.com/collections/cushions-may-2013 | http://www.masalaworks.com/collections/diary | http://www.masalaworks.com/collections/earring-organizer | http://www.masalaworks.com/collections/trivets




class ScrapySampleItem(Item):
    title = Field()
    link = Field()
    desc = Field()
    image = Field()
    price = Field()



class StackOverflowSpider(scrapy.Spider): 
    handle_httpstatus_list = [404]
    name = "masalaworks"
    
    
    def start_requests(self):
        index = 1
        while (index < 7):
            yield Request(URL.format(page=index))
            index +=1

    def parse(self, response):
        if (response.css('.c22::text').extract_first() == 'No products found in this collection.'):
        # stop crawling
                 logging.info("+++++++CLOOOSIIINGGGGGG+++++")
                 raise CloseSpider('STOPPED at %s' % response.url)
                 
        for href in response.css('.more a::attr(href)'): 
				full_url = response.urljoin(href.extract()) 
				yield scrapy.Request(full_url, callback=self.parse_product) 
				
    def parse_product(self, response):
    		
    		items = []
    		item = ScrapySampleItem()
    		
    		item['title'] =  response.css('h1::text').extract_first()
    		item['image'] =  response.css('.thumbnail a::attr(href)').extract_first()
    		item['desc']  = response.css('div[id="content"] p span::text').extract()
    		item['price'] = response.css('.price-current .money::text').extract_first()
    		
    		if not item['desc']:
    		 logging.info("EMPTY RECIEVED")
    		 item['desc']  = response.css('h1::text').extract_first()
    		 
    		item['link']  = response.url
    		
    		items.append(item)
    		
		for item in items:
			 		yield item
				