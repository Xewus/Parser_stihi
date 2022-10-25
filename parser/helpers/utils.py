"""Вспомогательные функции.
"""
import shutil
from datetime import datetime, timedelta
from parser.settings import DATE_FORMAT, RESULT_DIR
from pathlib import Path


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


def dir_manager() -> Path:
    """Создаёт папку для сохранения результатов парсинга и удалет устаревшую.

    Создаётся папка для текущей даты.
    Вчерашняя папка остаётся из-за 'проблемы 23:59:59'.
    Позавчерашняя папка удаляется.

    Returns:
        Path: `URI` папки.
    """
    today = datetime.today()
    two_days_ago = today - timedelta(days=2)
    today = today.strftime(DATE_FORMAT)
    two_days_ago = two_days_ago.strftime(DATE_FORMAT)

    today_dir = Path(RESULT_DIR % today)
    two_days_ago_dir = Path(RESULT_DIR % two_days_ago)

    if two_days_ago_dir.exists():
        shutil.rmtree(two_days_ago_dir)
    if not today_dir.exists():
        today_dir.mkdir()
    return today_dir
