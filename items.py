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
    # @jwt_required()
    def get(self,name):
        query = "SELECT * FROM items WHERE name=?"
        result = self.cursor.execute(query,(name,))
        row = result.fetchone()
        self.connect.close()

        if row:
            return row , 200 if row is not None else 404
        
        return {'items' : None} , 404
        # return{"Student":name}
    # def post(self,name):
    #     item = next(filter(lambda x : x['name'] == name , datas),None) 
    #     data = self.parser.parse_args()
    #     if item:
    #         return "we have this item"
    #     else:
    #         datas.append({'name':name,'price':data['price']})
    #         return f"item was create"
    # def delete(self,name):
    #     item = next(filter(lambda x : x['name'] == name , datas),None) 
    #     if item:
    #         datas.remove(item)
    #         return f"items was deleted"
    #     else:
    #         return "we dont have this item "
    # def put(self,name):
    #     item = next(filter(lambda x : x['name'] == name , datas),None) 
    #     data = self.parser.parse_args()
    #     if item:
    #         item.update({'name':name,'price':data['price']})
    #         return f"items was update"
    #     else:
    #         datas.append({'name':name,'price':data['price']})   
    #         return "iteam was crate"   