"""Команды для запуска парсеров.
"""
import os
import shutil
from parser.poems.settings import RESULT_DIR
from parser.poems.helpers import enums
from collections import namedtuple

ALL = enums.SpiderNames.ALL_POEMS.casefold()
LIST = enums.SpiderNames.LIST_POEMS.casefold()
CHOOSES = enums.SpiderNames.CHOOSE_POEMS.casefold()

COMMANDS = {
    ALL: f'scrapy crawl {ALL} -a author=%s --nolog',
    LIST: f'scrapy crawl {LIST} -a author=%s --nolog',
    CHOOSES: f'scrapy crawl {CHOOSES} -a author=%s -a urls=%s --nolog',
}


async def start_spider(spider: str, args: tuple) -> None:
    """Очищает директорию с результатами и запускает паука.

    #### Args:
    - spider (str): Имя паука.
    - args (tuple): Аргументы для запуска паука.
    """
    command = COMMANDS.get(spider)
    shutil.rmtree(RESULT_DIR)
    RESULT_DIR.mkdir()
    os.system(command=command % args)
