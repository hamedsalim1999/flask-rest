import sqlite3
from sqlite3.dbapi2 import Cursor

class User:
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
    # @classmethod
    # def find_by_password(cls,password):
    #     connect = sqlite3.connect('mydb.db')
    #     cursor = connect.cursor()
    #     query = "SELECT * FROM users WHERE password=?"
    #     result = cursor.execute(query,(password,))
    #     row = result.fetchone()
    #     if row:
    #         user=cls(*row)
    #     else:
    #         user= None
    #     connect.close()
    #     return user

