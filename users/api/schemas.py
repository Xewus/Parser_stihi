"""Схемы для эндпоинтов.
"""
from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    active: bool = False
    admin: bool = False

    class Config:
        orm_mode = True

class UserUpdateSchema(BaseModel):
    active: bool | None = None
    admin: bool | None = None

class UserNotFound(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenData(BaseModel):
    username: str | None = None
