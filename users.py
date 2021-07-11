import sqlite3
from sqlite3 import Cursor
from flask_restful import Resource,reqparse,output_json
class User:
    def __init__(self,_id,username,password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls,username):
        connect = sqlite3.connect('mydb.db')
        cursor = connect.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query,(username,))
        row = result.fetchone()
        if row:
            user=cls(*row)
        else:
            user= None
        connect.close()
        return user
    @classmethod
    def find_by_id(cls,_id):
        connect = sqlite3.connect('mydb.db')
        cursor = connect.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query,(_id,))
        row = result.fetchone()
        if row:
            user=cls(*row)
        else:
            user= None
        connect.close()
        return user


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
        connect = sqlite3.connect('mydb.db')
        cursor = connect.cursor()
        query = "INSERT INTO users VALUES (NULL,?,?)"
        cursor.execute(query,(data['username'],data['password']))
        connect.commit()
        connect.close()
        return {"msg":"user was create"}