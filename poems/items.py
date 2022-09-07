import scrapy


class ListPoemsItem(scrapy.Item):
    """_summary_

    #### Attrs:
    - title
    - link
    """
    title = scrapy.Field()
    link = scrapy.Field()


class PoemItem(scrapy.Item):
    """_summary_

    #### Attrs:
    - title
    - author
    - text
    """
    title = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field()
