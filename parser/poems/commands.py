"""Команды для запуска парсеров.
"""
import os
from parser.poems.settings import SpiderNames

ALL = SpiderNames.ALL_POEMS
LIST = SpiderNames.LIST_POEMS
CHOOSES = SpiderNames.CHOOSE_POEMS

COMMANDS = {
    ALL: f'scrapy crawl {ALL} -a author=%s --nolog',
    LIST: f'scrapy crawl {LIST} -a author=%s --nolog',
    CHOOSES: f'scrapy crawl {CHOOSES} -a author=%s -a urls=%s --nolog',
}


def start_spider(command: str) -> None:
    os.system(command=command)
