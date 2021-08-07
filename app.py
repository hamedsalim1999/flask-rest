from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from views.users import UserRegister,User,UserLogin
from views.items import Item,ItemList
from views.store import Store,StoreList
from db import db
from ma import ma
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] ='thisissecrettests'
jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)



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
    ma.init_app(app)
    db.init_app(app)
    app.run(debug=True)