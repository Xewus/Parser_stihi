"""Вспомогательные функции.
"""
import json
import shutil
from datetime import datetime, timedelta
from parser.core.enums import StoreFields
from parser.core.exceptions import NoLinksException
from parser.settings import DATE_FORMAT, POEMS_STORE, RESULT_DIR
from pathlib import Path

from pydantic import HttpUrl


def clean_poem_text(text: list[str]) -> str:
    """Отрезает текст стиха от нижележащих примечаний.

    #### Args:
    - text (list[str]): Текст стиха.

    #### Returns:
    - text (str): Текст стиха.
    """
    counter = 0
    for index, line in enumerate(text):
        counter = counter + 1 if line == '\n' else 0
        if counter == 3:
            text = text[:index]
    return ''.join(text)


async def get_result_file(author: str, spider: str) -> Path:
    """Создаёт папку для сохранения результатов парсинга и удалет устаревшую.

    Создаётся папка для текущей даты.
    Вчерашняя папка остаётся из-за 'проблемы 23:59:59'.
    Позавчерашняя папка удаляется.

    #### Returns:
    - Path: `URI` папки.

    #### Example:
    - /parser/results/2022_10_15/
    """
    today = datetime.today()
    two_days_ago = (today - timedelta(days=2))

    today_dir = Path(RESULT_DIR % today.strftime(DATE_FORMAT))
    two_days_ago_dir = Path(RESULT_DIR % two_days_ago.strftime(DATE_FORMAT))

    if two_days_ago_dir.exists():
        shutil.rmtree(two_days_ago_dir)

    today_dir.mkdir(parents=True, exist_ok=True)
    return today_dir / (POEMS_STORE % (author, spider))


async def extract_poem_links(file: str | Path) -> list[dict[str, str | HttpUrl]]:
    with open(file=file) as poems_links:
        poems_links = json.load(poems_links)
        if not poems_links or not poems_links[0].get(StoreFields.LINK.value):
            raise NoLinksException
        return poems_links
