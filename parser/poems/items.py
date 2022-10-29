"""Классы, упорядочивающие сохранение объектов.
"""
from scrapy import Field, Item


class ListPoemsItem(Item):
    """Список названий стихов с ссылками.

    #### Attrs:
    - title
    - link
    """
    title = Field()
    link = Field()


class PoemItem(Item):
    """Формат сохранения отдельного стиха.

    #### Attrs:
    - title
    - author
    - text
    """
    title = Field()
    author = Field()
    text = Field()
