from flask import Flask

from app_core.settings import Config

app = Flask(__name__)
app.config.from_object(Config)

from . import views
