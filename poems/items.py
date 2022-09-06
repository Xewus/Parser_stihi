import scrapy


class ListPoemsItem(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()

class PoemItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field()
    end = scrapy.Field()
