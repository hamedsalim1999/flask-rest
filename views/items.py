import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import JWT , jwt_required
from models.items import ItemModel
class Item(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('price',
        type=float,
        required=True,
        help="this field not can be blank"
        )
    
    

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
        item = ItemModel(name,data['price'])
        try:
            item.save_to_db()
            return {"msg":f"item was crate {item.json()}"}
        except:
            return {"msg":"An error occurred inserting the item"}
       

    def delete (self,name):
        item = ItemModel.find_by_name(name)
        
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
            item = ItemModel(name,data['price'])
        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        query = "SELECT * FROM items"
        connect = sqlite3.connect('mydb.db')
        cursor = connect.cursor()
        
        result = cursor.execute(query)
        item = []
        for row in result:
            item.append({
                "id":row[0],
                "name":row[1],
                "price":row[2],
            }
        )
        connect.close()
        return item