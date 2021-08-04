from marshmallow import Schema , fields

class StoreSchema(Schema):
    id = fields.Integer()
    name = fields.Str(required=True)
