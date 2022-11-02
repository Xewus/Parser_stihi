from tortoise.models import Model
from tortoise import fields


class User(Model):
    user_id = fields.IntField(pk=True)
    username = fields.CharField(max_length=10)
    # hash = fields.CharField
    admin = fields.BooleanField(default=False)
    active = fields.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username
