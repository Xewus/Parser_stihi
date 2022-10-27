"""Эндпоинты для управления пользователями.
"""
from fastapi import APIRouter, Form

router = APIRouter()

@router.get('/create_user')
async def create_user_view():
    """Создать нового пользователя.
    """
    return {"message": "create user"}

@router.post('/login')
async def login_view(username: str = Form(), password: str = Form()):
    """Страница входа.

    ### Args:
        username (str): Юзернейм пользователя.
        password (str): Пароль пользователя.

    ### Returns:
        _type_ : _description_
    """
    return {"message": f"Login, {username}, {password}"}

@router.get('/logout')
async def logout_view():
    """Выход пользователя.

    Returns:
        _type_: _description_
    """
    return {"message": 'logout'}
