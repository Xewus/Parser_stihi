"""Команды для запуска парсеров.
"""
import os
from parser.helpers.utils import dir_manager
from parser.settings import POEMS_STORE
from pathlib import Path


async def start_spider(
    spider: str, author: str, urls: str | None = None
) -> str:
    """Запускает паука.

    #### Args:
    - spider (str): Имя паука.
    - author (str):: Аргументы для запуска паука.
    - urls (str | None, optional): Список `url`ов, если необходим.

    #### Returns:
    - str: Расположение сохранённого файла.
    """
    result_dir = dir_manager()
    result_file = result_dir / (POEMS_STORE % (author, spider))

    command = f'scrapy crawl {spider} -a author={author} -a result_file={result_file}'
    if urls:
        command += f' -a urls={urls}'
    print(command)
    os.system(command=command)
    return str(result_file)
