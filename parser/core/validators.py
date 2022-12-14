"""Валидаторы.
"""
from parser.core.exceptions import (BadRequestException, NoFileException,
                                    RemoteServerException)
from parser.core.requests import SendRequest
from parser.settings import START_URL_FOR_PARSE
from pathlib import Path


async def validate_author(author: str) -> str:
    """Проверяет доступность удалённого сервера и наличие автора.

    #### Args:
    - author (str): Автор.

    #### Returns:
    - author(str):  Автор.
    """
    request = SendRequest(url=START_URL_FOR_PARSE + author)
    response = await request.GET

    if response is None or not response.ok:
        raise RemoteServerException(
            'Сервер вернул неожиданный ответ на запрос: %s' % request.url
        )
    text = await response.text()
    if 'Автор не найден' in text:
        raise BadRequestException('Автор не найден')
    return author


async def valdate_file(file: Path) -> None:
    """Проверяет, существует ли указанный файл.

    #### Args:
    - file (Path): Искомый файл.
    """
    if not file.exists():
        raise NoFileException(file=file)
