from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY '] = 'secret_key_bro_it_is_super_secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.secret_key = 'this_is_another_super_secrecet_secret_pro_max_secret_key_bro'
    # app.config['TESTING'] = False


    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from website.models import User, Posts

    app.app_context().push()
    create_database(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    login_manager.login_view = '/login'

    @login_manager.user_loader
    def user_loader(id):
        return User.query.filter(User.id == id).first()

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all()