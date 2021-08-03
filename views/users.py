from models.users import UserModel
from flask_restful import Resource,reqparse
from flask_jwt_extended import create_access_token,create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
        type=str,
        required=True,
        help="this field not can be blank"
        )
_user_parser.add_argument('password',
        type=str,
        required=True,
        help="this field not can be blank"
        )


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"MSG":"We have this user naem"}
        user = UserModel(**data)
        user.save_to_db()
        return {"msg":"user was create"}

class User(Resource):

    def get(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"msg": "user nOt found "},404
        return user.json()

    def delete(cls,user_id):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        if UserModel.find_by_id(user_id):
            UserModel.find_by_id(user_id).delete_from_db()
            return{"msg":"user was deleted"}
        else:
            return{"msg":"user not found"}
        
class UserLogin(Resource):


    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and data['password']:
            access_token = create_access_token(identity= user.id,fresh=True)
            refresh_token = create_refresh_token(user.id)
            return{
                "access_token":access_token,
                "refresh_token":refresh_token,
            },200
        return {"msg": "your username or password was not correct"},401

