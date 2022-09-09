"""Команды для запуска парсеров.
"""
import os

ALL_POEMS = 'all-poems'
LIST_POEMS = 'list-poems'
CHOOSE_POEMS = 'choose-poems'

COMMANDS = {
    ALL_POEMS: f'scrapy crawl {ALL_POEMS} -a author=%s  --nolog',
    LIST_POEMS: f'scrapy crawl {LIST_POEMS} -a author=%s --nolog',
    CHOOSE_POEMS: f'scrapy crawl {CHOOSE_POEMS} -a urls=%s --nolog',
}


def parse(command: str):
    os.system(command=command)
