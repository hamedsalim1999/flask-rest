import sqlite3
from models.users import UserModel
from flask_restful import Resource,reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,

)

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
        user = UserModel(**data)
        user.save_to_db()
        return {"msg":"user was create"}

class User(Resource):
    @classmethod
    def get(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"msg": "user nOt found "},404
        return user.json()
    @classmethod
    def delete(cls,user_id):
        if UserModel.find_by_id(user_id):
            UserModel.find_by_id(user_id).delete_from_db()
            return{"msg":"user was deleted"}
        else:
            return{"msg":"user not found"}
        
class UserLogin(Resource):
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
        user = UserModel.find_by_username(data['username'])
        if user and data['password']:
            access_token = create_access_token(identity= user.id,fresh=True)
            refresh_token = create_refresh_token(user.id)
            return{
                "access_token":access_token,
                "refresh_token":refresh_token,
            }
        return {"msg": "your username or password was not correct"}