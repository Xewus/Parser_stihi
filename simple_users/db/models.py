"""Модели хранения данных.
"""
from abc import ABC, abstractmethod, abstractstaticmethod
import json
from pprint import pprint
from typing import Any, Generic, TypeVar

from aiofile import AIOFile, LineReader, Writer
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field, SecretStr

from simple_users.core.exceptions import BadRequestException
from simple_users.settings import FIRST_USER, USERS_DB

U = TypeVar('U', bound='BaseUser')

pass_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class BaseUser(BaseModel, Generic[U]):
    username: str = Field(
        title='Юзернейм пользователя',
        min_length=3,
        max_length=9
    )
    password: str = Field(
        title='Пароль пользователя',
        min_length=8,
        max_length=20
    )
    hash: str | None
    active: bool = False
    admin: bool = False

    def verify_password(self, password: str) -> bool:
        """Проверить соответсвие пароля и хэша.
        """
        return pass_context.verify(password, self.hash)

    def hashing_password(self, password: str) -> str:
        """Получить хэш пароля.
        """
        return pass_context.hash(password)
 

class ABCUser(BaseUser, ABC):
    password: str | None = Field(
        default=None,
        title='Пароль пользователя',
        min_length=8,
        max_length=20
    )
    hash: str

    @abstractstaticmethod
    async def authenticate_user(username: str, password: str) -> U | None:
        """Аутефентицировать пользователя"""

    @abstractstaticmethod
    async def get(attr: str, value: Any) -> U | None:
        """Получить пользователя из БД по атрибуту.
        """

    @abstractstaticmethod
    async def create(data: U):
        """Созать пользователя.
        """


class User(ABCUser):

    @staticmethod
    async def authenticate_user(
        username: str, password: str
    ) -> BaseUser | None:
        """Проверяет соответствие пользователя и пароля.
        """
        user = await User.get(attr='username', value=username)
        if not user:
            raise BadRequestException(detail='Неправильный юзернейм')
        if not user.verify_password(password):
            raise BadRequestException(detail='Неправильный пароль')
        if not user.active:
            raise BadRequestException(detail='Неактивный пользователь')

        return user

    @staticmethod
    async def get(attr: str, value: Any) -> U | None:
        """Получить пользователя из БД по атрибуту.
        """
        async with AIOFile(USERS_DB) as db:
            async for line in LineReader(db):
                user = User(**json.loads(line))
                attr_value = getattr(user, attr, None)
                if attr_value and attr_value == value:
                    return user
    
    @staticmethod
    async def create(new_user: BaseUser) -> BaseUser:
        """Создать нового пользователя.
        #### Args:
        - data (BaseUser): Данные нового пользователя.
        #### Returns:
        - User | None: Объект пользователя если создан.
        """
        user = await User.get(attr='username', value=new_user.username)
        if user is not None:
            raise BadRequestException('Пользователь уже существует')

        new_user.hash = new_user.hashing_password(new_user.password)
        user = User(**new_user.dict())
        user.password = None
        user.active = True

        async with AIOFile(USERS_DB, 'a') as db:
            writer = Writer(db)
            await writer(user.json() + '\n')
            await db.fsync()
        return user


    #     if not self.admin:
    #         raise BadRequestException('Недостаточно прав для создания')
    #     user = await User.get_user(username=new_user.username)
    #     if user is not None:
    #         raise BadRequestException('Юзернейм занят')
    #     new_user.hash_password = new_user.hashing_password(new_user.password)
    #     user = User(**new_user.dict())
    #     print(user)
    #     user.password = None
    #     async with AIOFile(USERS_DB, 'a') as db:
    #         writer = Writer(db)
    #         await writer(user.json() + '\n')
    #         await db.fsync()
    #     return user


def create_first_user():
    with open(USERS_DB, 'r+') as db:
        line = db.readline()
        if not line:
            user = BaseUser(**FIRST_USER)
            user.hash = user.hashing_password(user.password)
            user = User(**user.dict())
            user.password = None
            db.write(user.json() + '\n')
