from flask import Blueprint, request, jsonify
from .models import User, Account, Record
from .extensions import db
from .schemas import user_schema, users_schema, account_schema, accounts_schema, record_schema, records_schema

api_bp = Blueprint('api', __name__)

# Users
@api_bp.post('/users')
def create_user():
    data = request.json
    user = User(name=data['name'])
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)

@api_bp.get('/users')
def get_users():
    return users_schema.jsonify(User.query.all())

# Accounts
@api_bp.post('/accounts')
def create_account():
    data = request.json
    acc = Account(user_id=data['user_id'], name=data['name'], balance=data.get('balance', 0))
    db.session.add(acc)
    db.session.commit()
    return account_schema.jsonify(acc)

@api_bp.get('/accounts')
def get_accounts():
    return accounts_schema.jsonify(Account.query.all())

# Records
@api_bp.post('/records')
def create_record():
    data = request.json
    acc = Account.query.get(data['account_id'])

    if not acc:
        return {"error": "account not found"}, 404

    amount = float(data['amount'])
    rec_type = data['type']

    if rec_type == "income":
        acc.balance += amount
    elif rec_type == "expense":
        acc.balance -= amount
    else:
        return {"error": "invalid type"}, 400

    rec = Record(account_id=acc.id, amount=amount, type=rec_type)

    db.session.add(rec)
    db.session.commit()

    return record_schema.jsonify(rec)

@api_bp.get('/records')
def get_records():
    return records_schema.jsonify(Record.query.all())