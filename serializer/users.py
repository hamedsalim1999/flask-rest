from models.users import UserModel
from ma import ma
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        id = ma.auto_field(dump_only=True)
        activate = ma.auto_field(dump_only=True)
        load_only=('password',)
        load_instance = True
        include_relationships = True
        model = UserModel
