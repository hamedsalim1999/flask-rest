from flask import Flask ,request
from flask_restful import Api , Resource , reqparse
from flask_jwt import JWT , jwt_required
from secrety import authenticate,identity
from users import UserRegister
from items import Item
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] ='thisissecret'
jwt = JWT(app,authenticate,identity)



api.add_resource(Item , '/item/<string:name>')
api.add_resource(UserRegister,'/singup')

if __name__ == '__main__':
    app.run(debug=True)