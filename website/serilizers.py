from . import ma
class UserSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'name',
            'age',
            'email',
        )
user_schema = UserSchema()
users_schema = UserSchema(many=True)