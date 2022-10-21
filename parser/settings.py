"""Настройки для `Scrapy`
"""
from core.settings import BASE_DIR, PROXY_LIST, USER_AGENTS  # noqa

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


# JSONRPC_ENABLED = True
# JSONRPC_LOGFILE = BASE_DIR / 'web_log.txt'
# JSONRPC_PORT= [6666]
# JSONRPC_HOST = '127.0.0.1'

