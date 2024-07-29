from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from os import path

db = SQLAlchemy()
login_manager = LoginManager()

def create_database(app):
    with app.app_context():
        db.create_all()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hufidfgfjfjf bhdjufjsdfjdbf'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, PatientDocument

    create_database(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
  