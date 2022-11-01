"""Организия доступов и разрешений.
"""
from datetime import datetime as dt
from datetime import timedelta
from parser.core.exceptions import TokenException, AuthException
from parser.db.user_models import User
from parser.settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from parser.web.schemas.users_schemas import TokenData

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(data: dict) -> str:
    """Создаёт зашифрованный `JWT-токен`.

    #### Args:
    - data (dict): Аргументы для шифрования в токене.

    #### Returns:
    - str: Зашифрованный `JWT-токен`.
    """
    to_encode = data.copy()
    expire = dt.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode['exp'] = expire
    return jwt.encode(
        claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM
    )


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Расшифровывает токен и возвращает пользователя.

    #### Args:
    - token (str): Токен из формы.

    #### Raises:
    - TokenException: Неверный токен.

    #### Returns:
    - User: Пользователь, владелец токена.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise TokenException
        token_data = TokenData(username=username)
    except JWTError:
        raise TokenException
    user: User = await User.get(username=token_data.username)
    if user is None:
        raise TokenException
    return user


def only_for_admin(user: User = Depends(get_current_user)) -> User:
    if not user.admin:
        raise AuthException
    return user
