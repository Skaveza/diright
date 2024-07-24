from flask import Flask
from flask_sqlalchemy import SQLALchemy
from flask_login import LoginManager

db = SQLALchemy
login_manager = LoginManager()

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'hufidfgfjfjf bhdjufjsdfjdbf'
  
  db.init_app(app)
  login_manager.init_app(app)
  login_manager.login_view = 'auth.login'
  
  from .views import views
  from .auth import auth
  
  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  
  from .models import User , PatientDocument
  create_database(app)
  
  return app

def create_database(app):
  with app.app_context():
    db.create_all()