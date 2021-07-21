import sqlite3
from models.store import StoreModel
from flask_restful import Resource,reqparse


class Store(Resource):


    def get(self,name):
        store =  StoreModel.find_by_name(name)
        if store : 
            return store.json()
        return {"msg":"store not found"} , 404
        

    def post (self,name):
        store = StoreModel.find_by_name(name)
        if store :
            return {"msg":f"{store.json()} already exists"}

        store = StoreModel(name)
        try:
            store.save_to_db()
            return {"msg":f"item was crate {store.json()}"}
        except:
            return {"msg":"An error occurred inserting the item"}
       

    def delete (self,name):
        store = StoreModel.find_by_name(name)
        
        if store:
            store.delete_from_db()
            return {"msg":"store was deleted"}
        return {"msg":"store wasn't exists"}
        
class StoreList(Resource):
    def get(self):
        return StoreModel.get_all_row()