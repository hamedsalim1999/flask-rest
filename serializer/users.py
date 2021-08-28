from models.users import UserModel
from ma import ma
class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        load_only=('password',)
        dump_only=('id','activate',)
        load_instance = True
        include_relationships = True
        model = UserModel
