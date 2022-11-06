"""Схемы валидации эндпоинтов парсинга.
"""
from datetime import datetime as dt
from parser.core.enums import DocType
from parser.settings import ARGS_SEPARATOR, DATE_FORMAT

from pydantic import BaseModel, Field, HttpUrl, validator

example_date = dt.date(dt.now()).strftime(DATE_FORMAT)


class RespTestSchema(BaseModel):
    """Схема ответа на тестовый запрос.
    """
    server: str = Field(
        default='Ok',
        title='Проверка сервера',
        alias='Server `Scrapy`'
    )

    class Config:
        title = 'Схема ответа для теста сервера'


class AuthorSchema(BaseModel):
    """Общая схема с автором.
    """
    author: str | HttpUrl = Field(
        title='Имя автора',
        description='Имя автора, как указано в `URL` или '
        '`URL` на страницу автора',
        example='oleg'
    )

    class Config:
        schema_extra = {
            'examples': {
                'Ссылка на страницу автора': {
                    'value': 'https://stihi.ru/avtor/oleg/'
                },
                'Имя автора как в ссылке': {
                    'value': 'oleg'
                }
            }
        }

    @validator('author')
    def extract_author(cls, author):
        """Вытаскивает автора, если передан `URL`.
        """
        return author.rstrip('/').split('/')[-1]


class AuthorDocTypeSchema(AuthorSchema):
    """Схема выбора автора и типа скачиваемого файла.
    """
    doc_type: DocType = Field(
        title='Тип скачиваемого файла',
        description='Выбор типа скачиваемого файла из доступных на сервере'
    )

    class Config:
        title = 'Схема выбора автора и типа скачиваемого файла'
        schema_extra = {
            'examples': {
                'С расширением `.json`': {
                    'value': {
                        'author': 'oleg',
                        'doc_type': '.json'
                    }
                },
                'С расширением `.docx`': {
                    'value': {
                        'author': 'https://stihi.ru/avtor/oleg/',
                        'doc_type': '.docx'
                    }
                },
                'С расширением `.md': {
                    'value': {
                        'author': 'oleg',
                        'doc_type': '.md'
                    }
                }
            }
        }


class ChoosedPoemsSchema(AuthorDocTypeSchema):
    """Схема приёма `URL` выбранных для скачивания стихов.
    """
    urls: list[HttpUrl] = Field(
        title='Список ссылок на выбранные стихи',
        example='[https://stihi.ru//2000/08/21-53, ...]'
    )

    class Config:
        title = 'Схема приёма `URL` выбранных для скачивания стихов'
        schema_extra = {
            'example': {
                'author': 'oleg',
                'doc_type': '.docx',
                'urls': [
                    'https://stihi.ru//2012/01/19/2059',
                    'https://stihi.ru//2000/08/21-53',
                    'https://stihi.ru//2000/08/09-81'
                ]
            }
        }

    @validator('urls')
    def urls_validate(cls, urls: list[HttpUrl]):
        return ARGS_SEPARATOR.join(urls)


class RespChoosePoemsSchema(AuthorSchema):
    """Схема со списком доступных для выбора стихов.
    """
    poems: list[dict[str, str | HttpUrl]] = Field(
        title='Список ссылок на стихи',
        description='Названия стихов с ссылками.'
    )

    class Config:
        title = 'Схема ответа для выбора стихов'
        schema_extra = {
            'example': {
                "author": "oleg",
                "poems": [
                    {
                        "title": "Английская колыбельная",
                        "link": "https://stihi.ru//2012/01/19/2059"
                    },
                    {
                        "title": "Ах, если б знал ты, как легко...",
                        "link": "https://stihi.ru//2000/08/21-53"
                    }
                ]
            }
        }
