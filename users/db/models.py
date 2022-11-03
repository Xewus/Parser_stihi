from tortoise.models import Model
from tortoise import fields
from passlib.context import CryptContext
from users.core.exceptions import BadRequestException


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

    def __str__(self) -> str:
        return self.username

    def __set_hash(self, password: str):
        self.hash = pass_context.hash(password)
    
    @classmethod
    async def create(cls, password: str | None,  **kwargs):
        if password is not None:
            hash = pass_context.hash(password)
            return await super().create(hash=hash, **kwargs)
        return await super().create(**kwargs)

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