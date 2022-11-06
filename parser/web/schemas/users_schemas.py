"""Схемы для эндпоинтов юзеров.
"""
from pydantic import BaseModel, Field, validator, SecretStr, validator
from string import digits, ascii_lowercase, ascii_uppercase
from parser.core.exceptions import NoValidPasswordException

DIGITS = set(digits)
LOWERS = set(ascii_lowercase)
UPPERS = set(ascii_uppercase)

class PasswordSchema(BaseModel):
    """Схема пароля.
    """
    password: SecretStr = Field(
        title='Пароль пользователя',
        description='Необходимы цифры, большие и маленькие буквы',
        min_length=8,
        example='j1E7jh8vg6'
    )

    class Comfig:
        title = 'Пароль пользователя',
    
    @validator('password')
    def validate_password(cls, password:str) -> SecretStr:
        pass_set = set(password)
        if len(pass_set & DIGITS | pass_set & LOWERS | pass_set & UPPERS) < 3:
            raise NoValidPasswordException
        return password
            
    


    @validator('password')
    def len_password(cls, password: str | SecretStr| None):
        if password is not None and len(password) < 8:
            raise ValueError('Пароль должен быть более 8 символов.')
        return password


class UserResponseSchema(BaseModel):
    """Схема возвращаемых пользовательских данных.
    """
    username: str = Field(max_length=10)
    active: bool = False
    admin: bool = False

    class Config:
        orm_mode = True


class UserCreateSchema(UserResponseSchema, PasswordSchema):
    """Схема данных для создания пользователя.
    """
    pass


class UserUpdateSchema(PasswordSchema):
    """Схема данных для изтенения данных пользователя.
    """
    password: str | None = None
    active: bool | None = None
    admin: bool | None = None


class Token(BaseModel):
    """Схема токена авторизации.
    """
    access_token: str
    token_type: str = 'bearer'


class TokenData(BaseModel):
    """Схема имени пользователя.
    """
    username: str | None = None
