from flask_restful import Resource
from models.confirmation import ConfirmationModel
from models.users import UserModel
from datetime import datetime
from serializer.confirmation import ConfirmationSchema
class Confirmation(Resource):
    @classmethod
    def get(cls,confirmation_id : str):
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return{"msg":"not found"},404
        
        if confirmation.expired:
            return {"msg":"this message was expired"},400
        
        if confirmation.confirmed:
            return{"msg":"was confirmed"},400
        
        confirmation.confirmed = True
        confirmation.save_to_db()
        return {
            "msg":f"{confirmation.user.email}",
            },200

class ConfirmationByUser(Resource):
    @classmethod
    def get(cls,user_id:int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"msg":"user not found"}
        return{
            "current_time":datetime.now(),
            "confirmation":[
                ConfirmationSchema().dump(i)
                for i in user.confirmation.order_by(ConfirmationModel.expire_at)
            ],
        },200
        
    
    
    @classmethod
    def post(cls):
        pass