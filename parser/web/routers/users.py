"""Эндпоинты для управления пользователями.
"""
from parser.core.enums import Tag
from parser.core.exceptions import BadRequestException
from parser.db.user_models import BaseUser, User
from parser.web.schemas.users_schemas import Token
from parser.web.secrets import create_access_token, get_current_user

from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=[Tag.USERS])


@router.post(
    path='/token',
    summary='Создаёт JWT-токен',
    response_model=Token
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user: User = await User.authenticate_user(
        form_data.username, form_data.password
    )
    if not user:
        raise BadRequestException(detail='Неправильный юзернейм или паролль.')
    if not user.active:
        raise BadRequestException(detail='Неактивный пользователь')

    return Token(access_token=create_access_token(data={"sub": user.username}))


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post('/create_user')
async def create_user_view(
    user_admin: User = Depends(get_current_user),
    new_user: BaseUser = Body()
):
    """Создать нового пользователя.
    """
    new_user: User = await user_admin.create_user(new_user)

    return new_user
