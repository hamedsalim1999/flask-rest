from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from serializer.items import ItemSchema
from models.items import ItemModel
from flask import request

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
    @classmethod
    def get(cls,name:str):
        item =  ItemModel.find_by_name(name)
        if item : 
            return item.json(),200
        return {"msg":"we dont have not found"} , 404
        

    def post (self,name:str):
        item = ItemModel.find_by_name(name)
        if item :
            return {"msg":f"{item.json()} already exists"},200
        data = ItemSchema.load(request.get_json())
        item = ItemModel(name,**data)
        try:
            item.save_to_db()
            return {"msg":f"item was crate {item.json()}"},201
        except:
            return {"msg":"An error occurred inserting the item"},404
       
    @jwt_required()
    @classmethod
    def delete (cls,name:str):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"msg":"item was deleted"},401
        return {"msg":"item wasn't exists"},404

    
    def put(self,name:str):
        item = ItemModel.find_by_name(name)
        data = ItemSchema.load(request.get_json())
        if item:
            item.price = data.price  ,202
        else:
            item = ItemModel(name,**data),201
        item.save_to_db()

        return item.json()

class ItemList(Resource):
    @classmethod
    def get(cls):
        return ItemModel.get_all_row(),200