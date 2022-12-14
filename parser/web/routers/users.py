"""Эндпоинты для управления пользователями.
"""
from parser.core.enums import Tag
from parser.db.models import User
from parser.web.schemas.users_schemas import (PasswordSchema, Token,
                                              UserSchema, UserCreateSchema,
                                              UserUpdateSchema)
from parser.web.secrets import (create_access_token, get_current_user,
                                only_admin)
from fastapi import APIRouter, Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(tags=[Tag.USERS])


@router.get(
    path='/me',
    summary='Вернуть пользователю его данные',
    response_model=UserSchema
)
async def users_me_view(current_user: User = Depends(get_current_user)):
    return current_user


@router.get(
    path='/get_user/{username}',
    summary='Получить данные указанного пользователя',
    description='Доступно только админам',
    response_model=UserSchema,
    dependencies=[Depends(only_admin)]
)
async def get_user_view(username: str):
    return await User.get(username=username)


@router.get(
    path='/all_users',
    summary='Получить данные всех пользователей',
    description='Доступно только админам',
    response_model=list[UserSchema],
    dependencies=[Depends(only_admin)]
)
async def all_users_view():
    return await User.all()


@router.post(
    path='/create_user',
    summary='Создать нового пользователя',
    description='Доступно только админам',
    response_model=UserSchema,
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
    path='/update_user/{username}',
    summary='Изменить данные указанного пользователя',
    description='Доступно только админам',
    dependencies=[Depends(only_admin)],
    response_model=UserSchema
)
async def update_user_view(
    update_data: UserUpdateSchema,
    username: str
):
    user = await User.get(username=username)    
    update_data = update_data.dict(exclude_none=True)
    password = update_data.pop('password', None)
    if password is not None:
        user.set_hash(password)
    user.update_from_dict(update_data)
    await user.save()
    return user


@router.patch(
    path='/update_user',
    summary='Изменить свои пользовательские данные',
    response_model=UserSchema,
    response_model_exclude={'admin'}
)
async def self_update_view(
    update_data: UserUpdateSchema,
    user: User = Depends(get_current_user)
):
    update_data.admin = None
    return await update_user_view(
        update_data=update_data,
        username=user.username
    )



@router.patch(
    path='/activate/{username}',
    summary='Активироапть указанного пользователя',
    description='Доступно только админам',
    response_model=UserSchema,
    dependencies=[Depends(only_admin)]
)
async def activate_user_view(username: str):
    return await update_user_view(
        update_data=UserUpdateSchema(active=True),
        username=username
    )


@router.patch(
    path='/deactivate/{username}',
    summary='Деактивировать указанного пользователя',
    description='Доступно только админам',
    response_model=UserSchema,
    dependencies=[Depends(only_admin)]
)
async def deactivate_user_view(username: str):
    return await update_user_view(
        update_data=UserUpdateSchema(active=False),
        username=username
    )


@router.post(
    path='/token',
    summary='Создаёт JWT-токен',
    response_model=Token
)
async def login_view(form_data: OAuth2PasswordRequestForm = Depends()):
    user: User = await User.authenticate_user(
        form_data.username, form_data.password
    )
    return Token(access_token=create_access_token(data={"sub": user.username}))


@router.patch(
    path='/change_password',
    summary='Изменить пароль пользователя',
    response_model=UserSchema
)
async def change_password_view(
    password: PasswordSchema,
    user: User = Depends(get_current_user)
):
    return await update_user_view(
        user=user,
        update_data=UserUpdateSchema(password=password.password)
    )
