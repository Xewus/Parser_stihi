"""Команды для запуска парсеров.
"""
import os


async def start_spider(spider: str, author: str, urls: str | None = None) -> None:
    """Запускает паука.

    #### Args:
    - spider (str): Имя паука.
    - author (str):: Аргументы для запуска паука.
    - urls (str | None, optional): Список `url`ов, если необходим.
    """
    if not urls:
        command = f'scrapy crawl {spider} -a author={author} --nolog'
    else:
        command = f'scrapy crawl {spider} -a author={author} -a urls={urls} --nolog'
    os.system(command=command)
