"""Эндпоинты для управления пользователями.
"""
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from users.api.schemas import Token, UserSchema, UserUpdateSchema, UserNotFound
from users.api.secrets import create_access_token, get_current_user, only_admin
from users.db.models import User

router = APIRouter(tags=['SimpleUsers'])


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


@router.get('/get_user/{username}', response_model=UserSchema)
async def get_user_view(username: str):
    return await User.get_or_none(username=username)


@router.get('/all_users', response_model=list[UserSchema])
async def all_users_view():
    return await User.all()


@router.post(
    path='/create_user',
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED
)#, dependencies=[Depends(only_admin)])
async def create_user_view(
    new_user: UserSchema = Body()
):
    user = await User.create(**new_user.dict())
    await user.save()
    return user


@router.put(
    path='/update_user/{username}',
    responses={
        200: {'model': UserSchema},
        202: {'model': UserSchema},
        404: {'model': UserNotFound}
    }
)
async def update_user_view(
    username: str,
    update_data: UserUpdateSchema
):
    user: User = await User.get(username=username)
    changes = 0
    for key, value in update_data.dict().items():
        if value is None or getattr(user, key) == value:
            continue
        setattr(user, key, value)
        changes += 1
    if not changes:
        return JSONResponse(
            content=UserSchema.from_orm(user).dict(),
            status_code=status.HTTP_200_OK
        )

    await user.save()
    return JSONResponse(
        content=UserSchema.from_orm(user).dict(),
        status_code=status.HTTP_202_ACCEPTED
    )


@router.put(
    path='/activate/{username}',
    responses={
        200: {'model': UserSchema},
        202: {'model': UserSchema},
        404: {'model': UserNotFound}
    }
)
async def activate_user_view(username: str):
    return await update_user_view(
        username=username,
        update_data=UserUpdateSchema(active=True)
    )


@router.put(
    path='/deactivate/{username}',
    responses={
        200: {'model': UserSchema},
        202: {'model': UserSchema},
        404: {'model': UserNotFound}
    }
)
async def deactivate_user_view(username: str):
    return await update_user_view(
        username=username,
        update_data=UserUpdateSchema(active=False)
    )
