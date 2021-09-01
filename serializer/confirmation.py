from ma import ma
from models.confirmation import ConfirmationModel

class ConfirmationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        dump_only = ('user',)
        load_only = ('id','expire_at','confirmed')
        model = ConfirmationModel
        include_fk = True
  
    