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
    SECRET_KEY = os.environ.get('SECRET_KEY')
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

# аргументы команд парсеров
ALL_POEMS = 'all-poems'
LIST_POEMS = 'list-poems'
CHOOSE_POEMS = 'choose-poems'

# Сохранение результатов
POEMS_STORE = f'{RESULT_DIR}/poems.json'
OUT_POEMS = f'{RESULT_DIR}/out'

# Строка разделяющая стихи
POEMS_SEPARATOR = '\n' + '-' * 50 + '\n\n'

ARGS_SEPARATOR = '#'

# Настройки для `Scrapy`
BOT_NAME = 'poems'

SPIDER_MODULES = ['poems.spiders']
NEWSPIDER_MODULE = 'poems.spiders'

ALLOWED_DOMAINS = ['stihi.ru']
SITE_URL = 'https://stihi.ru'
START_URL_FOR_PARSE = 'https://stihi.ru/avtor'

NAME_BASE_SPIDER = 'poems'
NAME_ALL_POEMS_SPIDER = 'all-poems'
NAME_LIST_POEMS_SPIDER = 'list-poems'
NAME_CHOOSE_POEMS_SPIDER = 'choose-poems'

ITEM_PIPELINES = {
    'poems.pipelines.JsonAllPoemsTitlePipeline': 300,
}

CONCURRENT_REQUESTS = 1
# DOWNLOAD_DELAY = 2
ROBOTSTXT_OBEY = False
# Retry many times since proxies often fail
RETRY_TIMES = 2
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy_proxies.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : None,
    'poems.middlewares.RotateUserAgentMiddleware' :400, 
}
# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
# ...
PROXY_LIST = BASE_DIR / 'proxy_list.txt'
# Proxy mode
# 0 = Every requests have different proxy
# 1 = Take only one proxy from the list and assign it to every requests
# 2 = Put a custom proxy to use in the settings
PROXY_MODE = 0

# If proxy mode is 2 uncomment this sentence :
#CUSTOM_PROXY = "http://host1:port"

# the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
# for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php

USER_AGENTS = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
    'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
    'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20140205 Firefox/24.0 Iceweasel/24.3.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
)
