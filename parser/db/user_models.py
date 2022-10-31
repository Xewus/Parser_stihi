import json
from parser.core.exceptions import BadRequestException
from parser.core.validators import valdate_file
from parser.settings import FIRST_USER, USERS_DB
from typing import Generic, TypeVar

from aiofile import AIOFile, LineReader, Writer
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field, SecretStr

U = TypeVar('U')


pass_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class BaseUser(BaseModel, Generic[U]):
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

    def verify_password(self, password: str, hashed_password: str) -> bool:
        raise

    def hashing_password(self, password: str) -> str:
        """Хэширует пароль.

        Args:
            password (str): _description_

        Returns:
            str: _description_
        """
        return pass_context.hash(str(password))

    def get_user(username: str) -> U | None:
        raise

    def authenticate_user(username: str, password: str) -> U | None:
        raise

    def create_user(data: U):
        raise


class User(BaseUser):
    hash_password = str
    password: SecretStr | None = None

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Проверяет соответсвие пароля и хэша.

        Args:
            password (str): _description_
            hashed_password (str): _description_

        Returns:
            bool: _description_
        """
        return pass_context.verify(secret=password, hash=hashed_password)

    @staticmethod
    async def get_user(username: str) -> BaseUser | None:
        """Находит польхователя в БД по уникальному юзернейму.

        Args:
            username (str): _description_

        Returns:
            U | None: _description_
        """
        await valdate_file(USERS_DB)
        async with AIOFile(USERS_DB) as db:
            async for line in LineReader(db):
                user = User(**json.loads(line))
                if user.username == username:
                    return user

    @staticmethod
    async def authenticate_user(
        username: str, password: str
    ) -> BaseUser | None:
        """Проверяет соответствие пользователя и пароля.

        Args:
            username (str): _description_
            password (str): _description_

        Returns:
            U | None: _description_
        """
        user: User = await User.get_user(username)
        if not user:
            return False
        if not user.verify_password(password, user.hash_password):
            return False
        return user

    async def create_user(self, new_user: BaseUser) -> BaseUser:
        if not self.admin:
            raise BadRequestException('Недостаточно прав для создания')
        await valdate_file(USERS_DB)
        user = await User.get_user(username=new_user.username)
        if user is not None:
            raise BadRequestException('Юзернейм занят')
        new_user.hash_password = new_user.hashing_password(new_user.password)
        user = User(**new_user.dict())
        user.password = None
        async with AIOFile(USERS_DB, 'a') as db:
            writer = Writer(db)
            await writer(user.json() + '\n')
            await db.fsync()
        return user


def create_first_user():
    with open(USERS_DB, 'r+') as db:
        line = db.readline()
        if not line:
            user = BaseUser(**FIRST_USER)
            user.hash_password = user.hashing_password(user.password)
            user = User(**user.dict())
            user.password = None
            db.write(user.json() + '\n')
