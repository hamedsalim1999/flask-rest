from flask.helpers import url_for
from db import db
from flask import request
from typing import Dict, Union
userJSON = Dict[str,Union[str,str]]
MAILGUN_DOMAIN=""
MAILGUN_API_KEY=""
FROM_TITLE = ""
FROM_EMAIL =""


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
    def find_by_email(cls, email:str)-> "UserModel":
        return cls.query.filter_by(email=email).first()
    @classmethod
    def find_by_id(cls, id:int) -> "UserModel":
        return cls.query.filter_by(id=id).first()

    def save_to_db(self)-> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self)-> None:
        db.session.delete(self)
        db.session.commit()
      
    def sendconfern_email(self) -> None:
        link = request.url_root[:-1]+ url_for('userconfirm',user_id=self.id)
        
        return post(
            f"",
            auth=("api",API_KEY),
            data={
                "form":f"{FROM_TITLE}<{FROM_EMAIL}>",
                "to":self.email,
                "subject":"Registerion confirmation",
                "text":f"please click this link for active your account : {link}"
            }
        )