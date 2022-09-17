"""Команды для запуска парсеров.
"""
import os

from app_core.settings import (NAME_ALL_POEMS_SPIDER, NAME_CHOOSE_POEMS_SPIDER,
                               NAME_LIST_POEMS_SPIDER)

COMMANDS = {
    NAME_ALL_POEMS_SPIDER: f'scrapy crawl {NAME_ALL_POEMS_SPIDER} -a author=%s  --nolog',
    NAME_LIST_POEMS_SPIDER: f'scrapy crawl {NAME_LIST_POEMS_SPIDER} -a author=%s --nolog',
    NAME_CHOOSE_POEMS_SPIDER: f'scrapy crawl {NAME_CHOOSE_POEMS_SPIDER} -a urls=%s --nolog',
}


def parse(command: str):
    os.system(command=command)
