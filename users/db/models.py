from tortoise.models import Model
from tortoise import fields
from passlib.context import CryptContext


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
