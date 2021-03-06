from db import db
from .items import ItemJSON
from typing import List , Dict, Union
StoreJSON = Dict[str,Union[str,List[ItemJSON]]]
class StoreModel(db.Model):
    __tablename__="store"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    # foreignkey
    items = db.relationship("ItemModel", lazy='joined')
    def __init__(self, name):
        self.name = name
      
    @classmethod
    def find_by_name(self, name:str)-> "StoreModel":
        return self.query.filter_by(name=name).first()
    
    @classmethod
    def get_all_row(self) -> List:
        return self.query.all()

    def save_to_db(self)-> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self)-> None:
        db.session.delete(self)
        db.session.commit()