"""Модель пользователя.

На данный момент реализовано хранение в обычном файле.
При подключении БД, необходимо в модель, подключаемую к БД вписать в качестве
последнего родителя класс `BaseUser`, так сигнатуры методов прописанные в нём
используются в других местах приложения.
Так как эти методы вызываются через `await`, необходимо использовать
**асинхронные ORM**, например `SQLAlchemy 1.4+` / `Tortoise` либо
обернуть эти методы в асинхронные декораторы.
"""
import json
from parser.core.validators import valdate_file
from parser.settings import FIRST_USER, USERS_DB
from typing import Generic, TypeVar

from aiofile import AIOFile, LineReader, Writer
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field, SecretStr

U = TypeVar('U')


pass_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UpdateUser(BaseModel):
    """Модель данных для обновления.
    """
    password: SecretStr | None = None
    email: EmailStr | None = None
    active: bool | None = None
    admin: bool | None = None


class BaseUser(BaseModel, Generic[U]):
    """Интерфейс модели пользователя.
    """
    username: str = Field(
        title='Юзернейм пользователя',
        min_length=3,
        max_length=9
    )
    password: SecretStr = Field(
        title='Пароль пользователя',
        min_length=8,
        max_length=20
    )
    hash_password: str | None = None
    email: EmailStr
    active: bool = True
    admin: bool = False

    def verify_password(
        self, password: SecretStr, hashed_password: str
    ) -> bool:
        """Проверяет соответсвие пароля и хэша.

        #### Args:
        - password (SecretStr): Пароль пьзователя.
        - hashed_password (str): Хэш от пароля пользователя.

        Returns:
            bool: Соответствуют ли пароль и хэш.
        """
        return pass_context.verify(secret=password, hash=hashed_password)

    def hashing_password(self, password: SecretStr) -> str:
        """Хэширует пароль.

        #### Args:
        - password (SecretStr): Пароль пользователя.

        #### Returns:
            str: Хэш от пароля.
        """
        return pass_context.hash(str(password))

    async def authenticate_user(username: str, password: str) -> U | None:
        """Проверяет, правильность введённого пароля.

        #### Args:
        - username (str): Юзернейм пользователя.
        - password (str): Пароль.

        #### Raises:
        - NotImplementedError: Метод нужно реализовать в наследнике.

        #### Returns:
        - BaseUser | None: Объект пользователя если пароль верный.
        """
        raise NotImplementedError('Метод нужно реализовать в наследнике')

    async def get(username: str) -> U | None:
        """Получает пользователя из БД.

        #### Args:
        - username (str): Юзернейм пользователя.

        #### Raises:
        - NotImplementedError: Метод нужно реализовать в наследнике.

        #### Returns:
        - U | None: Объект пользователя если найден.
        """
        raise NotImplementedError('Метод нужно реализовать в наследнике')

    async def create(data: U) -> U | None:
        """Создать нового пользователя.

        #### Args:
        - data (BaseUser): Данные нового пользователя.

        #### Raises:
        - NotImplementedError: Метод нужно реализовать в наследнике.

        #### Returns:
        - User | None: Объект пользователя если создан.
        """
        raise NotImplementedError('Метод нужно реализовать в наследнике')
    
    async def update(user: U, data: UpdateUser) -> U | None:
        """Обновляет данные пользователя.

        #### Args:
        - user (U): Обновляемый пользователь.
        - data (UpdateUser): Новые данные.

        #### Raises:
        - NotImplementedError: Метод нужно реализовать в наследнике.

        #### Returns:
        - BaseUser | None: Обновлённые пользователь.
        """
        raise NotImplementedError('Метод нужно реализовать в наследнике')

    async def deactivate(user: U) -> U:
        """Деактивирует пользователя.

        #### Args:
        - user (U): Обновляемый пользователь.

        #### Raises:
        - NotImplementedError: Метод нужно реализовать в наследнике.

        #### Returns:
        - BaseUser | None: ОбДеактивированный пользователь.
        """
        raise NotImplementedError('Метод нужно реализовать в наследнике')
    

class User(BaseUser):
    hash_password = str
    password: SecretStr | None = None

    @staticmethod
    async def authenticate_user(
        username: str, password: str
    ) -> BaseUser | None:
        """Проверяет, правильность введённого пароля.

        #### Args:
        - username (str): Юзернейм пользователя.
        - password (str): Пароль.

        #### Returns:
        - User | None: Объект пользователя, если пароль верный.
        """
        user: User = await User.get(username)
        if not user:
            return False
        if not user.verify_password(password, user.hash_password):
            return False
        return user

    @staticmethod
    async def get(username: str) -> BaseUser | None:
        """Получить пользователя из БД.

        #### Args:
        - username (str): Юзернейм пользователя.

        #### Returns:
        - User | None: Объект пользователя если найден.
        """
        await valdate_file(USERS_DB)
        async with AIOFile(USERS_DB) as db:
            async for line in LineReader(db):
                user = User(**json.loads(line))
                if user.username == username:
                    return user

    async def create(self, new_user: BaseUser) -> BaseUser:
        """Создать нового пользователя.

        #### Args:
        - data (BaseUser): Данные нового пользователя.

        #### Returns:
        - User | None: Объект пользователя если создан.
        """
        await valdate_file(USERS_DB)
        user = await User.get(username=new_user.username)
        if user is not None:
            return None

        new_user.hash_password = new_user.hashing_password(new_user.password)
        user = User(**new_user.dict())
        user.password = None

        async with AIOFile(USERS_DB, 'a') as db:
            writer = Writer(db)
            await writer(user.json() + '\n')
            await db.fsync()
        return user


def create_first_user():
    """Создаёт первого пользователя, если БД пустая.
    """
    with open(USERS_DB, 'r+') as db:
        line = db.readline()
        if not line:
            user = BaseUser(**FIRST_USER)
            user.hash_password = user.hashing_password(user.password)
            user = User(**user.dict())
            user.password = None
            db.write(user.json() + '\n')
