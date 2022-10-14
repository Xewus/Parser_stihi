from flask import Flask, request
import json
import requests
from random import choice


from poems.settings import USER_AGENTS, Config, SpiderNames, START_URL_FOR_PARSE, AUTH_KEY
from poems.commands import COMMANDS, start_spider
from poems.utils import clean_urls


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/scrapy/', methods=['GET'])
def parse():
    if request.headers.get('AUTH_KEY') != AUTH_KEY:
        return json.dumps({'error': 'Wrong AUTH_KEY'})

    spider = request.args.get('spider')
    author = request.args.get('author')

    if not spider or not author:
        return json.dumps({'error': 'Wrong query'})

    if not spider in SpiderNames:
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
