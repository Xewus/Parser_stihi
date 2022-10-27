from fastapi.exceptions import HTTPException
from http import HTTPStatus


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
