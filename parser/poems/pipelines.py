"""Организация обработки и сохранения результатов парсинга.
"""
import json
from parser.poems.spiders.author import BasePoemsSpider

from scrapy import Item

from core.enums import StoreFields
from core.settings import POEMS_STORE
from core.utils import dir_manager


class JsonAllPoemsTitlePipeline:
    def open_spider(self, spider: BasePoemsSpider):
        self.results = []

    def close_spider(self, spider: BasePoemsSpider):
        self.results.sort(key=lambda item: item[StoreFields.TITLE])

        result_dir = dir_manager()
        result_file = result_dir / (POEMS_STORE % spider.author)

        with open(result_file, 'w', encoding='utf-8') as store:
            store.write(json.dumps(self.results, indent=2, ensure_ascii=False))

    def process_item(self, item: Item, spider: BasePoemsSpider):
        self.results.append(dict(item))
        return item
