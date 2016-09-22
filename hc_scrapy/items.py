from scrapy.item import Item, Field

class HcScrapyItem(Item):
    title = Field()
    link = Field()
    desc = Field()
    image = Field()
    price = Field()
    source = Field()
