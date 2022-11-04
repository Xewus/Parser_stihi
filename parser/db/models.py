from parser.core.exceptions import BadRequestException

from passlib.context import CryptContext
from tortoise import fields
from tortoise.models import Model

pass_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class User(Model):
    user_id = fields.IntField(pk=True)
    username = fields.CharField(
        max_length=10,
        unique=True,
        description='Юзернейм пользователя'
    )
    hash = fields.CharField(max_length=64)
    admin = fields.BooleanField(default=False)
    active = fields.BooleanField(default=False)

    def __init__(self, password: str | None, **kwargs) -> None:
        super().__init__(**kwargs)
        if password is not None:
            self.set_hash(password)

    def __str__(self) -> str:
        return self.username

    def set_hash(self, password: str):
        self.hash = pass_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Проверить соответсвие пароля и хэша.
        """
        return pass_context.verify(password, self.hash)

    @staticmethod
    async def authenticate_user(
        username: str, password: str
    ):
        """Проверяет соответствие пользователя и пароля.
        """
        user = await User.get_or_none(username=username)
        if not user:
            raise BadRequestException(detail='Неправильный юзернейм')
        if not user.verify_password(password):
            raise BadRequestException(detail='Неправильный пароль')
        if not user.active:
            raise BadRequestException(detail='Неактивный пользователь')

        return user


async def create_first_user():
    user = await User.first()
    if user:
        print(user)
        return
    from parser.settings import FIRST_USER
    user = await User.create(**FIRST_USER)
    await user.save()
