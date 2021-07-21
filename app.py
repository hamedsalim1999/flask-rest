from flask import Flask 
from flask_restful import Api
from flask_jwt import JWT 
from secrety import authenticate,identity
from views.users import UserRegister,User
from views.items import Item,ItemList
from views.store import Store,StoreList
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] ='thisissecrettests'
jwt = JWT(app,authenticate,identity)

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
if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(debug=True)