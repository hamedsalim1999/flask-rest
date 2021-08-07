from models.users import UserModel
from ma import ma
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        dump_only = ('id',)
        load_only=('password',)
        model = UserModel
