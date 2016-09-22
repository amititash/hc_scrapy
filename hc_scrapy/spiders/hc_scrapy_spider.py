from scrapy.spiders import Spider
from scrapy.selector import Selector
from hc_scrapy.items import HcScrapyItem

class HcScrapySpider(Spider):
    name = "meetup"
    allowed_domains = ["meetup.com"]
    start_urls = [
        "http://www.meetup.com/Search-Meetup-Karlsruhe/"
    ]

    def parse(self, response):
        responseSelector = Selector(response)
        for sel in responseSelector.css('li.past.line.event-item'):
            item = HcScrapyItem()
            item['title'] = sel.css('a.event-title::text').extract()
            item['link'] = sel.xpath('a/@href').extract()
            yield item
