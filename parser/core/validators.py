"""Валидаторы.
"""
from parser.core.exceptions import BadRequestException, RemoteServerException
from parser.core.requests import SendRequest
from parser.settings import START_URL_FOR_PARSE


async def validate_author(author: str) -> str:
    """Проверяет доступность сервера и наличие автора.

    #### Args:
    - author (str): Автор.

    #### Returns:
    - author(str):  Автор.

    """
    author = author.rstrip('/').split('/')[-1]
    print(author)
    request = SendRequest(url=START_URL_FOR_PARSE + author)
    response = await request.GET

    if response is None or not response.ok:
        raise RemoteServerException('Сервер `Stihi` вернул неожиданный ответ')
    text = await response.text()
    if 'Автор не найден' in text:
        raise BadRequestException('Автор не найден')
    return author
