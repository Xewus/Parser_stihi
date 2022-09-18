"""Общие настройки приложения.
"""
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
RESULT_DIR = BASE_DIR / 'results'
DOCX_TEMPLATES = BASE_DIR / 'docx_templates'
DATABASE = f'{BASE_DIR}/stihoparse.db'

load_dotenv(dotenv_path=BASE_DIR)

APP_NAME = os.environ.get('APP_NAME')

DEFAULT_TIME_BLOCK_IP = 60 * 15  # 15 minutes
DEFAULT_AMOUNT_TRIES = 3


class Config:
    DEBUG = os.environ.get('DEBUG', default=False)
    ENV = os.environ.get('ENV', default='production')
    SECRET_KEY = "os.environ.get('SECRET_KEY')"
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    PONY = {
        'provider': 'sqlite',
        'filename': DATABASE,
        'create_db': True
    }


SU_PASSWORD = os.environ.get('SU_PASSWORD')
FIRST_USERNAME = os.environ.get('FIRST_USERNAME')
FIRST_PASSWORD = os.environ.get('FIRST_PASSWORD')

MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 16
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 24

# URL-адреса доступные для анонимных пользователей
URL_PATHS_FOR_ANONIM = ('/login/', '/static/style.css')

# Названия сохраняемых полей
TITLE = 'title'
AUTHOR = 'author'
TEXT = 'text'
LINK = 'link'

# Сохранение результатов
POEMS_STORE = f'{RESULT_DIR}/poems.json'
OUT_POEMS = f'{RESULT_DIR}/out'

# Строка разделяющая стихи
POEMS_SEPARATOR = '\n' + '-' * 50 + '\n\n'

ARGS_SEPARATOR = '#'
