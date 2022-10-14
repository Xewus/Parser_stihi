"""Парсеры с различными настройками для домена `stihi.ru`.
"""
from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from poems.items import ListPoemsItem, PoemItem
from poems import settings, xpaths, utils


class BasePoemsSpider(Spider):
    name = 'BasePoems'
    rotate_user_agent = True
    allowed_domains = settings.ALLOWED_DOMAINS
    site_url = settings.SITE_URL
    author_url = settings.START_URL_FOR_PARSE

    def __init__(self, author: str):
        super(BasePoemsSpider, self).__init__()
        self.author = author
        print('init with author', author)
        self.start_urls = [f'{self.author_url}/{author}']

    def parse(self, response: HtmlResponse):
        raise Exception('Implement parse')


class ListPoemsSpider(BasePoemsSpider):
    """Собирает названия и ссылки на все стихи указанного автора.
    """
    name = settings.SpiderNames.LIST_POEMS

    def parse(self, response: HtmlResponse):
        """Парсит страницу автора, переходит по страницам со списками его произведений.
        """
        print('start parse')
        page = response.xpath(xpaths.body_page)
        # name_author = page.xpath(xpaths.title_page).get()
        amount_poems = int(response.xpath(xpaths.amount_poems).get())

        all_pages = [
            f'{self.start_urls[0]}&s={i}' for i in range(0, amount_poems, 50)
        ]
        for page in all_pages:
            yield response.follow(page, callback=self.parse_page)

    def parse_page(self, response: HtmlResponse):
        """Собирает заголовки и ссылки на произведения.
        """
        i = 0
        for poem_link in response.xpath(xpaths.poem_link):
            i +=1
            print('yeld2', i)
            yield ListPoemsItem(
                title=poem_link.xpath('text()').get(),
                link=self.site_url + poem_link.xpath('.//@href').get()
            )


class AllPoemsSpider(ListPoemsSpider):
    """Собирает все стихи указанного автора.
    """
    name = settings.SpiderNames.ALL_POEMS

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
    name = settings.SpiderNames.CHOOSE_POEMS

    def __init__(self, author: str, urls: str):
        super(BasePoemsSpider, self).__init__(author=author)
        self.start_urls = urls

    def parse(self, response: HtmlResponse):
        """Переходит по переданному списку ссылок со избранными стихами.
        """
        for poem in self.start_urls:
            yield response.follow(poem, callback=self.parse_poem)
