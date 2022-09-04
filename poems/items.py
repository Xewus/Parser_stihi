import scrapy


class PoemsItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    