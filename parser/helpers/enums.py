from enum import Enum


class SpiderNames(str, Enum):
    ALL_POEMS = 'all-poems'
    LIST_POEMS = 'list-poems'
    CHOOSE_POEMS = 'choose-poems'


class Tag(str, Enum):
    """Тэги для эндпоинтов.

    INDEX: Главная страница
    USERS: Пользователи
    PARSING: Парсинг
    """
    INDEX = 'Index'
    USERS = 'Users'
    PARSING = 'Parsing'
