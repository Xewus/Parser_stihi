"""Организация обработки и сохранения результатов парсинга.
"""
import json
from parser.core.enums import StoreFields
from parser.poems.spiders.author import BasePoemsSpider

from scrapy import Item


class JsonAllPoemsTitlePipeline:
    def open_spider(self, spider: BasePoemsSpider):
        self.results = []

    def close_spider(self, spider: BasePoemsSpider):
        self.results.sort(key=lambda item: item[StoreFields.TITLE])

        with open(spider.result_file, 'w', encoding='utf-8') as store:
            store.write(json.dumps(self.results, indent=2, ensure_ascii=False))

    def process_item(self, item: Item, spider: BasePoemsSpider):
        self.results.append(dict(item))
        return item
