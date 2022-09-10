"""Вспомогательные функции.
"""
import json

from app_core import settings

TEXT = settings.TEXT
AUTHOR = settings.AUTHOR
TITLE = settings.TITLE
LINK = settings.LINK


def extract_author(dirty_string: str) -> str | None:
    """Вытаскивает имя автора из URL-строки.

    #### Args:
        dirty_string (str): URL-строка, содержащая автора.

    #### Returns:
        str | None: Автор.
    """
    dirty_list = dirty_string.split('/')
    if len(dirty_list) == 1:
        return dirty_list[0]

    for i, v in enumerate(dirty_list):
        if v == 'avtor' and i < len(dirty_list) - 1:
            return (dirty_list[i + 1])
    return None


def clean_poem_text(text: list) -> str:
    """Отрезает текст стиха от нижележащих примечаний.

    #### Args:
        text (list): Текст стиха.

    #### Returns:
        text (str): Обрезанный текст стиха.
    """
    n = 0
    for index, line in enumerate(text):
        n = n + 1 if line == '\n' else 0
        if n == 2:
            text = text[:index]
    return ''.join(text)


def create_choice_list() -> list[tuple[str, str]]:
    """Создаёт список для показа чек-боксов выбора в темплейте.

    Returns:
        list[tuple[str, str]]: Созданный список.
    """
    try:
        with open(settings.POEMS_STORE) as file_json:
            data = json.load(file_json)
            poems = [(d[LINK], d[TITLE]) for d in data]
    except FileNotFoundError:
        poems = []
    return poems
