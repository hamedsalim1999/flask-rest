from models.users import UserModel
from ma import ma
from marshmallow import pre_dump
class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        load_only=('password  ',)
        dump_only=('id','confirmation')
        load_instance = True
        include_relationships = True
        model = UserModel
    @pre_dump
    def _pre_dump(self,user:UserModel):
        user.confirmation = [user.most_recent_confirmation]
        return user