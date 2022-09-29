import crochet
crochet.setup()

from flask import Flask
from pony.orm import db_session, select
from werkzeug.middleware.proxy_fix import ProxyFix
from scrapy.crawler import CrawlerRunner

from app_core.settings import FIRST_PASSWORD, FIRST_USERNAME, Config
from poems.spiders import get_spider_by_name, BasePoemsSpider

app = Flask(__name__)
app.config.from_object(Config)
app.wsgi_app = ProxyFix(app.wsgi_app)
crawl_runner = CrawlerRunner()


@crochet.run_in_reactor
def scrape_with_crochet(spider: BasePoemsSpider, author: str):
    user.change_parsing_on(True)
    print('crochet', user)
    eventual = crawl_runner.crawl(spider, author)
    print(eventual)
    eventual.addCallback(finished_scrape, user)


def finished_scrape(user):
    user.change_parsing_on(False)


from . import model, views  # noqa


with db_session:
    """Создаёт первого пользователя, если БД пустая.
    """
    if not len(model.User.select()[:1]):
        model.User(
            username=FIRST_USERNAME,
            password=FIRST_PASSWORD,
            is_active=True,
            is_authenticated=True,
            is_admin=True
        )
    
    users = select(u for u in model.User)
    for user in users:
        user.parsing_on = False
