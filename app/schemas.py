from .extensions import ma
from marshmallow import fields

class UserSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)

class AccountSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    name = fields.Str(required=True)
    balance = fields.Float()

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)

class RecordSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    account_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    type = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)

record_schema = RecordSchema()
records_schema = RecordSchema(many=True)