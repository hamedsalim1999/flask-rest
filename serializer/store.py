from models.store import StoreModel
from ma import ma
class StoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        dump_only = ('id',)
        load_only=('store',)
        model=StoreModel
        include_relationships = True

    