import json

from itemadapter import ItemAdapter

from app_core import settings

from .spiders.author import AllPoemsSpider
from scrapy import Item


class JsonAllPoemsTitlePipeline:
    def open_spider(self, spider: AllPoemsSpider):
        self.results = []

    def close_spider(self, spider: AllPoemsSpider):
        self.results.sort(key=lambda item: item[settings.TITLE])
        with open(settings.POEMS_STORE, 'w', encoding='utf-8') as store:
            store.write(json.dumps(self.results, ensure_ascii=False))

    def process_item(self, item: Item, spider: AllPoemsSpider):
        self.results.append(dict(item))
        return item
