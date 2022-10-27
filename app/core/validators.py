"""Валидаторы.
"""
from app.core.settings import START_URL_FOR_PARSE
from app.core.requests import SendRequest
from app.core.exceptions import BadRequestException, RemoteServerException


async def validate_author(author: str) -> None:
    """Проверяет доступность сервера и наличие автора.

    #### Args:
    - author (str): Автор.
    """
    author = author.split('/')[-1]

    request = SendRequest(url=START_URL_FOR_PARSE + author)
    response = await request.GET

    if response is None or not response.ok:
        raise RemoteServerException('Удалённый сервер вернул некорректный ответ')
    text = await response.text()
    if 'Автор не найден' in text:
        raise BadRequestException('Автор не найден')
    return
