"""Формы для view-функций.
"""
from wtforms.validators import ValidationError
from flask_wtf import FlaskForm
from wtforms import (PasswordField, SelectField, SelectMultipleField,
                     StringField, SubmitField, URLField, widgets)
from wtforms.validators import DataRequired, Regexp

from app import commands, model
from app_core.settings import (MAX_PASSWORD_LENGTH, MAX_USERNAME_LENGTH,
                               MIN_PASSWORD_LENGTH, MIN_USERNAME_LENGTH)


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
                regex=r'^[a-zA-ZА-Яа-яЁё]{%d,%d}$' % (
                    MIN_USERNAME_LENGTH, MAX_USERNAME_LENGTH
                ),
                message='Разрешены только буквы. Длина от '
                        f'{MIN_USERNAME_LENGTH} до {MAX_USERNAME_LENGTH}.'
            )
        )
    )
    password = PasswordField(
        label='Пароль пользователя',
        validators=(
            DataRequired(message='Обязательное поле'),
            Regexp(
                regex=r'[\w]{%d,%d}$' % (
                    MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH
                ),
                message='Разрешены только буквы и цифры. Длина от '
                f'{MIN_PASSWORD_LENGTH} до {MAX_PASSWORD_LENGTH}.'
            )
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
    - poems: Отмечаемые стихи.
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
                regex=r'^[a-zA-ZА-Яа-яЁё]{3,16}$',
                message='Разрешены только буквы. Длина от '
                        f'{MIN_USERNAME_LENGTH} до {MAX_USERNAME_LENGTH}.'
            ),
        )
    )
    su_password = StringField(
        label='Пароль суперпользователя',
        validators=(
            DataRequired(message='Обязательное поле'),
        )
    )
    submit = SubmitField('Создать')

    def validate_username(self, field):
        if field.data in model.User.get_all_usernames():
            raise ValidationError('Юзернейм уже занят')
