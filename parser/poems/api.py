from crypt import methods
import json
from .commands import COMMANDS, start_spider
from .helpers.utils import clean_urls
from .settings import (AUTH_KEY, START_URL_FOR_PARSE, USER_AGENTS,
                             Config, SpiderNames)
from random import choice

import requests
from flask import Flask, request

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/test/', methods=['GET'])
def test() -> str:
    return json.dumps({'status': 200})


@app.route('/scrapy/', methods=['GET'])
def parse() -> str:
    """Принимает команды для запуска парсеров.

    Example:
        http://127.0.0.1:5000/scrapy/?spider=all-poems&author=ivanov

    Returns:
        str: _description_
    """
    if request.headers.get('AUTH_KEY') != AUTH_KEY:
        return json.dumps({'error': 'Wrong AUTH_KEY'})

    spider = request.args.get('spider')
    author = request.args.get('author')

    if not spider or not author:
        return json.dumps({'error': 'Wrong query'})

    if spider not in SpiderNames:
        return json.loads({'error': 'Wrong spider'})

    target_url = f'{START_URL_FOR_PARSE}/{author}'
    headers = {
        'Connection': 'keep-alive',
        'Host': 'stihi.ru',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': choice(USER_AGENTS)
    }
    try:
        response = requests.get(target_url, headers=headers, timeout=1)
    except requests.exceptions.ConnectionError:
        return json.dumps({'error': 'Remote server failure'})

    if not response.ok or 'Автор не найден' in response.text:
        return json.dumps({'error': 'Wrong author'})

    if spider == SpiderNames.CHOOSE_POEMS:
        urls = clean_urls(request.args.get('urls'))
        if not urls:
            return json.dumps({'error': 'Wrong query'})
        command = COMMANDS[spider] % (author, urls)
    else:
        command = COMMANDS[spider] % author

    start_spider(command)

    return json.dumps({'auyhor': author, 'spider': spider})
