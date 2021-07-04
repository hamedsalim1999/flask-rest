from flask import Flask ,request
from flask_restful import Api , Resource

app = Flask(__name__)
api = Api(app)
datas=[]

class ItemList(Resource):
    def get(self):
        pass

class Student(Resource):

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

api.add_resource(ItemList,'/items')
api.add_resource(Student , '/item/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)