"""Команды для запуска парсеров.
"""
import os
from enum import Enum

from app_core import settings

ALL_POEMS  =   'all-poems'
LIST_POEMS  =  'list-poems'
CHOOSE_POEMS = 'choose-poems'

COMMANDS = {
    ALL_POEMS:    f'scrapy crawl all-poems -a author=%s  --nolog',
    LIST_POEMS:   f'scrapy crawl list-poems -a author=%s --nolog',
    CHOOSE_POEMS: f'scrapy crawl choose-poems -a urls=%s --nolog',
}


def parse(command: str):
    os.system(command=command)
