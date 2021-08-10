from models.store import StoreModel
from models.items import ItemModel
from serializer.items import ItemSchema
from ma import ma
class StoreSchema(ma.SQLAlchemyAutoSchema):
    item = ma.Nested(ItemSchema,many=True)
    class Meta:
        dump_only = ('id',)
        load_only=('store',)
        model=StoreModel
        include_relationships = True

    