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


    @jwt_required()
    def get(self,name):
        query = "SELECT * FROM items WHERE name=?"
        result = self.cursor.execute(query,(name,))
        row = result.fetchone()
        self.connect.close()

        if row:
            return {'items':{'name':row[1],'price':row[2]}},200
        
        return {'items' : None} , 404
        

    def post (self,name):
        data = self.parser.parse_args()
        query = "INSERT INTO items VALUES (NULL,?,?)"
        self.cursor.execute(query,(name,data["price"]))
        self.connect.commit()
        return {"msg":"item was create"}


    def delete (self,name):
        query = "DELETE FROM items WHERE id=?"
        self.cursor.execute(query,(name,))
        self.connect.commit()
        return {"msg":"item was deleted"}