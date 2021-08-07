from models.items import ItemModel
from models.store import StoreModel
from ma import ma
class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        include_relationships = True
  
    