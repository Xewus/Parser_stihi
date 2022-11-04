"""Классы с константами.
"""
from enum import Enum


class DocType(str, Enum):
    """Доступные типы текстовых файлов.
    """
    DOCX = '.docx'
    JSON = '.json'
    MD = '.md'


class SpiderNames(str, Enum):
    """Имена пауков.
    """
    ALL_POEMS = 'all-poems'
    CHOOSE_POEMS = 'choose-poems'
    LIST_POEMS = 'list-poems'


class StoreFields(str, Enum):
    """Список сохраняемых полей.
    """
    AUTHOR = 'author'
    LINK = 'link'
    TEXT = 'text'
    TITLE = 'title'


class Tag(str, Enum):
    """Тэги для эндпоинтов.
    """
    INDEX = 'Index'
    PARSING = 'Parsing'
    TEST = 'Test'
    USERS = 'Users'
