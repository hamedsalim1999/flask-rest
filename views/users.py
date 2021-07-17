import sqlite3
from models.users import UserModel
from flask_restful import Resource,reqparse


class UserRegister(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username',
        type=str,
        required=True,
        help="this field not can be blank"
        )
        self.parser.add_argument('password',
        type=str,
        required=True,
        help="this field not can be blank"
        )
    def post(self):
        data = self.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"MSG":"We have this user naem"}
        else:
            connect = sqlite3.connect('mydb.db')
            cursor = connect.cursor()
            query = "INSERT INTO users VALUES (NULL,?,?)"
            cursor.execute(query,(data['username'],data['password']))
            connect.commit()
            connect.close()
            return {"msg":"user was create"}