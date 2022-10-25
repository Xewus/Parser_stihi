"""Настройки для параметров приложения.
"""
from pathlib import Path

from decouple import config

DEBUG = config('DEBUG', default=False)

DATE_FORMAT = config('DATE_FORMAT', default='%y_%m_%d')

BASE_DIR =         Path(__file__).resolve().parent
PROXY_LIST =       BASE_DIR / 'helpers/proxy_list.txt'
USER_AGENTS_LIST = BASE_DIR / 'helpers/user_agents_list.txt'

# |_ */<project>/27_05_21_results/
#   |_oleg_choose-poems.json
#   |_ivan_all-poems.json
#   |_...
# |_ */<project>/28_05_21_results/
RESULT_DIR =  str(BASE_DIR) + '/%s_results'
POEMS_STORE = '%s_%s.json'
DATE_FORMAT = config('DATE_FORMAT')

ARGS_SEPARATOR = '#'

# Настройки для FastAPI
APP_NAME =         config('APP_NAME')
APP_DESCRIPTION =  'API для запуска парсера сайта ***Stihi.ru***'
APP_VERSION =      '1.1.0'
WEB_SCRAPY_HOST =  config('WEB_SCRAPY_HOST', default='127.0.0.1')  # Хост, на котором будет запущено приложение.
WEB_SCRAPY_PORT =  config('WEB_SCRAPY_PORT', default=8765)         # Порт, на котором будет запущено приложение.
APP_KEY =          config('APP_KEY')                               # Елюч досьупа к приложению.

# Настройки `Scrapy'`
BOT_NAME =            'poems'

SPIDER_MODULES =      ['parser.poems.spiders']

LOG_LEVEL =           'ERROR' if not DEBUG else 'INFO'

ALLOWED_DOMAINS =     ['stihi.ru']
SITE_URL =            'https://stihi.ru'
START_URL_FOR_PARSE = SITE_URL + '/avtor'

with open(USER_AGENTS_LIST) as f:
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
