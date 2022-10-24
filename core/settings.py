"""Общие настройки приложения.
"""
from pathlib import Path

from decouple import config

from core import constants as cnst

DEBUG = config('DEBUG', default=True)

APP_NAME = config('APP_NAME')

WEB_SCRAPY_HOST = config('WEB_SCRAPY_HOST', default='127.0.0.1')
WEB_SCRAPY_PORT = config('WEB_SCRAPY_PORT', default=8765)
WEB_SCRAPY_URL = f'http://{WEB_SCRAPY_HOST}:{WEB_SCRAPY_PORT}/'

APP_KEY = config('APP_KEY')

BASE_DIR = Path(__file__).resolve().parent.parent

# PROXY_LIST = BASE_DIR / 'core/helpers/proxy_list.txt'
# USER_AGENTS_LIST = BASE_DIR / 'core/helpers/user_agents_list.txt'
DOCX_TEMPLATES = BASE_DIR / 'core/docx_templates'

# '27_05_21_results/author_poems.json'
RESULT_DIR = str(BASE_DIR) + '/%s_results'
POEMS_STORE = '%s_poems.json'

DATE_FORMAT = '%y_%m_%d'
OUT_FORMATS = ('.md', '.json', '.docx')

ARGS_SEPARATOR = '#'

DEFAULT_TIME_BLOCK_IP = 60 * 15  # 15 minutes
DEFAULT_AMOUNT_TRIES = 3

ALLOWED_DOMAINS = ['stihi.ru']
