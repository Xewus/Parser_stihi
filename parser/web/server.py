from pprint import pprint
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from core.settings import HEADERS, WEB_SCRAPY_PORT, WEB_SCRAPY_HOST
from core import constants as cnst


from parser.poems.commands import start_spider

def check_app_key(request: Request) -> bool:
    return request.headers.get(cnst.APP_KEY) == HEADERS[cnst.APP_KEY]


async def test_server(request: Request) -> Response:
    data = {cnst.SERVER_SCRAPY: cnst.OK}
    if not check_app_key(request):
        data[cnst.SERVER_SCRAPY] = cnst.APP_KEY
    return web.json_response(data)



async def parse(request: Request):
    body = await Request.json()
    print(body)


app = web.Application()
app.add_routes([
    web.get('/test', test_server),
    web.post('/scrapy', parse)
])

set_app = {'app': app, 'host': WEB_SCRAPY_HOST, 'port': WEB_SCRAPY_PORT}
