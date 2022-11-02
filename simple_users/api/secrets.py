from datetime import datetime as dt
from datetime import timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from simple_users.api.schemas import TokenData
from simple_users.core.exceptions import TokenException
from simple_users.db.models import User
from simple_users.settings import (ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM,
                                   SECRET_KEY)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/token')


def create_access_token(data: dict) -> str:
    """Создаёт зашифрованный JWT-токен.
    """
    to_encode = data.copy()
    expire = dt.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode['exp'] = expire
    return jwt.encode(
        claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM
    )


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Расшифровывает токен и возвращает пользователя.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise TokenException
        token_data = TokenData(username=username)
    except JWTError:
        raise TokenException
    user: User = await User.get(attr='username', value=token_data.username)
    if user is None:
        raise TokenException
    return user
