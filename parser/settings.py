"""Настройки параметров приложения.
"""
from pathlib import Path

from decouple import config

DEBUG = config('DEBUG', default=True, cast=bool)

APP_NAME = config('APP_NAME')
APP_DESCRIPTION = '''
Сервис для формирваания запросов к `Scrapy` и выдачи файлов в нужном формате.
'''
APP_VERSION =         '0.4.0'

################################################################################

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATE_FORMAT =         config('DATE_FORMAT', default='%y_%m_%d')

BASE_DIR =            Path(__file__).resolve().parent
PROXY_LIST =          BASE_DIR / 'helpers/proxy_list.txt'
USER_AGENTS_LIST =    BASE_DIR / 'helpers/user_agents_list.txt'
DOCX_TEMPLATES =      BASE_DIR / 'helpers/docx_templates'
USERS_DB =            BASE_DIR / 'helpers/users.json'

if not USERS_DB.exists():
    USERS_DB.touch()

FIRST_USER =          {
    'username': config('USERNAME', default='User'),
    'email': config('EMAIL', default='q@q.qq'),
    'password': config('FIRST_USER_PASSWORD', default='12345678'),
    'active': True,
    'admin': True
}

# |_ */<project>/results/27_05_21/
#   |_oleg_choose-poems.json
#   |_ivan_all-poems.json
#   |_...
# |_ */<project>/results/28_05_21/
RESULT_DIR =  str(BASE_DIR) + '/results/%s/'
POEMS_STORE = '%s_%s.json'

# Строка разделяющая стихи
POEMS_SEPARATOR = '\n' + '-' * 50 + '\n\n'
# Разделитель для перевода списка в строку
ARGS_SEPARATOR = '#'

# _______Настройки `Scrapy'` ________ #
BOT_NAME =            'poems'

SPIDER_MODULES =      ['parser.poems.spiders']

LOG_LEVEL =           'ERROR' if not DEBUG else 'INFO'

ALLOWED_DOMAINS =     ['stihi.ru']
SITE_URL =            'https://stihi.ru/'
START_URL_FOR_PARSE = SITE_URL + 'avtor/'

with open(USER_AGENTS_LIST, 'r', encoding='utf-8') as f:
    USER_AGENTS = [line.rstrip() for line in f.readlines()]

ITEM_PIPELINES = {
    'parser.poems.pipelines.JsonAllPoemsTitlePipeline': 300,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
CONCURRENT_REQUESTS =                  2000
CONCURRENT_REQUESTS_PER_DOMAIN =       2000
DNS_TIMEOUT =                          5
DOWNLOAD_DELAY =                       .05
ROBOTSTXT_OBEY =                       False

# Retry many times since proxies often fail
RETRY_TIMES =                          5

# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy_proxies.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

# Proxy mode
# 0 = Every requests have different proxy
# 1 = Take only one proxy from the list and assign it to every requests
# 2 = Put a custom proxy to use in the settings
PROXY_MODE = 0

##########################################################################
AUTHOR = {
    'name': 'xewus',
    'email': 'xewuss@yandex.ru',
    'url': 'https://github.com/Xewus/Parser_stihi'
}
