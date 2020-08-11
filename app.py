import logging
import datetime
import os

from flask          import Flask
from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_cors     import CORS

from model          import Models
from service        import *
from view           import *


class Services:
    pass


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    
    if test_config is None:
        app.config["DB_URL"] = os.environ["DB_URL"]
        app.config["JWT_SECRET_KEY_A"] = os.environ["JWT_SECRET_KEY_A"]
        app.config["JWT_SECRET_KEY_B"] = os.environ["JWT_SECRET_KEY_B"]
    else:
        app.config.update(test_config)

    database = create_engine(app.config["DB_URL"], encoding="utf-8", max_overflow=0)
    app.database = database

    session_factory = sessionmaker(database)
    app.Session = scoped_session(session_factory)


    ## Persistence Layer
    models = Models(database)

    ## Business Layer
    services = Services
    services.auth_service = AuthService(models, app.config)
    services.sample_service = SampleService(models, app.config)

    ## 엔드포인트 생성
    create_endpoints(app, services)
    
    return app