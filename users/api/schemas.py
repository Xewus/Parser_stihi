"""Схемы для эндпоинтов.
"""
from pydantic import BaseModel, Field

class UserResponseSchema(BaseModel):
    username: str
    active: bool
    admin: bool

    class Config:
        orm_mode = True


class UserCreateSchema(UserResponseSchema):
    password: str = Field(min_length=8)
    active: bool = False
    admin: bool = False


class UserUpdateSchema(BaseModel):
    password: str | None = Field(max_length=8)
    active: bool | None = None
    admin: bool | None = None

class UserNotFound(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenData(BaseModel):
    username: str | None = None
