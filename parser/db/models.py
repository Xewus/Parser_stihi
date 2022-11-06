"""Модель пользователя и верификации пользователя.
"""
from __future__ import annotations

from parser.core.exceptions import BadRequestException

from passlib.context import CryptContext
from tortoise import fields
from tortoise.models import Model
from pydantic import SecretStr

pass_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class User(Model):
    user_id = fields.IntField(pk=True)
    username = fields.CharField(
        max_length=10,
        unique=True,
        description='Юзернейм пользователя'
    )
    hash = fields.CharField(
        max_length=64,
        description='Хэш для аутенфитикации'
    )
    admin = fields.BooleanField(default=False)
    active = fields.BooleanField(default=False)

    def __init__(self, password: str | SecretStr | None, **kwargs) -> None:
        super().__init__(**kwargs)
        if password is not None:
            self.set_hash(str(password))

    def __str__(self) -> str:
        return f'{self.username}, active: {self.active}, admin: {self.admin}'

    def set_hash(self, password: str) -> None:
        """Вычислить и установить атрибут `hash` объекта.

        #### Args:
        - password (str): Пароль.
        """
        self.hash = pass_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Проверить соответсвие пароля и хэша.

        #### Args:
        - password (str): Проверяемый пароль.

        #### Returns:
        - bool: Правильный ли пароль.
        """
        return pass_context.verify(password, self.hash)

    @staticmethod
    async def authenticate_user(
        username: str, password: str
    ) -> User:
        """Проверить наличие пользователя и соответствие пароля.

        #### Args:
        - username (str): Юзернейм пользователя.
        - password (str): Пароль введённый пользователем.

        #### Returns:
        - User: Проверенный пользователь.
        """
        user = await User.get_or_none(username=username)
        if not user:
            raise BadRequestException(detail='Неправильный юзернейм')
        if not user.verify_password(password):
            raise BadRequestException(detail='Неправильный пароль')
        if not user.active:
            raise BadRequestException(detail='Неактивный пользователь')

        return user


async def create_first_user() -> None:
    """Создаёт первого пользователя-админа, если БД пуста.
    """
    user = await User.first()
    if user:
        print(user)
        return None
    try:
        from parser.settings import FIRST_USER
        user = await User.create(**FIRST_USER)
        await user.save()
    except ImportError:
        print('В настройках нет данных для первого пользователя')
        return None
