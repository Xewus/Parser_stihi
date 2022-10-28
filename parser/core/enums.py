"""Классы с константами.
"""
from enum import Enum


class SpiderNames(str, Enum):
    """Имена пауков.
    """
    ALL_POEMS = 'all-poems'
    LIST_POEMS = 'list-poems'
    CHOOSE_POEMS = 'choose-poems'


class StoreFields(str, Enum):
    """Список сохраняемых полей.
    """
    TITLE = 'title',
    AUTHOR = 'author',
    TEXT = 'text',
    LINK = 'link'


class Tag(str, Enum):
    """Тэги для эндпоинтов.
    """
    INDEX = 'Index'
    PARSING = 'Parsing'
    TEST = 'Test'
    USERS = 'Users'


class DocType(str, Enum):
    """Доступные типы текстовых файлов.
    """
    MD = '.md'
    JSON = '.json'
    DOCX = '.docx'
