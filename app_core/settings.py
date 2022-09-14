"""Общие настройки приложения.
"""
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

APP_NAME = os.environ.get('APP_NAME')

BASE_DIR = Path(__file__).resolve().parent.parent
RESULT_DIR = BASE_DIR / 'results'
DOCX_TEMPLATES = BASE_DIR / 'docx_templates'
DATABASE = f'{BASE_DIR}/stihoparse.db'

load_dotenv(dotenv_path=BASE_DIR)


class Config:
    SECRET_KEY = 'qwerty12;;;;;;;;;;;;;;'
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)


PONY = {
    'provider': 'sqlite',
    'filename': DATABASE,
    'create_db': True
}


SU_PASSWORD = os.environ.get('SU_PASSWORD')

MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 16
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 24


# Сохранение результатов
POEMS_STORE = f'{RESULT_DIR}/poems.json'
OUT_POEMS = f'{RESULT_DIR}/out'
POEMS_SEPARATOR = '\n' + '-' * 50 + '\n\n'

ARGS_SEPARATOR = '#'

# URL-адреса доступные для анонимных пользователей
URL_PATHS_FOR_ANONIM = {'/login/', '/static/style.css'}

# Названия сохраняемых полей
TITLE = 'title'
AUTHOR = 'author'
TEXT = 'text'
LINK = 'link'

# Настройки для `Scrapy`

BOT_NAME = 'poems'

SPIDER_MODULES = ['poems.spiders']
NEWSPIDER_MODULE = 'poems.spiders'

ALLOWED_DOMAINS = ['stihi.ru']
SITE_URL = 'https://stihi.ru/'
START_URL_FOR_PARSE = 'https://stihi.ru/avtor'

NAME_BASE_SPIDER = 'poems'
NAME_ALL_POEMS_SPIDER = 'all-poems'
NAME_LIST_POEMS_SPIDER = 'list-poems'
NAME_CHOOSE_POEMS_SPIDER = 'choose-poems'

CONCURRENT_REQUESTS = 32
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'poems.pipelines.JsonAllPoemsTitlePipeline': 300,
}
