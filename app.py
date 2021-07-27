from flask import Flask 
from flask_restful import Api
from flask_jwt_extended import JWTManager
from views.users import UserRegister,User,UserLogin
from views.items import Item,ItemList
from views.store import Store,StoreList

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] ='thisissecrettests'
jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):  # Remember identity is what we define when creating the access token
    if identity == 1:   # instead of hard-coding, we should read from a config file or database to get a list of admins instead
        return {'is_admin': True}
    return {'is_admin': False}

@app.before_first_request
def create_tables():
    db.create_all()

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
if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(debug=True)