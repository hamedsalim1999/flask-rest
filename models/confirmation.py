from uuid import uuid4
from datetime import datetime,timedelta
from db import db

class ConfirmationModel(db.Model):
    __tablename__ = 'confirmations'
    id = db.Column(db.String(50),primary_key=True)
    expire_at = db.Column(db.Integer,nullable=False)
    confirmed = db.Column(db.Boolean,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    user = db.relationship("UserModel")
    def __init__(self,user_id : int,**kwargs) -> None:
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at=int(datetime.now()+timedelta(minutes=30))
        self.confirmed=False
        