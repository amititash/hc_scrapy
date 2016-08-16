
import scrapy
import logging
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import SitemapSpider

from scrapy.item import Item, Field


class ScrapySampleItem(Item):
   link = Field()
    
    
class MySpider(scrapy.Spider):
    name = "xyz"
    allowed_domains = ["http://kcwalldecals.com"]
    start_urls = ["http://kcwalldecals.com/sitemap"] 


    def parse(self, response):
        items = []
        for href in response.css('.tree li a::attr(href)'): 
          full_url = response.urljoin(href.extract())
          item = ScrapySampleItem()
          item['link'] = full_url
          items.append(item)
        return self.parse_product(items)

    def parse_product(self, items):
      logging.info('here')
      for item in items:
      	 yield item