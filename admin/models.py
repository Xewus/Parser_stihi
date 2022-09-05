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

    def _set_token(self) -> None:
        self.token = str(uuid.uuid1())
        self.time_token = datetime.now() + timedelta(seconds=LIVE_TOKEN)

    @staticmethod
    def check_user(username: str, password: str) -> bool:
        try:
            with open(BaseUser.store, 'r') as file:
                for line in file.readlines():
                    f_username, f_password = line.split()
                    if username == f_username and password == f_password:
                        return True
        except FileNotFoundError:
            return False
        return False

    @staticmethod
    def check_username(username: str) -> bool:
        try:
            with open(BaseUser.store, 'r') as file:
                for line in file.readlines():
                    f_username, _ = line.split()
                    if username == f_username:
                        return True
        except FileNotFoundError:
            return False
        return False

    def check_time_token(self) -> bool:
        if not BaseUser.check_username(self.username):
            return False
        return self.time_token > datetime.now()


class User(BaseUser):
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self._set_token()


class SuperUser(BaseUser):
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    superuser = True

    def __create_user(self, username: str, password: str) -> User:
        with open(self.store, 'a+', 'utf-8') as file:
            file.write(f'{str(username)} {str(password)}')
