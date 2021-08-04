from marshmallow import Schema , fields

class ItemSchema(Schema):
    id = fields.Integer()
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Integer(required=True)