"""Работа с пользователями.
"""
import os
import uuid
from datetime import datetime, timedelta

from dotenv import load_dotenv

from app_core.settings import BASE_DIR, LIVE_TOKEN, USERS_STORE

load_dotenv(dotenv_path=BASE_DIR)


class BaseUser:
    username = None
    password = None
    superuser = False
    store = USERS_STORE

    def __str__(self) -> str:
        return self.username

    def _set_token(self) -> None:
        self.token = str(uuid.uuid1())
        self.time_token = datetime.now() + timedelta(seconds=LIVE_TOKEN)

    @staticmethod
    def check_user(username: str, password: str) -> bool:
        try:
            file = open(BaseUser.store, 'r')
            for line in file.readlines():
                f_username, f_password = line.split()
                if username == f_username and password == f_password:
                    return True
        except FileNotFoundError:
            return False
        else:
            file.close()
        return False

    @staticmethod
    def check_username(username: str) -> bool:
        try:
            file = open(BaseUser.store, 'r')
            for line in file.readlines():
                f_username, _ = line.split()
                if username == f_username:
                    return True
        except FileNotFoundError:
            return False
        else:
            file.close()
        return False

    def check_time_token(self) -> bool:
        if not self.check_username(self.username):
            return False
        return self.time_token and self.time_token > datetime.now()

    @staticmethod
    def get_request_user_by_session(store: dict, session: str):
        """Проверяет наличие пользователя по сессии.

        Args:
            store (dict): _description_
            session (str): _description_

        Returns:
            bool: _description_
        """
        return store.get(session)


class User(BaseUser):
    def __init__(self, username: str) -> None:
        self.username = username
        self._set_token()


class SuperUser(BaseUser):
    password = os.environ.get('PASSWORD')
    superuser = True

    def create_user(
        self, su_password: str, username: str, user_password: str
    ) -> bool:
        if su_password != self.password:
            return False
        with open(self.store, 'a+', 'utf-8') as file:
            for user in file.readlines:
                if user[0] == username:
                    return False
            file.write(f'{str(username)} {str(user_password)}')
        return True
