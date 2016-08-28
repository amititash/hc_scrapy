
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


URL = 'http://www.amazon.in/s/ref=sr_pg_2/253-9879297-6008115?me=A14ORPKX5JU4E3&rh=i%3Amerchant-items&page={page}&ie=UTF8&qid=1471625807'





class ScrapySampleItem(Item):
    title = Field()
    link = Field()
    desc = Field()
    image = Field()
    price = Field()



class amazonSpider(scrapy.Spider): 
    handle_httpstatus_list = [404]
    name = "amazon"
    
    
    def start_requests(self):
        index = 1
        while (index < 6):
            yield Request(URL.format(page=index))
            index +=1

    def parse(self, response):              
        for href in response.css('.a-link-normal::attr(href)'): 
				full_url = response.urljoin(href.extract()) 
				yield scrapy.Request(full_url, callback=self.parse_product) 
				
    def parse_product(self, response):
    		
    		items = []
    		item = ScrapySampleItem()
    		
    		item['title'] =  response.css('h1::text').extract_first()
    		item['image'] =  response.css('.a-dynamic-image::attr(src)').extract_first()
    		item['desc']  = response.css('div[id="productDescription"] p::text').extract()
    		item['price'] = response.css('.a-color-price::text').extract()
    		
    		if not item['desc']:
    		 logging.info("EMPTY RECIEVED")
    		 item['desc']  = response.css('h1::text').extract_first()
    		 
    		item['link']  = response.url
    		
    		items.append(item)
    		
		for item in items:
			 		yield item
				