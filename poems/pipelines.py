from pathlib import Path

import docx
from itemadapter import ItemAdapter


class PoemsPipeline:
    def open_spider(self, spider):
        print('open', spider)
        spider.document = docx.Document()

    def close_spider(self, spider):
        document_name = Path.cwd() / f'{self.name}.docx'
        spider.document.save(document_name)

    def process_item(self, item, spider):
        return item
