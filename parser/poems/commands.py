"""Команды для запуска парсеров.
"""
import os
from parser.helpers.utils import dir_manager
from parser.settings import POEMS_STORE


async def start_spider(
    spider: str, author: str, urls: str | None = None
) -> str:
    """Запускает паука.

    #### Args:
    - spider (str): Имя паука.
    - author (str):: Аргументы для запуска паука.
    - urls (str | None, optional): Список `url`ов, если необходим.
        Note: `Scrapy` принимает только строковые аргументы.

    #### Raises:
        FileNotFoundError: Отсутствует файл с результатами.

    #### Returns:
    - str: Расположение сохранённого файла.
    """
    res_dir = dir_manager()
    file = res_dir / (POEMS_STORE % (author, spider))
    command = f'scrapy crawl {spider} -a author={author} -a result_file={file}'
    if urls:
        command += f' -a urls={urls}'

    os.system(command=command)

    if not file.exists():
        raise FileNotFoundError(
            'Ошибка при создании файла с результатами парсинга.'
            f' Файл `{file}` не найден'
        )
    return str(file)
