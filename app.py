from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from views.users import UserRegister,User,UserLogin,UserConfirm
from views.items import Item,ItemList
from views.store import Store,StoreList
from db import db
from ma import ma
from mail import mail
from marshmallow import ValidationError
from views.confirmation import Confirmation,ConfirmationByUser
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] ='thisissecrettests'
jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handel_error_marshmallow_validator(err):
    return jsonify(err.message),400


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'



api.add_resource(Item , '/item/<string:name>')
api.add_resource(UserRegister,'/singup')
api.add_resource(ItemList,'/')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(UserLogin,'/login')
api.add_resource(UserConfirm,'/userconfern/<int:user_id>')
api.add_resource(Confirmation,'/confirmation/<string:confirmation_id>')
api.add_resource(ConfirmationByUser,'/userconfirmation/<int:user_id>')

if __name__ == '__main__':
    ma.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    app.run(debug=True,host="0.0.0.0")