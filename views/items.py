from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required,create_access_token,get_jwt

from models.items import ItemModel
class Item(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('price',
        type=float,
        required=True,
        help="this field not can be blank"
        )
        self.parser.add_argument('store_id',
        type=int,
        required=True,
        help="every item need store id "
        )
    
    @jwt_required()
    def get(self,name):
        item =  ItemModel.find_by_name(name)
        if item : 
            return item.json()
        return {"msg":"we dont have not found"} , 404
        

    def post (self,name):
        item = ItemModel.find_by_name(name)
        if item :
            return {"msg":f"{item.json()} already exists"}
        data = self.parser.parse_args()
        item = ItemModel(name,**data)
        try:
            item.save_to_db()
            return {"msg":f"item was crate {item.json()}"}
        except:
            return {"msg":"An error occurred inserting the item"}
       
    @jwt_required()
    def delete (self,name):
        claims = get_jwt()
        item = ItemModel.find_by_name(name)
        if not claims['is_admin']:
            return{"msg": "your don't have permission "},401
        if item:
            item.delete_from_db()
            return {"msg":"item was deleted"}
        return {"msg":"item wasn't exists"}

    
    def put(self,name):
        item = ItemModel.find_by_name(name)
        data = self.parser.parse_args()
        if item:
            item.price = data['price']  
        else:
            item = ItemModel(name,**data)
        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        return ItemModel.get_all_row()