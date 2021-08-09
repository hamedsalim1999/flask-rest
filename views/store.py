from flask import request
from models.store import StoreModel
from flask_restful import Resource,reqparse
from serializer.store import StoreSchema

class Store(Resource):

    @classmethod
    def get(cls,name:str):
        store =  StoreModel.find_by_name(name)
        if store : 
            return Resource().dump(store),200
        return {"msg":"store not found"} , 404
        
    @classmethod
    def post (cls,name:str):
        store = StoreModel.find_by_name(name)
        if store :
            return {"msg":f"{Resource().dump(store)} already exists"},200

        store = StoreModel(name)
        try:
            store.save_to_db()
            return {"msg":f"item was crate {Resource().dump(store)}"},201
        except:
            return {"msg":"An error occurred inserting the item"},404
       
    @classmethod
    def delete (cls,name:str):
        store = StoreModel.find_by_name(name)
        
        if store:
            store.delete_from_db()
            return {"msg":"store was deleted"},202
        return {"msg":"store wasn't exists"},404 
        
class StoreList(Resource):
    @classmethod
    def get(cls):
        return {"items":StoreSchema(many=True).dump(StoreModel.get_all_row())},200