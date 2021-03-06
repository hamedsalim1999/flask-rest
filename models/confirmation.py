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
        self.expire_at=datetime.now()+timedelta(minutes=30)
        self.confirmed=False
    @classmethod
    def find_by_id(cls, id:int) -> "ConfirmationModel":
        return cls.query.filter_by(id=id).first()
    @classmethod
    def expired(self) -> bool:
        return datetime.now() > self.expire_at
    def force_to_expire(self) -> None:
        if not self.expired:
            self.expire_at = int(datetime.now())
            self.save_to_db()

    def save_to_db(self)-> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self)-> None:
        db.session.delete(self)
        db.session.commit()