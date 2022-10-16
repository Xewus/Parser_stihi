"""Вспомогательные функции для парсинга.
"""
from ..settings import ARGS_SEPARATOR, SITE_URL


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


def clean_urls(
    urls: str, sep: str = ARGS_SEPARATOR, site: str = SITE_URL
) -> list[str]:
    """Выбирает подходящие url`ы.

    #### Args:
    - urls (str): Строка содержащая адреса, разделённые определённым знаком.
    - sep (str, optional): Знак разделяющий адреса.
    - site (str, optional): Разрешённый домен.

    #### Returns:
    - list[str]: Список адресов.
    """
    return [
        url for url in urls.split(sep) if url.startswith(site)
    ]
