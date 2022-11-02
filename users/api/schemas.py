"""Схемы для эндпоинтов.
"""
from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    password: str
    active: bool = False
    admin: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenData(BaseModel):
    username: str | None = None
