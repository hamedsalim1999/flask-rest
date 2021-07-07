from flask import Flask ,request
from flask_restful import Api , Resource
from flask_jwt import JWT , jwt_required
from secrety import authenticate,identity


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] ='thisissecret'
jwt = JWT(app,authenticate,identity)

datas=[]

class ItemList(Resource):
    def get(self):
        pass

class Student(Resource):
    @jwt_required()
    def get(self,name):
        item = next(filter(lambda x : x['name'] == name , datas),None) 
        if item:
            return item , 200 if item is not None else 404
        
        return {'items' : None} , 404
        # return{"Student":name}
    def post(self,name):
        data = request.get_json()
        datas.append({'name':name,'price':data['price']})
        return datas , 201
    def delete(self,name):
        item = next(filter(lambda x : x['name'] == name , datas),None) 
        if item:
            datas.remove(item)
            return f"items was deleted"
        else:
            return "we dont have this item "
    def put(self,name):
        item = next(filter(lambda x : x['name'] == name , datas),None) 
        data = request.get_json()
        if item:
            item.update({'name':name,'price':data['price']})
            return f"items was update"
        else:
            datas.append({'name':name,'price':data['price']})   
            return "iteam was crate"   
api.add_resource(ItemList,'/items')
api.add_resource(Student , '/item/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)