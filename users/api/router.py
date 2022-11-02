"""Эндпоинты для управления пользователями.
"""
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from users.api.schemas import Token, UserSchema
from users.api.secrets import create_access_token, get_current_user, only_admin
from users.db.models import User

router = APIRouter(tags=['SimpleUsers'])

user_pydantic = pydantic_model_creator(User)


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


@router.post('/create_user')#, dependencies=[Depends(only_admin)])
async def create_user_view(
    new_user: UserSchema = Body()
):
    """Создать нового пользователя.
    """
    user = await User.create(**new_user.dict())
    return await user_pydantic.from_tortoise_orm(user)
