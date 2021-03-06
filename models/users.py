from flask import request , url_for
from db import db
from lib.mailgun import MailGun
from typing import Dict, Union
import os
from decouple import config
from models.confirmation import ConfirmationModel
userJSON = Dict[str,Union[str,str]]
class UserModel(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    confirmation = db.relationship("ConfirmationModel",lazy='dynamic', cascade="all, delete-orphan")

    @property
    def most_recent_confirmation(self) -> "ConfirmationModel":
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()
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
        link = request.url_root[:-1]+ url_for('confirmation',confirmation_id=self.most_recent_confirmation.id)
        subject = f"Registration confirmation"
        text = f"plese click this link for confirm your registers {link} "
        html = f"<html> <h1>plese click this link for confirm your registers {link} </h1></html>"
        return MailGun.send_email([self.email,] ,subject,text,html)