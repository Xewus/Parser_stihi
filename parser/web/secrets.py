from datetime import datetime as dt
from datetime import timedelta
from parser.core.exceptions import AuthException, TokenException
from parser.db.models import User
from parser.settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from parser.web.schemas.users_schemas import UsernameSchema

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/token')


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
    """Расшифровывает токен и возвращает пользоват

    #### Args:
    - token (str): Токен из формы.

    #### Returns:
    - User: Пользователь, владелец токена.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(username)
        if username is None:
            raise TokenException
        token_data = UsernameSchema(username=username)
    except JWTError:
        raise TokenException
    user = await User.get_or_none(username=token_data.username)
    if user is None:
        raise TokenException
    return user


def only_admin(user: User = Depends(get_current_user)) -> User:
    if not user.admin:
        raise AuthException
    return user
