"""Работа с пользователями.
"""
from flask import abort, request
from pony.orm import (Database, PrimaryKey, Required, db_session, select,
                      sql_debug)

from app_core.settings import (MAX_PASSWORD_LENGTH, MAX_USERNAME_LENGTH, PONY,
                               SU_PASSWORD)
from app_core.utils import AllowTries

sql_debug(True)
db = Database(**PONY)

pass_tries = AllowTries(tries=10)


class AnonimUser:
    user_id = 0
    username = 'anonim'
    active = True
    superuser = False
    is_logged = False

    def __repr__(self) -> str:
        return self.username

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'is_logged': self.is_logged
        }


class User(AnonimUser, db.Entity):
    user_id = PrimaryKey(int, auto=True)
    username = Required(str, MAX_USERNAME_LENGTH, unique=True)
    password = Required(str, MAX_PASSWORD_LENGTH)
    active = Required(bool, default=False)
    superuser = Required(bool, default=False)
    is_logged = True

    def __str__(self) -> str:
        return f'{self.user_id}: {self.username}'

    @classmethod
    @db_session
    def get_all_usernames(cls):
        return select(u.username for u in cls)[:]


db.generate_mapping(create_tables=1)


with db_session:
    if not len(User.select()[:1]):
        User(username='user', password='password', active=True)


def check_su_password(password: str) -> tuple[bool, str | None]:
    pass_tries(request.remote_addr, abort, 429)
    if password != SU_PASSWORD:
        return False, 'Неверный пароль суперпользователя'
    return True, None
