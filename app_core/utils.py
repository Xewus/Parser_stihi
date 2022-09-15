"""Вспомогательные функции.
"""
import json
from time import time

from app_core.settings import (DEFAULT_AMOUNT_TRIES, LINK, POEMS_STORE,
                               TIME_BLOCK_IP, TITLE)


def extract_author(dirty_string: str) -> str | None:
    """Выделяет имя автора из URL-строки.

    #### Args:
        dirty_string (str): URL-строка, содержащая автора.

    #### Returns:
        str | None: Автор.
    """
    dirty_list = dirty_string.split('/')
    if len(dirty_list) == 1:
        return dirty_list[0]

    for i, v in enumerate(dirty_list):
        if v == 'avtor' and i < len(dirty_list) - 1:
            return (dirty_list[i + 1])
    return None


def clean_poem_text(text: list) -> str:
    """Отрезает текст стиха от нижележащих примечаний.

    #### Args:
        text (list): Текст стиха.

    #### Returns:
        text (str): Обрезанный текст стиха.
    """
    counter = 0
    for index, line in enumerate(text):
        counter = counter + 1 if line == '\n' else 0
        if counter == 2:
            text = text[:index]
    return ''.join(text)


def create_choice_list() -> list[tuple[str, str]]:
    """Создаёт список для показа чек-боксов выбора в темплейте.

    Returns:
        list[tuple[str, str]]: Созданный список.
    """
    try:
        with open(POEMS_STORE) as file_json:
            data = json.load(file_json)
            poems = [(d[LINK], d[TITLE]) for d in data]
    except FileNotFoundError:
        poems = []
    return poems


class AllowTries:
    """Хранит и считает попытки входа.

    При привышении допустимого количества - блокирует IP на указанное время.

    #### Attrs
    - store (dict): Хранилище {IP: (количество попыток, время ограничения)}
    - time_limit (int):
        Время (в секундах), допускающее указанное количество попыток.
    - tries (int): Допустимое количество попыток входа.
    """
    store = {}
    time_limit = TIME_BLOCK_IP
    tries = DEFAULT_AMOUNT_TRIES

    def __init__(
        self,
        store: dict | None = None,
        time_limit: int | None = None,
        tries: int | None = None
    ) -> None:
        if store is not None:
            self.store = store
        if time_limit is not None:
            self.time_limit = time_limit
        if tries is not None:
            self.tries = tries

    def __call__(self, key: str, action, *args) -> bool:
        if key not in self.store or self.store[key][1] < time():
            self.store[key] = [1, int(time()) + self.time_limit]
            return True

        self.store[key][0] += 1
        if self.store[key][0] >= self.tries:
            action(*args)
