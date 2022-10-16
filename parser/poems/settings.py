"""Настройки для `Scrapy`
"""
import os
from collections import namedtuple
from pathlib import Path

AUTH_KEY = 'qwerty'

BASE_DIR = Path(__file__).resolve().parent
RESULT_DIR = BASE_DIR.parent / 'results'

RESULT_DIR.mkdir(exist_ok=True)

# Сохранение результатов
POEMS_STORE = f'{RESULT_DIR}/%s_poems.json'
OUT_POEMS = f'{RESULT_DIR}/out_for_%s'
OUT_FORMATS = ('.md', '.json', '.docx')

# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
PROXY_LIST = BASE_DIR / 'helpers/proxy_list.txt'

USER_AGENTS_LIST = BASE_DIR / 'helpers/user_agents_list.txt'


class Config:
    FLASK_APP = os.environ.get('FLASK_APP')
    DEBUG = os.environ.get('DEBUG', default=False)
    ENV = os.environ.get('ENV', default='production')
    SECRET_KEY = "os.environ.get('SECRET_KEY')"

print(Config.FLASK_APP)

BOT_NAME = 'poems'

SPIDER_MODULES = ['poems.spiders']
# NEWSPIDER_MODULE = 'poems.spiders'

ALLOWED_DOMAINS = ['stihi.ru']
SITE_URL = 'https://stihi.ru'
START_URL_FOR_PARSE = 'https://stihi.ru/avtor'

ARGS_SEPARATOR = '#'
# Названия пауков
SpiderNames = namedtuple(
    'SpiderNames', ['ALL_POEMS', 'LIST_POEMS', 'CHOOSE_POEMS']
)
SpiderNames = SpiderNames(
    ALL_POEMS='all-poems',
    LIST_POEMS='list-poems',
    CHOOSE_POEMS='choose-poems'
)

# Названия сохраняемых полей
StoreFields = namedtuple(
    'StoreFields', ['TITLE', 'AUTHOR', 'TEXT', 'LINK']
)
StoreFields = StoreFields(
    TITLE='title',
    AUTHOR='author',
    TEXT='text',
    LINK='link'
)

ITEM_PIPELINES = {
    'poems.pipelines.JsonAllPoemsTitlePipeline': 300,
}

CONCURRENT_REQUESTS = 2000
CONCURRENT_REQUESTS_PER_DOMAIN = 2000
DNS_TIMEOUT = 5
DOWNLOAD_DELAY = .05
ROBOTSTXT_OBEY = False

# Retry many times since proxies often fail
RETRY_TIMES = 5

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

# the default user_agent_list composes
# chrome,I E,firefox,Mozilla,opera,netscape
# for more user agent strings,
# you can find it in http://www.useragentstring.com/pages/useragentstring.php
USER_AGENTS = None

with open(USER_AGENTS_LIST) as f:
    USER_AGENTS = [line.rstrip() for line in f.readlines()]
