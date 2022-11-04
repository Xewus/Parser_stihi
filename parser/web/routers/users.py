"""Эндпоинты для управления пользователями.
"""
from parser.core.enums import Tag
<<<<<<< HEAD
from parser.core.exceptions import BadRequestException
from parser.db.user_models import BaseUser, User
from parser.web.schemas.users_schemas import Token
from parser.web.secrets import create_access_token, get_current_user, only_for_admin

from fastapi import APIRouter, Body, Depends
=======
from parser.db.models import User
from parser.web.schemas.users_schemas import (PasswordSchema, Token,
                                              UserCreateSchema,
                                              UserResponseSchema,
                                              UserUpdateSchema)
from parser.web.secrets import (create_access_token, get_current_user,
                                only_admin)

from fastapi import APIRouter, Body, Depends, status
>>>>>>> users
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=[Tag.USERS])


@router.get(
    path='/me',
    response_model=UserResponseSchema
)
async def users_me_view(current_user: User = Depends(get_current_user)):
    return current_user


@router.get(
    path='/get_user/{username}',
    response_model=UserResponseSchema,
    dependencies=[Depends(only_admin)]
)
async def get_user_view(username: str):
    return await User.get(username=username)


@router.get(
    path='/all_users',
    response_model=list[UserResponseSchema],
    dependencies=[Depends(only_admin)]
)
async def all_users_view():
    return await User.all()


@router.post(
    path='/create_user',
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(only_admin)]
)
async def create_user_view(
    new_user: UserCreateSchema = Body()
):
    user = await User.create(**new_user.dict())
    await user.save()
    return user


@router.patch(
    path='/update_user',
    response_model=UserResponseSchema,
    dependencies=[Depends(only_admin)]
)
async def update_user_view(
    update_data: UserUpdateSchema,
    user: User = Depends(get_current_user),
):
    update_data = update_data.dict(exclude_none=True)
    password = update_data.pop('password')
    if password is not None:
        user.set_hash(password)
    user.update_from_dict(update_data)
    await user.save()
    return user


@router.patch(
    path='/activate/{username}',
    response_model=UserResponseSchema,
    dependencies=[Depends(only_admin)]
)
async def activate_user_view(username: str):
    return await update_user_view(
        user=await User.get(username=username),
        update_data=UserUpdateSchema(active=True)
    )


@router.patch(
    path='/deactivate/{username}',
    response_model=UserResponseSchema,
    dependencies=[Depends(only_admin)]
)
async def deactivate_user_view(username: str):
    return await update_user_view(
        user=await User.get(username=username),
        update_data=UserUpdateSchema(active=False)
    )


@router.post(
    path='/token',
    summary='Создаёт JWT-токен',
    response_model=Token
)
<<<<<<< HEAD
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user: User = await User.authenticate_user(
        form_data.username, form_data.password
    )
    if user is None:
        raise BadRequestException(detail='Неправильный юзернейм или паролль.')
    if not user.active:
        raise BadRequestException(detail='Неактивный пользователь')

    return Token(access_token=create_access_token(data={"sub": user.username}))


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post('/create_user')
async def create_user_view(
    user_admin: User = Depends(only_for_admin),
    new_user: BaseUser = Body()
):
    new_user: User = await user_admin.create(new_user)
    if new_user is None:
        raise BadRequestException('Юзернейм занят')

    return new_user
=======
async def login_view(form_data: OAuth2PasswordRequestForm = Depends()):
    user: User = await User.authenticate_user(
        form_data.username, form_data.password
    )
    return Token(access_token=create_access_token(data={"sub": user.username}))


@router.patch(
    path='/change_password',
    response_model=UserResponseSchema
)
async def change_password_view(
    password: PasswordSchema,
    user: User = Depends(get_current_user)
):
    return await update_user_view(
        user=user,
        update_data=UserUpdateSchema(password=password.password)
    )
>>>>>>> users
