"""Схемы валидации данных.
"""
from datetime import datetime as dt
from parser.core.enums import SpiderNames
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


class ChooseParsingSchema(BaseModel):
    """Схема запроса для старта парсинга.
    """
    spider: SpiderNames = Field(title='Имя паука')
    author: str = Field(
        title='Имя автора',
        description='Имя автора, как указано в `URL`'
    )

    class Config:
        title = 'Схема параметров необходимых для парсинга'
        schema_extra = {
            'examples': {
                'Все стихи': {
                    'summary': 'Полный URL на страницу автора',
                    'value': {
                        'spider': 'all-poems',
                        'author': 'https://stihi.ru/avtor/oleg/'
                    }
                },
                'Список стихов': {
                    'summary': 'Только имя из URL страницы автора',
                    'value': {
                        'spider': 'list-poems',
                        'author': 'oleg'
                    }
                },
                'С избранными стихами': {
                    'summary': 'Запрос с URL`ами стихов',
                    'value': {
                        'spider': 'choose-poems',
                        'author': 'oleg',

                    }
                }
            }
        }

    def dict(self) -> dict[str, str]:
        return {
            'spider': self.spider.value,
            'author': self.author,
        }


class ChoosePoemsSchema(BaseModel):
    poems: list[dict[str, HttpUrl]] = Field(
        title='Список ссылок на стихи',
        description='Названия стихов с ссылками.',
        example='''[
            {
                "title": "Английская колыбельная",
                "link": "https://stihi.ru//2012/01/19/2059"
            },
            {
                
                "title": "Ах, если б знал ты, как легко..."
                "link": "https://stihi.ru//2000/08/21-53"
            }
        ]'''
    )


class RespUriSchema(BaseModel):
    """Схема ответа после парсинга.
    """
    uri: Path = Field(
        title='Месторасположение файла',
        description='',
        example=f'{RESULT_DIR}/{POEMS_STORE}' % (
            example_date, 'oleg', SpiderNames.ALL_POEMS.value
        )
    )

    class Config:
        title = 'Схема ответа после парсинга'
