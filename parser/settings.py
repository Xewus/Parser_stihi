"""Настройки для `Scrapy`
"""
from pathlib import Path

from decouple import config

WEB_SCRAPY_HOST =  config('WEB_SCRAPY_HOST')
WEB_SCRAPY_PORT = config('WEB_SCRAPY_PORT')
APP_KEY = config('APP_KEY')

DEBUG = config('DEBUG')

BASE_DIR = Path(__file__).resolve().parent
PROXY_LIST = BASE_DIR / 'helpers/proxy_list.txt'
USER_AGENTS_LIST = BASE_DIR / 'helpers/user_agents_list.txt'

# '27_05_21_results/author_poems.json'
RESULT_DIR = str(BASE_DIR) + '/%s_results'
POEMS_STORE = '%s_%s.json'
DATE_FORMAT = config('DATE_FORMAT')
OUT_FORMATS = ('.md', '.json', '.docx')

ARGS_SEPARATOR = '#'

ALLOWED_DOMAINS = ['stihi.ru']
SITE_URL = 'https://stihi.ru'
START_URL_FOR_PARSE = SITE_URL + '/avtor'

with open(USER_AGENTS_LIST) as f:
    USER_AGENTS = [line.rstrip() for line in f.readlines()]

BOT_NAME = 'poems'

SPIDER_MODULES = ['parser.poems.spiders']

ITEM_PIPELINES = {
    'parser.poems.pipelines.JsonAllPoemsTitlePipeline': 300,
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
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
LOG_LEVEL = 'ERROR'