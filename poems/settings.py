"""Scrapy settings for poems project.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BOT_NAME = 'poems'

SPIDER_MODULES = ['poems.spiders']
NEWSPIDER_MODULE = 'poems.spiders'

ALLOWED_DOMAINS = ['stihi.ru']
SITE_URL = 'https://stihi.ru'
START_URL_FOR_PARSE = 'https://stihi.ru/avtor'

SCRAPEOPS_API_KEY = os.getenv('SCRAPEOPS_API_KEY')

NAME_BASE_SPIDER = 'poems'
NAME_ALL_POEMS_SPIDER = 'all-poems'
NAME_LIST_POEMS_SPIDER = 'list-poems'
NAME_CHOOSE_POEMS_SPIDER = 'choose-poems'

CONCURRENT_REQUESTS = 2000
CONCURRENT_REQUESTS_PER_DOMAIN = 2000
DNS_TIMEOUT = 5
DOWNLOAD_DELAY = .04
ROBOTSTXT_OBEY = False

# Retry many times since proxies often fail
RETRY_TIMES = 5

# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

ITEM_PIPELINES = {
    'poems.pipelines.JsonAllPoemsTitlePipeline': 300,
}

SCRAPEOPS_API_KEY = 'afc25c0b-1360-4ba6-badf-f8110e7ae9ed'

EXTENSIONS = {
    'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
}

DOWNLOADER_MIDDLEWARES = {
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy_proxies.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
PROXY_LIST = BASE_DIR + '/proxy_list.txt'

# Proxy mode
# 0 = Every requests have different proxy
# 1 = Take only one proxy from the list and assign it to every requests
# 2 = Put a custom proxy to use in the settings
PROXY_MODE = 0
