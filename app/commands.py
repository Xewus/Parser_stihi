"""Команды для запуска парсеров.
"""
import os

from app_core.settings import (NAME_ALL_POEMS_SPIDER, NAME_CHOOSE_POEMS_SPIDER,
                               NAME_LIST_POEMS_SPIDER)

ALL_POEMS = NAME_ALL_POEMS_SPIDER
CHOOSE_POEMS = NAME_CHOOSE_POEMS_SPIDER
LIST_POEMS = NAME_LIST_POEMS_SPIDER

COMMANDS = {
    ALL_POEMS: f'scrapy crawl -a author=%s -a user=%s {ALL_POEMS}',#  --nolog',
    LIST_POEMS: f'scrapy crawl -a author=%s -a user=%s {LIST_POEMS} --nolog',
    CHOOSE_POEMS: f'scrapy crawl -a author=%s -a user=%s {CHOOSE_POEMS}',# --nolog',
}


def parse(command: str):
    os.system(command=command)
