"""Валидаторы.
"""
from random import choice
from core.settings import (ARGS_SEPARATOR, HEADERS, SITE_URL,
                           START_URL_FOR_PARSE, USER_AGENTS)
from core.utils import SendRequest


def validate_headers(key: str, value: str) -> tuple[bool, str | None]:
    """Проверяет заголовки.

    #### Args:
    - key (str): Имя заголовка.
    - value (str): Полученное значение заголовка.

    #### Returns:
    - tuple[bool, str | None]: Допустимый ли заголовок и описание ошибки.
    """
    if HEADERS.get(key) == value:
        return True, None
    return False, 'Application key'


async def validate_author(author: str) -> tuple[str, str | None]:
    """Проверяет доступность сервера и наличие автора.

    #### Args:
    - author (str): Автор.

    #### Returns:
    - tuple[bool, str | None]: Результат проверки
    """
    author = author.split('/')[-1]
    url = f'{START_URL_FOR_PARSE}/{author}'
    headers = {
        'Connection': 'keep-alive',
        'Host': 'stihi.ru',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': choice(USER_AGENTS)
    }
    request = SendRequest(url=url, headers=headers)
    response = await request.GET
    
    if response is None or not response.ok:
        return '', 'Remote server failure'
    text = await response.text()
    if 'Автор не найден' in text:
        return '', 'Wrong author'
    return author, None


def validate_urls(
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
