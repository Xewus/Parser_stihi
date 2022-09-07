from app_core import settings

import json
from itemadapter import ItemAdapter
from .spiders.author import AllPoemsSpider


# Example. Not using now.
class JsonAllPoemsTitlePipeline:
    def open_spider(self, spider: AllPoemsSpider):
        print('open', spider)
        self.file = open(settings.POEMS_STORE, 'w')

    def close_spider(self, spider: AllPoemsSpider):
        self.file.close()

    def process_item(self, item, spider: AllPoemsSpider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
