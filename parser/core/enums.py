from enum import Enum

class SpiderNames(str, Enum):
    """Имена пауков.

    - ALL_POEMS: Собирает все стихи с текстами.
    - LIST_POEMS: Собирает названия симхов с ссылками на них.
    - CHOOSE_POEMS: Собирает выбранные стихи.
    """
    ALL_POEMS = 'all-poems'
    LIST_POEMS = 'list-poems'
    CHOOSE_POEMS = 'choose-poems'


class StoreFields(str, Enum):
    """Список сохраняемых полей.

    - TITLE: Название стиха.
    - AUTHOR: Автор стиха.
    - TEXT: Текст стиха.
    - LINK: Ссылка на стих.
    """
    TITLE = 'title',
    AUTHOR = 'author',
    TEXT = 'text',
    LINK = 'link'


class Tag(str, Enum):
    """Тэги для эндпоинтов.

    - INDEX: Главная страница
    - USERS: Пользователи
    - PARSING: Парсинг
    """
    DEFAULT = ''
    INDEX = 'Index'
    PARSING = 'Parsing'
    SCRAPY = 'Scrapy'
    TEST = 'Test'
    USERS = 'Users'


class DocType(str, Enum):
    MD = '.md'
    JSON = '.json'
    DOCX = '.docx'
