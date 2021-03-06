from models.users import UserModel
from flask_restful import Resource
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required
from serializer.users import UserSchema 
from flask import request
from lib.mailgun import MailGunException
from models.confirmation import ConfirmationModel
import traceback
class UserRegister(Resource):
    @classmethod
    def post(cls):
        user = UserSchema().load(request.get_json())
        if UserModel.find_by_username(user.username):
            return {"MSG":"We have this user naem"}
        if UserModel.find_by_email(user.email):
            return {"MSG":"We have this email"}
        try:
            user.save_to_db()
            ConfirmationModel(user.id).save_to_db()
            user.sendconfern_email()
            return{"msg":"user successfully crate"},201
        except MailGunException:
            user.delete_from_db()
            return {"msg":str(MailGunException)},500
        except:
            traceback.print_exc()
            return {"msg":"filed to create user "},500
            
        

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
        data = UserSchema().load(request.get_json(),partial=("email"))
        user = UserModel.find_by_username(data.username)
        
        if user and data.password:
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
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