from db import db
from typing import List , Dict
class UserModel(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128), nullable=False)
    def __init__(self,username:str,password:str):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username:str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id:int):
        return cls.query.filter_by(id=id).first()
    
    def json(self)-> Dict:
        return{"id":self.id,"username":self.username}
    def save_to_db(self)-> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self)-> None:
        db.session.delete(self)
        db.session.commit()