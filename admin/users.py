"""Работа с пользователями.
"""
from collections import defaultdict
from pprint import pprint
from time import time
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import abort, request

from app_core.settings import BASE_DIR, USERS_STORE
from app_core.utils import AllowTries

load_dotenv(dotenv_path=BASE_DIR)

Path(USERS_STORE).touch()

DATA_SEPARATOR = ':'

USERS_SESSIONS = {}  # {'session_key': 'username'}

allow_tries = AllowTries()


class BaseUser:
    username = None
    password = None
    superuser = False

    def __str__(self) -> str:
        return self.username

    @staticmethod
    def check_user(username: str, password: str) -> bool:
        """Проверяет наличие пользователя с указанными юхернеймом и паролем.

        #### Args:
            username (str): Юзернейм.
            password (str): Пароль.

        #### Returns:
            bool: Найден ли пользователь.
        """
        allow_tries(request.remote_addr, abort, 403)
        with open(USERS_STORE, 'r') as file_store:
            for line in file_store.readlines():
                f_username, f_password, *_ = line.split(DATA_SEPARATOR)
                if username == f_username:
                    return password == f_password
        return False

    @staticmethod
    def get_all_usernames() -> set:
        """Получает набор всех юзернеймов.

        Returns:
            set: Набор всех юзернеймов.
        """
        with open(USERS_STORE) as file_store:
            return {
                line.split(DATA_SEPARATOR)[0] for line in file_store.readlines()
            }

    @staticmethod
    def check_username(username: str) -> bool:
        """Проверяет, занят ли юзернейм.

        #### Args:
            username (str): Юзернейм.

        #### Returns:
            bool: Занят или нет.
        """
        return username in BaseUser.get_all_usernames()

    @staticmethod
    def get_user_by_session(
        session: str, session_store: dict | None = None
    ) -> str | None:
        """Получает пользователя по сессии.

        #### Args:
            session (str): Ключ сессии.
            store (dict): Словарь, хранящий сессии.

        #### Returns
            str | None: Юхернейм, если найден.
        """
        store = session_store or USERS_SESSIONS
        return store.get(session)


class User(BaseUser):
    def __init__(self, username: str) -> None:
        self.username = username


class SuperUser(BaseUser):
    password = os.environ.get('PASSWORD')
    superuser = True

    @classmethod
    def check_su_password(cls, password: str) -> tuple[bool, str | None]:
        allow_tries(request.remote_addr)
        if password != cls.password:
            return False, 'Неверный пароль суперпользователя'
        return True, None        


    @classmethod
    def create_user(
        cls, username: str, user_password: str
    ) -> tuple[bool, str | None]:
        """Создаёт нового пользователя.

        Args:
            su_password (str): Пароль суперпользователя.
            username (str): Юзернейм нового пользователя.
            user_password (str): Пароль нового пользователя.

        Returns:
            tuple[bool, str | None]:
              Создан ли новый пользователь и текст ошибки.
        """
        with open(USERS_STORE, 'r+', encoding='utf-8') as store:
            for user in store.readlines():
                if user.split(':')[0] == username:
                    return False, 'Юзернейм уже занят'
            store.write(f'{str(username)}:{str(user_password)}:\n')
        return True, None
