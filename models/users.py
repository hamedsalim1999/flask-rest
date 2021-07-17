import sqlite3
from db import db
class UserModel:
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    def __init__(self,_id,username,password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls,username):
        connect = sqlite3.connect('mydb.db')
        cursor = connect.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query,(username,))
        row = result.fetchone()
        if row:
            user=cls(*row)
        else:
            user= None
        connect.close()
        return user
    @classmethod
    def find_by_id(cls,_id):
        connect = sqlite3.connect('mydb.db')
        cursor = connect.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query,(_id,))
        row = result.fetchone()
        if row:
            user=cls(*row)
        else:
            user= None
        connect.close()
        return user
