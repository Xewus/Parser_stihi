"""Общие настройки приложения.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
RESULT_DIR = BASE_DIR / 'results'
DOCX_TEMPLATES = BASE_DIR / 'docx_templates'

load_dotenv(dotenv_path=BASE_DIR)

SECRET_KEY = os.environ.get('SECRET KEY')

USERS_STORE = f'{BASE_DIR}/users.txt'

# Сохранение результатов
POEMS_STORE = f'{RESULT_DIR}/poems.json'
OUT_POEMS = f'{RESULT_DIR}/out'

# Время действия токена авторизации
LIVE_TOKEN = 60 * 60 * 20  # 20 hours

ARGS_SEPARATOR = '#'
SORT_KEY_CHOOSE_BY_TITLE = lambda x: x[1]

# URL-адреса доступные для анонимных пользователей
URL_PATHS_FOR_ANONIM = ('/login', '/static/style.css')

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

FEEDS = {
    POEMS_STORE: {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'item_classes': ['poems.items.ListPoemsItem', 'poems.items.PoemItem'],
        'overwrite': True
    }
}
