"""Схемы валидации данных.
"""
from datetime import datetime as dt
from parser.helpers.enums import SpiderNames
from parser.settings import (ARGS_SEPARATOR, DATE_FORMAT, POEMS_STORE,
                             RESULT_DIR)
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, root_validator, validator

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


class ParsingArgsSchema(BaseModel):
    """Схема запроса для старта парсинга.
    """
    spider: SpiderNames = Field(title='Имя паука')
    author: HttpUrl | str = Field(
        title='Имя автора',
        description='Имя автора, как указано в `URL` либо полный `URL`'
    )
    urls: Optional[list[HttpUrl]] = Field(
        title='Список URL`ов выбранных стихов',
        description='Список стихов используется только для '
                    f'паука `{SpiderNames.CHOOSE_POEMS}`'
    )

    class Config:
        title = 'Схема Параметров необходимые для парсинга'
        schema_extra = {
            'examples': {
                'Полный `URL': {
                    'summary': 'Полный URL на страницу автора',
                    'value': {
                        'spider': 'all-poems',
                        'author': 'https://stihi.ru/avtor/oleg'
                    }
                },
                'Только имя': {
                    'summary': 'Только имя из URL страницы автора',
                    'value': {
                        'spider': 'list-poems',
                        'author': 'oleg'
                    }
                },
                'С избранными стихами': {
                    'summary':'Запрос с URL`ами стихов',
                    'value': {
                        'spider': 'choose-poems',
                        'author': 'oleg',
                        'urls': [
                            'https://stihi.ru/2010/05/07/6867',
                            'https://stihi.ru/2012/09/10/9439',
                            'https://stihi.ru/2015/10/10/3770'
                        ]
                    }
                }
            }
        }

    @validator('author')
    def extract_author(cls, author: HttpUrl | str) -> str:
        """Проверяет параметр `author`.
        Если передан в виде `URL` - то выделяет из него автора.

        #### Args:
        - author (HttpUrl | str): Строка, содержащая автора.

        #### Raises:
        - ValueError: Передана пустая строка.

        #### Returns:
        - str: Автор.
        """
        author = author.split('/')[-1]
        if not author:
            raise ValueError('Нет автора')
        return author

    @validator('urls')
    def urls_validator(cls, urls: list[HttpUrl]) -> str:
        """Преобразует список в строку-аргумент для `Scrapy`.

        #### Args:
        - urls (list[HttpUrl]): Спсок URL стихов.

        #### Returns:
        - str: Строка с URL стихов.
        """
        return ARGS_SEPARATOR.join(url.strip() for url in urls)

    @root_validator
    def url_for_spider(cls, values: dict) -> dict:
        """Проверяет, соответствие списка стихов с пауком.

        #### Args:
        - values (dict): Параметры для пауков.

        #### Raises:
        - ValueError: Отсутствует список стихов для паука.
        - ValueError: Передан список стихов с несоответствующим пауком.
        
        #### Returns:
        - dict: Проверенные параметры для паука.
        """
        urls = values.get('urls')
        spider_name = values.get('spider')
        if not urls and spider_name == SpiderNames.CHOOSE_POEMS.value:
            raise ValueError('Необходим список стихов')
        if urls and spider_name != SpiderNames.CHOOSE_POEMS.value:
            raise ValueError('Паередан лишний параметр - `urls`')
        return values


    def dict(self) -> dict[str, str]:
        return {
            'spider': self.spider.value,
            'author': self.author,
        } | ({'urls': self.urls} if self.urls else {})


class RespParsingArgsSchema(BaseModel):
    """Схема ответа после парсинга.
    """
    uri: Path = Field(
        title = 'Месторасположение файла',
        description='',
        example = f'{RESULT_DIR}/{POEMS_STORE}' % (
            example_date, 'oleg', SpiderNames.ALL_POEMS.value
        )
    )
    
    class Config:
        title = 'Схема ответа после парсинга'
