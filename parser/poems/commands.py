"""Команды для запуска парсеров.
"""
import os

from core.settings import POEMS_STORE
from core.utils import dir_manager


async def start_spider(
    spider: str, author: str, urls: str | None = None
) -> None:
    """Запускает паука.

    #### Args:
    - spider (str): Имя паука.
    - author (str):: Аргументы для запуска паука.
    - urls (str | None, optional): Список `url`ов, если необходим.
    """
    result_dir = dir_manager()
    result_file = result_dir / (POEMS_STORE % author)

    if not urls:
        command = f'scrapy crawl {spider} -a author={author} -a result_file={result_file} --nolog'
    else:
        command = 'scrapy crawl '
        f'{spider} -a author={author} -a urls={urls} --nolog'

    os.system(command=command)
