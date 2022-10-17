"""Команды для запуска парсеров.
"""
import os
import shutil

from helpers import enums
from settings import RESULT_DIR

ALL = enums.SpiderNames.ALL_POEMS
LIST = enums.SpiderNames.LIST_POEMS
CHOOSES = enums.SpiderNames.CHOOSE_POEMS

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
