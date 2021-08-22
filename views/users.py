from models.users import UserModel
from flask_restful import Resource
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required
from serializer.users import UserSchema 
from flask import request
import traceback
class UserRegister(Resource):
    @classmethod
    def post(cls):
        data = UserSchema().load(request.get_json())
        user = UserModel.find_by_username(data)
        if UserModel.find_by_username('username'):
            return {"MSG":"We have this user naem"}
        if UserModel.find_by_email('email'):
            return {"MSG":"We have this email"}
        try:
            user.save_to_db()
            user.sendconfern_email()
        except:
            traceback.print_exc()
            return {"msg":"filed to create user "},500
            
        return {"msg":"user was create"},201

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

    @classmethod
    def post(cls):
        data = UserSchema().load(request.get_json())
        user = UserModel.find_by_username(data,partial=("email",))
        if user and data.password:
            if user.activate:
                access_token = create_access_token(identity= user.id,fresh=True)
                refresh_token = create_refresh_token(user.id)
                return{
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                },200
            return {"msg":"user not activate yet please check your email"},403
        return {"msg": "your username or password was not correct"},401

class UserConfirm(Resource):
    @classmethod
    def get(cls,user_id:int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return{"msg": "user not found"},404
        
        user.activate = True
        user.save_to_db()
        return{"msg": "user activeate"},200