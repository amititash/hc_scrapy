from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from hc_scrapy.items import HcScrapyItem

URL = 'http://www.amazon.in/s/ref=sr_pg_2/253-9879297-6008115?me=A14ORPKX5JU4E3&rh=i%3Amerchant-items&page={page}&ie=UTF8&qid=1471625807'

class amazonSpider(Spider): 
    handle_httpstatus_list = [404]
    name = "amazon"
    allowed_domains = ["amazon.in"]
    
    def start_requests(self):
        index = 1
        while (index < 6):
            yield Request(URL.format(page=index), self.parse)
            index += 1

    def parse(self, response):
        self.logger.error('=======parse===========')
        for href in response.css('.a-link-normal::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield Request(full_url, callback=self.parse_product)

    def parse_product(self, response):
            
        items = []
        item = HcScrapyItem()

        item['title'] =  response.css('h1::text').extract_first()
        item['image'] =  response.css('.a-dynamic-image::attr(src)').extract_first()
        item['desc']  = response.css('div[id="productDescription"] p::text').extract()
        item['price'] = response.css('.a-color-price::text').extract()
        item['source'] = 'amazon'

        if not item['desc']:
            self.logger.info("EMPTY RECIEVED")
            item['desc']  = response.css('h1::text').extract_first()

        item['link']  = response.url
        items.append(item)
            
        for item in items:
            yield item
