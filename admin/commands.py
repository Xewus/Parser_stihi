"""Команды для запуска парсеров.
"""
import os
from enum import Enum

from app_core import settings

set_env_path = 'export PYTHONPATH=${PYTHONPATH}:%s' % settings.BASE_DIR

ALL_POEMS = 'all-poems'
LIST_POEMS = 'list-poems'
CHOOSE_POEMS = 'choose-poems'

COMMANDS = {
    ALL_POEMS: 'scrapy crawl all-poems -a author=%s -O all.csv --nolog',
    LIST_POEMS: 'scrapy crawl list-poems -a author=%s --nolog',
    CHOOSE_POEMS: 'scrapy crawl choose-poems -a urls=%s -O choose.csv'
}
command = 'scrapy crawl %s -a author=%s -o %s.csv --nolog'


def parse(command: str):
    print(command)
    os.system(command=command)
