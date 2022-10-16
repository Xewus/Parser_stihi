"""Организация обработки и сохранения результатов парсинга.
"""
import json
from poems.spiders.author import BasePoemsSpider
from poems.settings import POEMS_STORE, StoreFields
from time import time

from scrapy import Item


class JsonAllPoemsTitlePipeline:
    def open_spider(self, spider: BasePoemsSpider):
        self.results = []

        print('\n' * 3, 'pip start', spider.name, spider.author, time().real)

    def close_spider(self, spider: BasePoemsSpider):

        print('pip clos', spider.name, spider.author, time().real)

        self.results.sort(key=lambda item: item[StoreFields.TITLE])
        result_file = POEMS_STORE % spider.author
        with open(result_file, 'w', encoding='utf-8') as store:
            store.write(json.dumps(self.results, indent=2, ensure_ascii=False))

    def process_item(self, item: Item, spider: BasePoemsSpider):
        self.results.append(dict(item))
        return item
