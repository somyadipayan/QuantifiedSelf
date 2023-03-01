from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .views import *
from .auth import *
from os import path, urandom
from flask_login import LoginManager

db = SQLAlchemy()
database = "quantifiedself.sqlite3"

def create_app():
    app = Flask(__name__)
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "SECRET_KEY"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database}'
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    db.init_app(app)

    from .models import User, Tracker, Log

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = u"Please Login to access this page"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(int(uid))
    
    return app

def create_database(app):
    if path.exists('website/' + database) == False:
        db.create_all(app=app)
        print('Database Created Successfully')
