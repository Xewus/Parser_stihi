"""Обработчики ошибок.
"""
from fastapi import status
from fastapi.exceptions import HTTPException


<<<<<<< HEAD
class ScrapyException(HTTPException):
    def __init__(self, detail: str = 'Ошибка при запуске `Scrapy`') -> None:
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY, detail=detail
=======
class AuthException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Нет прав для доступа'
        )


class BadRequestException(HTTPException):
    """Обработчик ошибки со статус-кодом `400`'
    """
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
>>>>>>> users
        )


class NoFileException(HTTPException):
    def __init__(self, file='') -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ффйл `%s` не найден' % file
        )


class NoLinksException(HTTPException):
    def __init__(self, detail='Нет ссылок') -> None:
        super().__init__(
            status_code=status.HTTP_204_NO_CONTENT, detail=detail
        )


class RemoteServerException(HTTPException):
    """Ошибки удалённого сервера.
    """
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=detail
        )


class ScrapyException(HTTPException):
    def __init__(self, detail: str = 'Ошибка при запуске `Scrapy`') -> None:
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY, detail=detail
        )


class TokenException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный токен',
            headers={"WWW-Authenticate": "Bearer"},
        )
<<<<<<< HEAD


class AuthException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Нет прав для доступа'
        )
=======
>>>>>>> users
