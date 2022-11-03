"""Эндпоинты для управления пользователями.
"""
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from users.api.schemas import Token, UserResponseSchema, UserUpdateSchema, UserCreateSchema, UserUpdateSchema, UserNotFound
from users.api.secrets import create_access_token, get_current_user, only_admin
from users.db.models import User

router = APIRouter(tags=['Users'])


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


@router.get('/me')
async def users_me_view(current_user: User = Depends(get_current_user)):
    return current_user


@router.get('/get_user/{username}', response_model=UserResponseSchema)
async def get_user_view(username: str):
    return await User.get(username=username)


@router.get('/all_users', response_model=list[UserResponseSchema])
async def all_users_view():
    return await User.all()


@router.post(
    path='/create_user',
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED
)#, dependencies=[Depends(only_admin)])
async def create_user_view(
    new_user: UserCreateSchema = Body()
):
    # new_user = {'hash': hash} | new_user.dict(exclude={'paassword'})
    user = await User.create(**new_user.dict())
    await user.save()
    return user


@router.patch(
    path='/update_user/{username}',
    response_model=UserResponseSchema
)
async def update_user_view(
    username: str,
    update_data: UserUpdateSchema
):
    user: User = await User.get(username=username)
    user.update_from_dict(update_data.dict(exclude_none=True))
    await user.save()
    return user

@router.patch(
    path='/activate/{username}',
    response_model=UserResponseSchema
)
async def activate_user_view(username: str):
    return await update_user_view(
        username=username,
        update_data=UserUpdateSchema(active=True)
    )


@router.patch(
    path='/deactivate/{username}',
    response_model=UserResponseSchema
)
async def deactivate_user_view(username: str):
    return await update_user_view(
        username=username,
        update_data=UserUpdateSchema(active=False)
    )
