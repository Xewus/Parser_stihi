"""Классы, упорядочивающие сохранение объектов.
"""
import scrapy


class ListPoemsItem(scrapy.Item):
    """Список названий стихов с ссылками.

    #### Attrs:
    - title
    - link
    """
    title = scrapy.Field()
    link = scrapy.Field()


class PoemItem(scrapy.Item):
    """Формат сохранения отдельного стиха.

    #### Attrs:
    - title
    - author
    - text
    """
    title = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field()
