from pathlib import Path

import docx
from app_core.settings import BASE_DIR
from itemadapter import ItemAdapter


class AllPoemsTitlePipeline:
    def open_spider(self, spider):
        print('open', spider)
        spider.file = open(BASE_DIR / 'list.csv', 'a')

    def close_spider(self, spider):
        spider.file.close()

    def process_item(self, item, spider):
        spider.file.write(item)
