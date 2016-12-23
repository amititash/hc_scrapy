
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

        name = 'rediff' 
        start_urls = ["http://shopping.rediff.com/categories/wall-stickers---decals/cat-13568/?sc_cid=fixcat_home|browse","http://shopping.rediff.com/categories/living-room-furniture/cat-715/format-0?sc_cid=fixcat_home|browse|search","http://shopping.rediff.com/categories/furniture/cat-712/format-0?sc_cid=fixcat_home|browse|search"] 


        def parse(self, response): 
             for href in response.css('.bwsURL::attr(href)'): 
               full_url = response.urljoin(href.extract()) 
               yield scrapy.Request(full_url, callback=self.parse_product) 
              
             next_page = response.css(".nextBtnbtm a::attr('href')")
             if next_page:
               url = response.urljoin(next_page[0].extract())
               yield scrapy.Request(url, self.parse)

        def parse_product(self, response):
           items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('.prodtitlenew::text').extract_first()
           item['image'] =  response.css('img[id="zoomImage"]::attr(src)').extract_first()
           item['desc']  = response.css('.rt').extract()
           item['price'] = response.css('span[id="prod_prcs"]::text').extract()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('.prodtitlenew::text').extract_first()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 