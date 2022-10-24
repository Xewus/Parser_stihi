"""Обработчики ошибок.
"""
from http import HTTPStatus

from fastapi.exceptions import HTTPException


class AppKeyException(HTTPException):
    def __init__(self, app_key: str) -> None:
        super().__init__(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Неверный `app-key`: %s' % app_key
        )

class ScrapyException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=502,
            detail='Ошибка при запуске `Scrapy`'
        )
