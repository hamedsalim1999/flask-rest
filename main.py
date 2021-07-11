from flask import Flask ,request
from flask_restful import Api , Resource , reqparse
from flask_jwt import JWT , jwt_required
from secrety import authenticate,identity
from users import UserRegister

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] ='thisissecret'
jwt = JWT(app,authenticate,identity)

datas=[]

class ItemList(Resource):
    def get(self):
        pass

class Student(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('price',
        type=float,
        required=True,
        help="this field not can be blank"
        )
    # @jwt_required()
    def get(self,name):
        item = next(filter(lambda x : x['name'] == name , datas),None) 
        if item:
            return item , 200 if item is not None else 404
        
        return {'items' : None} , 404
        # return{"Student":name}
    def post(self,name):
        item = next(filter(lambda x : x['name'] == name , datas),None) 
        data = self.parser.parse_args()
        if item:
            return "we have this item"
        else:
            datas.append({'name':name,'price':data['price']})
            return f"item was create"
    def delete(self,name):
        item = next(filter(lambda x : x['name'] == name , datas),None) 
        if item:
            datas.remove(item)
            return f"items was deleted"
        else:
            return "we dont have this item "
    def put(self,name):
        item = next(filter(lambda x : x['name'] == name , datas),None) 
        data = self.parser.parse_args()
        if item:
            item.update({'name':name,'price':data['price']})
            return f"items was update"
        else:
            datas.append({'name':name,'price':data['price']})   
            return "iteam was crate"   
api.add_resource(ItemList,'/items')
api.add_resource(Student , '/item/<string:name>')
api.add_resource(UserRegister,'/singup')
if __name__ == '__main__':
    app.run(debug=True)