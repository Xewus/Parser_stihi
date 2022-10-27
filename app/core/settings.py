"""Общие настройки приложения.
"""
from pathlib import Path

from decouple import config

DEBUG = config('DEBUG', default=True)

APP_NAME = config('APP_NAME')
APP_DESCRIPTION = '''
Сервер для формирваания запросов к `Scrapy` и выдачи файлов в нужном формате.
'''
APP_VERSION = '0.1.1'

WEB_SCRAPY_HOST = config('WEB_SCRAPY_HOST', default='127.0.0.1')
WEB_SCRAPY_PORT = config('WEB_SCRAPY_PORT', default=8765)
WEB_SCRAPY_URL = f'http://{WEB_SCRAPY_HOST}:{WEB_SCRAPY_PORT}/scrapy'

START_URL_FOR_PARSE = 'https://stihi.ru/avtor/'

APP_KEY = config('APP_KEY')
HEADERS = {
    'app-key': APP_KEY
}

BASE_DIR = Path(__file__).resolve().parent.parent

DOCX_TEMPLATES = BASE_DIR / 'core/docx_templates'

POEMS_STORE = '%s_%s.json'

DATE_FORMAT = config('DATE_FORMAT')
OUT_FORMATS = ('.md', '.json', '.docx')

DEFAULT_TIME_BLOCK_IP = 60 * 15  # 15 minutes
DEFAULT_AMOUNT_TRIES = 3

##########################################################################
AUTHOR = {
    'name': 'xewus',
    'email': 'xewuss@yandex.ru',
    'url': 'https://github.com/Xewus/Parser_stihi'
}
