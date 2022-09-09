"""Вспомогательные функции.
"""
import json

from app_core import settings

TEXT = settings.TEXT
AUTHOR = settings.AUTHOR
TITLE = settings.TITLE
LINK = settings.LINK


def extract_author(dirty_string: str) -> str:
    """Вытаскивает имя автора из URL-строки.

    #### Args:
        dirty_string (str): URL-строка, содержащая автора.

    #### Raises:
        Exception: Автор не найлен.

    #### Returns:
        str: Автор.
    """
    dirty_list = dirty_string.split('/')
    if len(dirty_list) == 1:
        return dirty_list[0]

    for i, v in enumerate(dirty_list):
        if v == 'avtor' and i < len(dirty_list) - 1:
            return (dirty_list[i + 1])

    raise Exception(f'no author in {dirty_list}')


def clean_poem_text(text: list) -> list:
    """Отрезает текст стиха от нижележащих примечаний.

    #### Args:
        text (list): Текст стиха.

    #### Returns:
        text (list): Обрезанный текст стиха.
    """
    n = 0
    for index, line in enumerate(text):
        n = n + 1 if line == '\n' else 0
        if n == 2:
            text = text[:index]
    return text


def create_choice_list() -> list[tuple[str, str]]:
    """Создаёт список для показа чек-боксов выбора в темплейте.
    """
    try:
        with open(settings.POEMS_STORE) as file_json:
            data = json.load(file_json)
            poems = sorted(
                ((d[LINK], d[TITLE]) for d in data),
                key=settings.SORT_KEY_CHOOSE_BY_TITLE
            )
    except Exception:
        poems = []
    return poems
