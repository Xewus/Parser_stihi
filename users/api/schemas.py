"""Схемы для эндпоинтов.
"""
from pydantic import BaseModel, Extra, Field, validator


class ErrorSchema(BaseModel):
    detail: str


class PasswordSchema(BaseModel):
    password: str

    @validator('password')
    def len_password(cls, password: str | None):
        if password is not None and len(password) < 8:
            raise ValueError('Пароль должен быть более 8 символов.')
        return password


class UserResponseSchema(BaseModel):
    username: str = Field(max_length=10)
    active: bool = False
    admin: bool = False

    class Config:
        orm_mode = True


class UserCreateSchema(UserResponseSchema, PasswordSchema):
    pass


class UserUpdateSchema(PasswordSchema):
    password: str | None = None
    active: bool | None = None
    admin: bool | None = None


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenData(BaseModel):
    username: str | None = None
