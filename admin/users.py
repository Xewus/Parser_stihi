"""Работа с пользователями.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

from app_core.settings import BASE_DIR, USERS_STORE

load_dotenv(dotenv_path=BASE_DIR)

Path(USERS_STORE).touch()

DATA_SEPARATOR = ':'


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
        with open(USERS_STORE, 'r') as store:
            for line in store.readlines():
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
        with open(USERS_STORE) as store:
            return {
                line.split(DATA_SEPARATOR)[0] for line in store.readlines()
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
    def get_request_user_by_session(store: dict, session: str) -> str | None:
        """Получает пользователя по сессии.

        #### Args:
            store (dict): Словарь, хранящий сессии.
            session (str): Ключ сессии.

        #### Returns
            str | None: Юхернейм, если найден.
        """
        return store.get(session)


class User(BaseUser):
    def __init__(self, username: str) -> None:
        self.username = username


class SuperUser(BaseUser):
    password = os.environ.get('PASSWORD')
    superuser = True

    @classmethod
    def create_user(
        cls, su_password: str, username: str, user_password: str
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
        if su_password != cls.password:
            return False, 'Неверный пароль суперпользователя'

        with open(USERS_STORE, 'r+', encoding='utf-8') as store:
            for user in store.readlines():
                if user.split(':')[0] == username:
                    return False, 'Юзернейм уже занят'
            store.write(f'{str(username)}:{str(user_password)}:\n')
        return True, None
