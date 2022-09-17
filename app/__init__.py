from pprint import pprint
from flask import Flask
from pony.orm import db_session
from werkzeug.middleware.proxy_fix import ProxyFix

from app_core.settings import FIRST_PASSWORD, FIRST_USERNAME, Config

app = Flask(__name__)
app.config.from_object(Config)
app.wsgi_app = ProxyFix(app.wsgi_app)

pprint(dict(app.config))

from . import model, views  # noqa


with db_session:
    """Создаёт первого пользователя, если БД пустая.
    """
    if not len(model.User.select()[:1]):
        model.User(
            username=FIRST_USERNAME,
            password=FIRST_PASSWORD,
            is_active=True,
            is_authenticated = True,
            is_admin = True
        )
