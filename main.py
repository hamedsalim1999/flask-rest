from flask import Flask
from flask_restful import Api , Resource

app = Flask(__name__)
api = Api(app)

class Student(Resource):
    def get(self,name):
        return{"Student":name}

api.add_resource(Student , '/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)