"""Команды для запуска парсеров.
"""
import os

from app_core.settings import (NAME_ALL_POEMS_SPIDER, NAME_CHOOSE_POEMS_SPIDER,
                               NAME_LIST_POEMS_SPIDER)

ALL_POEMS = NAME_ALL_POEMS_SPIDER
CHOOSE_POEMS = NAME_CHOOSE_POEMS_SPIDER
LIST_POEMS = NAME_LIST_POEMS_SPIDER

COMMANDS = {
    ALL_POEMS: f'scrapy crawl {ALL_POEMS} -a author=%s',#  --nolog',
    LIST_POEMS: f'scrapy crawl {LIST_POEMS} -a author=%s',# --nolog',
    CHOOSE_POEMS: f'scrapy crawl {CHOOSE_POEMS} -a urls=%s',# --nolog',
}


def parse(command: str):
    os.system(command=command)
