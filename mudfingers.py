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

        name = 'mudfingers' 
        start_urls = ["http://www.mudfingers.com/AIR-PLANTS-depid-956101-page-1.html","http://www.mudfingers.com/COLORED-CLAYS-depid-932279-page-1.html","http://www.mudfingers.com/SUN-LOVERS-depid-421491-page-1.html","http://www.mudfingers.com/TERRARIUMS-depid-421269-page-1.html","http://www.mudfingers.com/AIR-PLANTS-depid-956101-page-1.html",] 
     
		
        def parse(self, response): 
            for href in response.css('.standard a::attr(href)'): 
              full_url = response.urljoin(href.extract()) 
              logging.info(full_url)
              yield scrapy.Request(full_url, callback=self.parse_product,dont_filter = True) 

        def parse_product(self, response):
           items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('h1::text').extract_first()
           item['image'] =  response.css('.z-product-thumbs img::attr(src)').extract_first()
           item['desc']  = response.css('div[id="description"]').extract()
           item['price'] = response.css('.prices .price_original span[id="price-standard"]::text').extract_first()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('h1::text').extract_first()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 