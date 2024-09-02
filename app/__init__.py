# app/__init__.py

# third-party imports
from flask import Flask
from flask_sse import sse
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config

# db variable initialization
#db = SQLAlchemy()

config_name = 'development'


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    #db.init_app(app)
    app.register_blueprint(sse, url_prefix='/api/sse_stream')

    return app