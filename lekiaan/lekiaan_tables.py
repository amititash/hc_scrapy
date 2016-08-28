
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


URL = 'http://www.lekiaan.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput=%7B%22PgControlId%22:2544135,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:{page},%22DivClientId%22:%222544135_CU00204262%22,%22SortingValues%22:%22LIFO%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CU00204262%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%220%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22%7D&_=1471488752780'


class ScrapySampleItem(Item):
    title = Field()
    link = Field()
    desc = Field()
    image = Field()
    price = Field()



class StackOverflowSpider(scrapy.Spider): 
    handle_httpstatus_list = [404]
    name = "lekiaan tables"
    
    
    def start_requests(self):
        index = 1
        while (index < 6):
            yield Request(URL.format(page=index))
            index +=1

    def parse(self, response):
                 
        for href in response.css('.bucket_left a::attr(href)'): 
				full_url = response.urljoin(href.extract()) 
				yield scrapy.Request(full_url, callback=self.parse_product) 
				
    def parse_product(self, response):
    		
    	   items = []
           item = ScrapySampleItem()
    
           item['title'] =  response.css('h1::text').extract_first()
           item['image'] =  response.css('.product-largimg::attr(src)').extract_first()
           item['desc']  = response.css('.product_desc p').extract()
           item['price'] = response.css('.sp_amt::text').extract_first()
           
           if not item['desc']:
               logging.info("EMPTY RECIEVED")
               item['desc']  = response.css('h1::text').extract_first()
           item['link']  = response.url
           items.append(item)
    		
           for item in items:
               yield item 
				