from db import db
from typing import List , Dict, Union
userJSON = Dict[str,Union[str,str]]
class UserModel(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    activate = db.Column(db.Boolean, default=False)


    @classmethod
    def find_by_username(cls, username:str)-> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id:int) -> "UserModel":
        return cls.query.filter_by(id=id).first()

    def save_to_db(self)-> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self)-> None:
        db.session.delete(self)
        db.session.commit()