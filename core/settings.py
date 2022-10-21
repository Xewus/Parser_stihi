"""Общие настройки приложения.
"""
import os
from pathlib import Path

from decouple import config

APP_NAME = os.environ.get('APP_NAME')

HEADERS = {
    'APP_KEY': config('APP_KEY')
}

BASE_DIR = Path(__file__).resolve().parent.parent

PROXY_LIST = BASE_DIR / 'core/helpers/proxy_list.txt'
USER_AGENTS_LIST = BASE_DIR / 'core/helpers/user_agents_list.txt'
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

SITE_URL = 'https://stihi.ru'
START_URL_FOR_PARSE = SITE_URL + '/avtor'

with open(USER_AGENTS_LIST) as f:
    USER_AGENTS = [line.rstrip() for line in f.readlines()]