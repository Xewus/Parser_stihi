"""Команды для запуска парсеров.
"""
import os
from parser.core.exceptions import NoFileException, ScrapyException
from parser.core.utils import get_result_file
from pathlib import Path


async def start_spider(
    spider: str, author: str, urls: str | None = None
) -> Path:
    """Запускает паука.

    #### Args:
    - spider (str): Имя паука.
    - author (str):: Имя автора.
    - urls (str | None, optional): Список `url`ов, если необходим.
        Note: `Scrapy` принимает только строковые аргументы.

    #### Raises:
    - FileNotFoundError: Отсутствует файл с результатами.
    - ScrapyException: Ошибка при попытке выполнить команду.

    #### Returns:
    - str: Расположение сохранённого файла.
    """
    file = await get_result_file(author, spider)
    command = f'scrapy crawl {spider} -a author={author} -a result_file={file}'
    if urls:
        command += f' -a urls={urls}'
    try:
        os.system(command=command)
    except Exception as exc:
        raise ScrapyException(exc.args)

    if not file.exists():
        raise NoFileException(file=file)
    return file
