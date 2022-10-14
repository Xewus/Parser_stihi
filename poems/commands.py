"""Команды для запуска парсеров.
"""
import os

from poems.settings import SpiderNames

COMMANDS = {
    SpiderNames.ALL_POEMS: f'scrapy crawl {SpiderNames.ALL_POEMS} -a author=%s --nolog',
    SpiderNames.LIST_POEMS: f'scrapy crawl {SpiderNames.LIST_POEMS} -a author=%s --nolog',
    SpiderNames.CHOOSE_POEMS: f'scrapy crawl {SpiderNames.CHOOSE_POEMS} -a author=%s -a urls=%s,# --nolog',
}


def start_spider(command: str) -> None:
    os.system(command=command)