

import scrapy
import logging
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector


class StackOverflowSpider(scrapy.Spider): 

		name = 'stackoverflow' 
		start_urls = ['http://www.mirrorkart.com/Buy-Designers-Mirrors-online'] 
		
		rules = (
		    Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//ul[@class="pagination"]/li',)), callback="parse", follow=True),
		)
		
		def parse(self, response): 
			for href in response.css('.product-thumb .image a::attr(href)'): 
				full_url = response.urljoin(href.extract()) 
				yield scrapy.Request(full_url, callback=self.parse_product) 
				
		def parse_product(self, response): 
			yield { 
			'title': response.css('h1::text').extract_first(), 
			'image': response.css('.thumbnails a::attr(href)').extract_first(), 
			'desc' : response.css('div[id="tab-description"] p').extract(),
			'link': response.url, 
			}