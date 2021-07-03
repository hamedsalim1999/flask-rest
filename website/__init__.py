from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_mail import Mail 
import os
from dotenv import load_dotenv 

db = SQLAlchemy()
mail = Mail()
ma = Marshmallow()

def create_app():
    load_dotenv()
    # config
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "2Hk8q_YjpSzxLyXjA" 
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir,'mydb.db')}"
    db= SQLAlchemy(app)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
    app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    jwt = JWTManager(app)
    ma = Marshmallow(app)
    from .views import views

    app.register_blueprint(views, url_prefix='/')


    from .models import User


    
    @app.cli.command('db_create')
    def db_create():
        db.create_all()
        print("data base is create")


    @app.cli.command('db_drop')
    def db_drop():
        db.drop_all()
        print("data base is drop")
    return app