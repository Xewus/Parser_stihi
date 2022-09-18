"""Парсеры с различными настройками для домена `stihi.ru`.
"""
from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from app_core import settings, utils, xpaths
from poems.items import ListPoemsItem, PoemItem


class BasePoemsSpider(Spider):
    name = settings.NAME_BASE_SPIDER
    rotate_user_agent = True
    allowed_domains = settings.ALLOWED_DOMAINS
    site_url = settings.SITE_URL
    author_url = settings.START_URL_FOR_PARSE

    def __init__(self, author: str, *args, **kwargs):
        super(BasePoemsSpider, self).__init__(*args, **kwargs)
        self.author = author
        self.start_urls = [f'{self.author_url}/{author}']

    def parse(self, response: HtmlResponse):
        raise Exception('Implement parse')


class AllPoemsTittleSpider(BasePoemsSpider):
    """Собирает названия и ссылки на все стихи указанного автора.
    """
    name = settings.NAME_LIST_POEMS_SPIDER

    def parse(self, response: HtmlResponse):
        """Парсит страницу автора, переходит по страницам со списками его произведений.
        """
        page = response.xpath(xpaths.body_page)
        # name_author = page.xpath(xpaths.title_page).get()
        amount_poems = response.xpath(xpaths.amount_poems).get()
        amount_poems = 0 if amount_poems is None else int(amount_poems)

        all_pages = [
            f'{self.start_urls[0]}&s={i}' for i in range(0, amount_poems, 50)
        ]
        for page in all_pages:
            yield response.follow(page, callback=self.parse_page)

    def parse_page(self, response: HtmlResponse):
        """Собирает заголовки и ссылки на произведения.
        """
        for poem_link in response.xpath(xpaths.poem_link):
            yield ListPoemsItem(
                title=poem_link.xpath('text()').get(),
                link=self.site_url + poem_link.xpath('.//@href').get()
            )


class AllPoemsSpider(AllPoemsTittleSpider):
    """Собирает все стихи указанного автора.
    """
    name = settings.NAME_ALL_POEMS_SPIDER

    def parse_page(self, response: HtmlResponse):
        """Собирает ссылки на произведения и переходит по ним.
        """
        for poem_link in response.xpath(xpaths.poem_link):
            poem_link = self.site_url + poem_link.xpath('.//@href').get()
            yield response.follow(poem_link, callback=self.parse_poem)

    def parse_poem(self, response: HtmlResponse):
        """Собирает название, автора и текст.
        """
        page = response.xpath(xpaths.body_page)
        yield PoemItem(
            title=page.xpath(xpaths.title_page).get(),
            author=page.xpath(xpaths.author_on_poem_page).get(),
            text=utils.clean_poem_text(
                page.xpath(xpaths.poem_text).getall()
            )
        )


class ChooseSpider(AllPoemsSpider):
    """Собирает избранные стихи.
    """
    name = settings.NAME_CHOOSE_POEMS_SPIDER

    def __init__(self, urls: str, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        urls = urls.split(settings.ARGS_SEPARATOR)
        self.start_urls = urls

    def parse(self, response: HtmlResponse):
        """Переходит по переданному списку ссылок со избранными стихами.
        """
        for poem in self.start_urls:
            yield response.follow(poem, callback=self.parse_poem)
