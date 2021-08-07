from models.users import UserModel
from flask_restful import Resource
from flask_jwt_extended import create_access_token,create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt
from serializer.users import UserSchema 
from flask import request
from marshmallow import ValidationError
class UserRegister(Resource):
    @classmethod
    def post(cls):
        try:
            data = UserSchema().load(request.get_json())
        except ValidationError as error :
            return error.messages,400
        if UserModel.find_by_username.username:
            return {"MSG":"We have this user naem"}
        user = UserModel(**data)
        user.save_to_db()
        return {"msg":"user was create"}

class User(Resource):

    def get(cls,user_id:int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"msg": "user nOt found "},404
        return UserSchema().dump(user)

    def delete(cls,user_id:int):
        if UserModel.find_by_id(user_id):
            UserModel.find_by_id(user_id).delete_from_db()
            return{"msg":"user was deleted"}
        else:
            return{"msg":"user not found"}
        
class UserLogin(Resource):


    def post(cls):
        try:
            data = UserSchema().load(request.get_json())
        except ValidationError as error :
            return error.messages,400
        user = UserModel.find_by_username(data.username)
        if user and data.password:
            access_token = create_access_token(identity= user.id,fresh=True)
            refresh_token = create_refresh_token(user.id)
            return{
                "access_token":access_token,
                "refresh_token":refresh_token,
            },200
        return {"msg": "your username or password was not correct"},401

