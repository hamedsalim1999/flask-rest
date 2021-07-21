from db import db

class StoreModel(db.Model):
    __tablename__="store"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    # foreignkey
    items = db.relationship("ItemModel", lazy='dynamic')
    def __init__(self, name):
        self.name = name


    def json(self):
        return {'name': self.name, "items":[item.json() for item in self.items.all()]}
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    @classmethod
    def get_all_row(cls):

        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()