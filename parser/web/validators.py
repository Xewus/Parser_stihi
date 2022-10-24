"""Валидаторы данных.
"""
from parser.settings import APP_KEY
from parser.web.exceptions import AppKeyException


def app_key_validator(app_key: str) -> bool:
    """Проверяет разрешение по заголовку.

    #### Args:
    - app_key (str): Объект запроса.

    #### Returns:
    - bool: Пройдена ли проверка.
    """
    if not app_key == APP_KEY:
        raise AppKeyException(app_key)
