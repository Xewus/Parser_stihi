"""Схемы для эндпоинтов юзеров.
"""
from pydantic import BaseModel, Field, validator, SecretStr, validator
from string import digits, ascii_lowercase, ascii_uppercase
from parser.core.exceptions import NoValidPasswordException

MIN_LENGT_PASSWORD = 8
DIGITS = set(digits)
LOWERS = set(ascii_lowercase)
UPPERS = set(ascii_uppercase)

class PasswordSchema(BaseModel):
    """Схема пароля.
    """
    password: SecretStr = Field(
        title='Пароль пользователя',
        description='Необходимы цифры, большие и маленькие буквы',
        example='j1E7jh8vg6'
    )

    class Comfig:
        title = 'Пароль пользователя',
    
    @validator('password')
    def validate_password(
        cls, password: SecretStr | None
    ) -> SecretStr | None:
        if password is None:
            return
        if len(password) < MIN_LENGT_PASSWORD:
            raise NoValidPasswordException(
                detail='Пароль должен быть длиннее %s символов' % MIN_LENGT_PASSWORD
            )
        pass_set = set(str(password.get_secret_value()))
        if not (
            (pass_set & DIGITS) and (pass_set & LOWERS) and (pass_set & UPPERS)
        ):
            raise NoValidPasswordException
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
