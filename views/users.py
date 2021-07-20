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
        user = UserModel(data['username'],data['password'])
        user.save_to_db()
        return {"msg":"user was create"}