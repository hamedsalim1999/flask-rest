from uuid import uuid4
from datetime import datetime
from db import db

class ConfirmationModel(db.Model):
    __tablename__ = 'confirmations'
    id = db.Column(db.String(50),primary_key=True)
    expire_at = db.Column(db.Integer,nullable=False)
    confirmed = db.Column(db.Boolean,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    user = db.relationship("UserModel")