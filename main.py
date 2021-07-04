from flask import Flask
from flask_restful import Api , Resource

app = Flask(__name__)
api = Api(app)
datas=[]
class Student(Resource):

    def get(self,name):
        for i in datas:
            if i['name'] == name:
                return name , 200
            
        return {'items' : None} , 404
        # return{"Student":name}
    def post(self,name):
        data = {}
        datas.append({'name':name})
        return datas , 201

        
api.add_resource(Student , '/item/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)