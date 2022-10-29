"""Обработчики ошибок.
"""
from fastapi import status

from fastapi.exceptions import HTTPException


class ScrapyException(HTTPException):
    def __init__(self, detail: str = 'Ошибка при запуске `Scrapy`') -> None:
        super().__init__(status_code=status.BAD_GATEWAY, detail=detail)


class NoFileException(HTTPException):
    def __init__(self, file='') -> None:
        super().__init__(
            status_code=status.INTERNAL_SERVER_ERROR,
            detail='Ффйл `%s` не найден' % file
        )


class NoLinksException(HTTPException):
    def __init__(self, detail='Нет ссылок') -> None:
        super().__init__(
            status_code=status.NO_CONTENT, detail=detail
        )


class BadRequestException(HTTPException):
    """Обработчик ошибки со статус-кодом `400`'
    """
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.BAD_REQUEST,
            detail=detail
        )


class RemoteServerException(HTTPException):
    """Ошибки удалённого сервера.
    """
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.BAD_GATEWAY,
            detail=detail
        )
