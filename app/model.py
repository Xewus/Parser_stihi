"""Работа с пользователями.
"""
from ast import match_case
from flask import abort, request
from pony.orm import (Database, PrimaryKey, Required, db_session, select,
                      sql_debug)
from werkzeug.security import generate_password_hash, check_password_hash

from app_core.settings import (MAX_USERNAME_LENGTH,
                               SU_PASSWORD, Config)
from app_core.utils import AllowTries

# sql_debug(Config.DEBUG)

db = Database(**Config.PONY)


pass_tries = AllowTries(tries=10)


class AnonimUser:
    user_id = 0
    username = 'anonim'
    active = True
    superuser = False
    is_authenticated = False

    def __repr__(self) -> str:
        return self.username

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'is_authenticated': self.is_authenticated
        }


class User(AnonimUser, db.Entity):
    user_id = PrimaryKey(int, auto=True)
    username = Required(str, MAX_USERNAME_LENGTH, unique=True)
    password = Required(str, 128)
    is_active = Required(bool, default=False)
    is_authenticated = Required(bool, default=False)
    is_admin = Required(bool, default=False)

    def __init__(self, *args, **kwargs) -> None:
        kwargs['password'] = generate_password_hash(kwargs['password'])
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.user_id}: {self.username}'
    
    @db_session
    def check_password(self, password: str) -> bool:
        self.is_authenticated = check_password_hash(self.password, password)
        return self.is_authenticated

    @staticmethod
    @db_session
    def login(username: str, password: str):
        user = User.get(username=username)
        if user and user.check_password(password):
            user.is_authenticated = True
            return user
        return None

    @db_session
    def logout(self):
        user = User.get(user_id=self.user_id)
        user.is_authenticated = False

    @db_session
    def create_user(self, username: str, password: str) -> str:
        if  User.get(username=username) is None:
            User(username=username, password=password, is_active=True)
            return f'{username} создан'
        return '{username} не создан'

    @staticmethod
    @db_session
    def get_by_id(user_id: int | str):
        if isinstance(user_id, str) and user_id.isnumeric():
            return User.get(user_id=int(user_id))
        if isinstance(user_id, int):
            return User.get(user_id=user_id)
        return None



    @staticmethod
    @db_session
    def get_all_usernames():
        return select(u.username for u in User)[:]
    


db.generate_mapping(create_tables=1)


def check_su_password(password: str) -> tuple[bool, str | None]:
    """Проверяет пароль суперпользователя.

    Args:
        password (str): Проверяемый пароль.

    Returns:
        tuple[bool, str | None]: Правильный ли пароль.
    """
    pass_tries(request.remote_addr, abort, 429)
    if password != SU_PASSWORD:
        return False, 'Неверный пароль суперпользователя'
    return True, None
