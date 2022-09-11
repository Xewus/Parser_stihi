"""Формы для view-функций.
"""
from flask_wtf import FlaskForm
from wtforms import (PasswordField, SelectField, SelectMultipleField,
                     StringField, SubmitField, URLField, widgets)
from wtforms.validators import DataRequired, NoneOf, Regexp

from admin import commands, users


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


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
            Regexp(
                regex='^[a-zA-ZА-Яа-яЁё]{3,16}$',
                message='Разрешены только буквы. Длина от 3 до 16.'
            )
        )
    )
    password = PasswordField(
        label='Пароль',
        validators=(
            DataRequired(message='Обязательное поле'),
        )
    )
    submit = SubmitField('Войти')


class ChoiceParseForm(FlaskForm):
    """Форма выбора варианта парсинга.

    #### Attrs:
    - author: URL-ссылка на выбранного автора.
    - choice: Выбор из доступных вариантов.
    - submit: Кнопка отправки данных.
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
    submit = SubmitField('Спарсить')


class ChoicePoemsForm(FlaskForm):
    """Форма для отметки необходимых для скачивания стихов.

    #### Atrrs:
    - poems: Отмечаемыt стихи.
    - submit: Кнопка отпраки данных.
    """
    choice = MultiCheckboxField(
        label='Выбрано',
        choices=[],
        validate_choice=False
    )
    submit = SubmitField('Подтвердить')


class CreateUserForm(LoginForm):
    """Форма для создания пользователя.

    #### Attrs:
    - username: Юзернейм нового пользователя.
    - user_password: Пароль нового пользователя.
    - password: Пароль суперюзера.
    - submit: Кнопка отпраки данных.
    """
    username = StringField(
        label='Имя пользователя',
        validators=(
            DataRequired(message='Обязательное поле'),
            Regexp(
                regex='^[a-zA-ZА-Яа-яЁё]{3,16}$',
                message='Разрешены только буквы. Длина от 3 до 16.'
            ),
            NoneOf(
                values=users.BaseUser.get_all_usernames(),
                message='Юзернейм уже занят!'
            )
        )
    )
    user_password = StringField(
        label='Пароль нового пользователя',
        validators=(
            DataRequired(message='Обязательное поле'),
            Regexp(
                regex='^[\w]{8,32}$',
                message='Разрешены только буквы и цифры. Длина от 8 до 32.'
            )
        )
    )
    submit = SubmitField('Создать')
