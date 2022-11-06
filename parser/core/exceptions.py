"""Обработчики ошибок.
"""
from pathlib import Path
from typing import Any
from fastapi import status
from fastapi.exceptions import HTTPException


class BadRequestException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Данные из запроса не могут быть обработаны'
    headers = None

    def __init__(
        self,
        status_code: int | None = None,
        detail: str | None = None,
        headers: dict[str, Any] | None = None
    ) -> None:
        self.status_code = status_code or self.status_code
        self.detail = detail or self.detail
        super().__init__(status_code, detail, headers)


class AuthException(BadRequestException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Нет прав для доступа'


class NoFileException(BadRequestException):
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, file: str | Path) -> None:
        super().__init__(detail='Фвйл `%s` не найден' % file)
    

class NoLinksException(BadRequestException):
    status_code=status.HTTP_204_NO_CONTENT
    detail='Нет ссылок'


class NoValidPasswordException(BadRequestException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Пароль не безопасен'


class RemoteServerException(BadRequestException):
    status_code=status.HTTP_502_BAD_GATEWAY
    detail="Ошибки удалённого сервера"


class ScrapyException(RemoteServerException):
    detail: str = 'Ошибка при запуске `Scrapy`'


class TokenException(NoValidPasswordException):
    detail='Неверный токен',
    headers={"WWW-Authenticate": "Bearer"}
