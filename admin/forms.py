"""Формы для view-функций.
"""
from flask_wtf import FlaskForm
from wtforms import (PasswordField, SelectField, StringField, SubmitField,
                     URLField)
from wtforms.validators import DataRequired, Length

from admin import commands


class LoginForm(FlaskForm):
    """Форма для входа пользователя.

    #### Attrs:
    - username: Имя пользователя.
    - password: Пароль.
    - submit: Кнопка отпраки данных.
    """
    username = StringField(
        label='Имя пользователя',
        validators=(
            DataRequired(message='Обязательное поле'),
            Length(3, 16)
        )
    )
    password = PasswordField(
        label='Пароль',
        validators=(
            DataRequired(message='Обязательное поле'),
            Length(8, 16)
        )
    )
    submit = SubmitField('Войти')


class ChoiceParseForm(FlaskForm):
    """Форма выбора варианта парсинга.

    #### Attrs:
    - author: URL-ссылка на выбранного автора.
    - choice: Выбор из доступных вариантов.
    - submit: Кнопка отпраки данных.
    """
    author = URLField(
        label='URL-адрес автора',
        validators=(
            DataRequired(message='Обязательное поле'),
        )
    )
    choice = SelectField(
        label='Выбрать тип парсинга',
        choices=[
            (commands.ALL_POEMS, 'Все стихи'),
            (commands.LIST_POEMS, 'Список стихов'),
            (commands.CHOOSE_POEMS, 'Выбрать стихи')
        ]
    )
    submit = SubmitField('Выбрать')


class ChoicePoemForm(FlaskForm):
    """Форма для отметки необходимых для скачивания стихов.
    #### Atrrs:
    - poems: Отмечаемыt стихи.
    - submit: Кнопка отпраки данных.
    """
    poems = ...
    submit = SubmitField('Выбрать')
