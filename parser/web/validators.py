"""Валидаторы данных.
"""
from parser.core.exceptions import AppKeyException
from parser.settings import APP_KEY


def app_key_validator(app_key: str) -> None:
    """Проверяет разрешение по заголовку.

    #### Args:
    - app_key (str): Проверяемый ключ.

    #### Raises:
        AppKeyException: Недопустимый ключ.
    """
    if not app_key == APP_KEY:
        raise AppKeyException(app_key)
