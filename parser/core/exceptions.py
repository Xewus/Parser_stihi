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
    def __init__(self, detail: str = 'Ошибка при запуске `Scrapy`') -> None:
        super().__init__(status_code=HTTPStatus.BAD_GATEWAY, detail=detail)


class NoFileException(HTTPException):
    def __init__(self, detail='Файл не найден') -> None:
        super().__init__(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=detail
        )


class NoLinksException(HTTPException):
    def __init__(self, detail='Нет ссылок') -> None:
        super().__init__(
            status_code=HTTPStatus.NO_CONTENT, detail=detail
        )


class BadRequestException(HTTPException):
    """Обработчик ошибки со статус-кодом `400`'
    """
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=detail
        )


class RemoteServerException(HTTPException):
    """Ошибки удалённого сервера.
    """
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail=detail
        )
