from db import db

class ItemModel(db.Model):
    __tablename__="items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    # foreignkey
    store_id = db.Column(db.Integer,db.ForeignKey("store.id"))
    store = db.relationship('StoreModel')

    def __init__(self, name, price,store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
    def json(self):
        return {
            'name': self.name, 
            'price': self.price,
            }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all_row(cls):
        return {'items':  [x.json() for x in ItemModel.query.all()]}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()