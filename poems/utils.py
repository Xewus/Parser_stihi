"""Вспомогательные функции для парсинга.
"""
from poems.settings import ARGS_SEPARATOR, SITE_URL


def clean_poem_text(text: list) -> str:
    """Отрезает текст стиха от нижележащих примечаний.

    #### Args:
        text (list): Текст стиха.

    #### Returns:
        text (str): Обрезанный текст стиха.
    """
    counter = 0
    for index, line in enumerate(text):
        counter = counter + 1 if line == '\n' else 0
        if counter == 3:
            text = text[:index]
    return ''.join(text)


def clean_urls(urls: str) -> list:
    """Выбирает подходящие url`ы.

    Args:
        urls (str): _description_

    Returns:
        list: _description_
    """
    return [
        url for url in urls.split(ARGS_SEPARATOR) if url.startswith(SITE_URL)
    ]
