from flask import Flask
from pony.orm import db_session

from app_core.settings import FIRST_PASSWORD, FIRST_USERNAME, Config

app = Flask(__name__)
app.config.from_object(Config)

from . import model, views  # noqa

with db_session:
    """Создаёт первого пользователя, если БД пустая.
    """
    if not len(model.User.select()[:1]):
        model.User(
            username=FIRST_USERNAME, password=FIRST_PASSWORD, active=True
        )
