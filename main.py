from flask import Flask 
from flask_restful import Api
from flask_jwt import JWT 
from secrety import authenticate,identity
from users import UserRegister
from items import Item,ItemList


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] ='thisissecret'
jwt = JWT(app,authenticate,identity)



api.add_resource(Item , '/item/<string:name>')
api.add_resource(UserRegister,'/singup')
api.add_resource(ItemList,'/')
if __name__ == '__main__':
    app.run(debug=True)