import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import JWT , jwt_required

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

    @classmethod
    def insert(cls,item):
        query = "INSERT INTO items VALUES (NULL,?,?)"
        connect = sqlite3.connect('mydb.db')
        cursor = connect.cursor()
        cursor.execute(query,(item["name"],item["price"]))
        connect.commit()
        connect.close()
    
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('mydb.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[1], 'price': row[2]}}

    @classmethod
    def update(cls,item):
        query = "UPDATE items SET price=? WHERE name=?"
        connect = sqlite3.connect('mydb.db')
        cursor = connect.cursor()
        cursor.execute(query,(item["price"],item["name"]))
        connect.commit()
        connect.close()


    def get(self,name):
        query = "SELECT * FROM items WHERE name=?"
        result = self.cursor.execute(query,(name,))
        row = result.fetchone()
        self.connect.close()

        if row:
            return {'items':{'name':row[1],'price':row[2]}},200
        
        return {'items' : None} , 404
        

    def post (self,name):
        if self.find_by_name(name):
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
        item = self.find_by_name(name)
        update_item = {'name':name,'price':data['price']}
        if item:
            self.update(update_item)
        else:
            self.insert(update_item)
            try:
                self.insert(update_item)
            except:
                return {"MSG":"An error occurred inserting the item"}
        return {"msg":"item was update"}

