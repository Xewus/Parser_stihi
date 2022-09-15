"""Команды для запуска парсеров.
"""
import os

from app_core.settings import ALL_POEMS, CHOOSE_POEMS, LIST_POEMS

COMMANDS = {
    ALL_POEMS: f'scrapy crawl {ALL_POEMS} -a author=%s  --nolog',
    LIST_POEMS: f'scrapy crawl {LIST_POEMS} -a author=%s --nolog',
    CHOOSE_POEMS: f'scrapy crawl {CHOOSE_POEMS} -a urls=%s --nolog',
}


def parse(command: str):
    os.system(command=command)
