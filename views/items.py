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
        self.connect = sqlite3.connect('mydb.db')
        self.cursor = self.connect.cursor()
    

    def get(self,name):
        query = "SELECT * FROM items WHERE name=?"
        result = self.cursor.execute(query,(name,))
        row = result.fetchone()
        self.connect.close()

        if row:
            return {'items':{'name':row[1],'price':row[2]}},200
        
        return {'items' : None} , 404
        

    def post (self,name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}
        data = self.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            Item.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}

        return item
       

    def delete (self,name):
        query = "DELETE FROM items WHERE name=?"
        self.cursor.execute(query,(name,))
        self.connect.commit()
        return {"msg":"item was deleted"}

    
    def put(self,name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        update_item = {'name':name,'price':data['price']}
        if item:
            ItemModel.update(update_item)
        else:
            ItemModel.insert(update_item)
            try:
                ItemModel.insert(update_item)
            except:
                return {"MSG":"An error occurred inserting the item"}
        return {"msg":"item was update"}

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