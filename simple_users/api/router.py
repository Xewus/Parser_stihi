"""Эндпоинты для управления пользователями.
"""
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from simple_users.api.schemas import Token
from simple_users.api.secrets import create_access_token, get_current_user
from simple_users.core.exceptions import BadRequestException
from simple_users.db.models import BaseUser, User

router = APIRouter(tags=['SimpleUsers'])


@router.post(
    path='/token',
    summary='Создаёт JWT-токен',
    response_model=Token
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user: User = await User.authenticate_user(
        form_data.username, form_data.password
    )
    return Token(access_token=create_access_token(data={"sub": user.username}))


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post('/create_user')
async def create_user_view(
    new_user: BaseUser = Body()
):
    """Создать нового пользователя.
    """
    return await User.create(new_user)
