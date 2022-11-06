"""Схемы для эндпоинтов юзеров.
"""
from pydantic import BaseModel, Field, validator, validator
from string import digits, ascii_lowercase, ascii_uppercase
from parser.core.exceptions import BadRequestException

MIN_LENGT_PASSWORD = 8
MAX_LENGTH_USERNAME = 8
DIGITS = set(digits)
LOWERS = set(ascii_lowercase)
UPPERS = set(ascii_uppercase)


class Token(BaseModel):
    """Схема токена авторизации.
    """
    access_token: str
    token_type: str = 'bearer'


class UsernameSchema(BaseModel):
    """Схема имени пользователя.
    """
    username: str = Field(
        title='Юзернейм пользователя',
        description='Юзернейм должен быть только из букв и уникальным. '
        'Юзернейм всегда будет записываться в формате `Capitalize`.',
        max_length=MAX_LENGTH_USERNAME,
        example='John'
    )

    @validator('username')
    def validate_username(cls, username: str) -> str:
        if len(username) > MAX_LENGTH_USERNAME:
            raise BadRequestException(detail='Слишком длинный юзернейм')
        if not username.isalpha():
            raise BadRequestException(detail='Разрешены только буквы')
        return username.capitalize()


class PasswordSchema(BaseModel):
    """Схема пароля.
    """
    password: str = Field(
        title='Пароль пользователя',
        description='Необходимы цифры, большие и маленькие латинские буквы',
        example='111qqqQQQ'
    )

    class Config:
        title = 'Схема пароля пользователя'
    
    @validator('password')
    def validate_password(cls, password: str) -> str:
        if len(password) < MIN_LENGT_PASSWORD:
            raise BadRequestException(
                detail='Пароль должен быть длиннее %s символов' % (
                    MIN_LENGT_PASSWORD,
                )
            )
        pass_set = set(password)
        if not (
            (pass_set & DIGITS) and (pass_set & LOWERS) and (pass_set & UPPERS)
        ):
            raise BadRequestException(detail='Должны быть цифры, '
            'большие и маленькие буквы')
        return password


class UserSchema(UsernameSchema):
    """Схема пользовательских данных.
    """
    active: bool = Field(
        default=False,
        title='Метка - активирован ли пользователь',
        description='После создания пользователя админы могут активировать '
        'и деактивировать пользователя. Для авторизации пользователь должен '
        'быть активированным.',
        example='true' 
    )
    admin: bool = Field(
        default=False,
        title='Метка - является ли пользователь админом',
        description='Адимны могут создать, (де)активировать пользователя, '
        'изменять данные пользователя, кроме юзернейма.',
        example='false'
    )

    class Config:
        title = 'Схема пользовательских данных'
        orm_mode = True


class UserCreateSchema(PasswordSchema, UserSchema):

    class Config:
        title = 'Схема для создания пользователя'


class UserUpdateSchema(PasswordSchema):
    """Схема данных для изменения данных пользователя.
    """
    password: str | None = Field(
        default=None,
        title='Пароль пользователя',
        description='Необходимы цифры, большие и маленькие буквы',
        example='111qqqQQQ'
    )
    active: bool | None = Field(
        default=None,
        title='Метка - активирован ли пользователь',
        description='После деактивации, пользователь не сможет авторизоваться.',
        example='true' 
    )
    admin: bool | None = None

    class Config:
        title = 'Схема данных для изменения данных текущего пользователя'
