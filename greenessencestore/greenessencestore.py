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

        name = 'green essence' 
        start_urls = ["http://www.greenessencestore.com/Planters-depid-423-page-1.html"] 
     
		
        def parse(self, response): 
            for href in response.css('.catprodimg a::attr(href)'): 
              full_url = response.urljoin(href.extract()) 
              logging.info(full_url)
              yield scrapy.Request(full_url, callback=self.parse_product,dont_filter = True) 

        def parse_product(self, response):
           items = []
           item = ScrapySampleItem()
    
           item['title'] =  map(unicode.strip, response.css('.title::text').extract())
           item['image'] =  response.css('img[id="largeImage"]::attr(src)').extract_first()
           item['desc']  = response.css('.desc_shorttext').extract()
           item['price'] = response.css('.amt::text').extract_first()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('.title::text').extract()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 