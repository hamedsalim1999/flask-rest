from flask import Flask 
from flask_restful import Api
from flask_jwt import JWT 
from secrety import authenticate,identity
from views.users import UserRegister
from views.items import Item
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] ='thisissecret'
jwt = JWT(app,authenticate,identity)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'



api.add_resource(Item , '/item/<string:name>')
# api.add_resource(UserRegister,'/singup')
# api.add_resource(ItemList,'/')
if __name__ == '__main__':
    app.run(debug=True)