from turtle import title
from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from app_core import xpaths
from app_core import constants as const


class BasePoemsSpider(Spider):
    name = const.NAME_BASE_SPIDER
    allowed_domains = const.ALLOWED_DOMAINS
    site_url = const.SITE_URL
    author_url = const.START_URL_FOR_PARSE

    def __init__(self, author: str, *args, **kwargs):
        super(BasePoemsSpider, self).__init__(*args, **kwargs)
        find_author = author.split('/')
        if len(find_author) == 1:
            author=find_author[0]
        else:
            for i, v in enumerate(find_author):
                if v == 'avtor':
                    if i < len(find_author) - 2:
                        author = find_author[i + 1]
                    break
            else:
                raise Exception('no author')
        self.start_urls = [f'{self.author_url}/{author}']

    def parse(self, response: HtmlResponse):
        raise Exception('Implement parse')


class AllPoemsTittleSpider(BasePoemsSpider):
    """Собирает названия и ссылки на все стихи указанного автора.
    """
    name = const.NAME_LIST_POEMS_SPIDER

    def parse(self, response: HtmlResponse):
        """Парсит страницу автора и переходит по страницам со списками его произведений.
        """
        about_author = response.xpath(xpaths.about_page)
        name_author = about_author.xpath(xpaths.title_page).get()
        amount_poems = int(response.xpath(xpaths.amount_poems).get())
        print(name_author, amount_poems)
        all_pages = [f'{self.start_urls[0]}&s={i}' for i in range(0, amount_poems, 50)]
        for page in all_pages:
            yield response.follow(page, callback=self.parse_page)
    
    def parse_page(self, response: HtmlResponse):
        """Собирает заголовки и ссылки на произведения.
        """
        for poem_link in response.xpath(xpaths.poem_link):
            yield {
                'title': poem_link.xpath(xpaths.title).get(),
                'link': self.site_url + poem_link.xpath(xpaths.link).get()
            }


class AllPoemsSpider(AllPoemsTittleSpider):
    name = const.NAME_ALL_POEMS_SPIDER

    def parse_page(self, response: HtmlResponse):
        for poem_link in response.xpath(xpaths.poem_link):
            poem_link = self.site_url + poem_link.xpath(xpaths.link).get()
            yield response.follow(poem_link, callback=self.parse_poem)
    
    def parse_poem(self, response: HtmlResponse):
        yield {
            'title': ...
        }
    

class ChoseSpider(BasePoemsSpider):
    name = const.NAME_CHOOSE_POEMS_SPIDER
