from flask import Blueprint, request, jsonify
from .models import User, Account, Record
from .extensions import db
from .schemas import user_schema, users_schema, account_schema, accounts_schema, record_schema, records_schema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from passlib.hash import pbkdf2_sha256

api_bp = Blueprint('api', __name__)

# ------------------------
# AUTH — Реєстрація
# ------------------------
@api_bp.post("/register")
def register():
    data = request.json

    if User.query.filter_by(username=data["username"]).first():
        return {"error": "Username already exists"}, 400

    user = User(
        username=data["username"],
        password=pbkdf2_sha256.hash(data["password"])
    )

    db.session.add(user)
    db.session.commit()

    return {"message": "User created successfully"}, 201


# ------------------------
# AUTH — Логін
# ------------------------
@api_bp.post("/login")
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()

    if user and pbkdf2_sha256.verify(data["password"], user.password):
        token = create_access_token(identity=user.id)
        return {"access_token": token}, 200

    return {"error": "Invalid credentials"}, 401


# ------------------------
# USERS (Захищені)
# ------------------------
@api_bp.get('/users')
@jwt_required()
def get_users():
    return users_schema.jsonify(User.query.all())

# ------------------------
# ACCOUNTS (Захищені)
# ------------------------
@api_bp.post('/accounts')
@jwt_required()
def create_account():
    data = request.json
    user_id = get_jwt_identity()

    acc = Account(user_id=user_id, name=data['name'], balance=data.get('balance', 0))
    db.session.add(acc)
    db.session.commit()
    return account_schema.jsonify(acc)

@api_bp.get('/accounts')
@jwt_required()
def get_accounts():
    user_id = get_jwt_identity()
    return accounts_schema.jsonify(Account.query.filter_by(user_id=user_id).all())

# ------------------------
# RECORDS (Захищені)
# ------------------------
@api_bp.post('/records')
@jwt_required()
def create_record():
    data = request.json
    acc = Account.query.get(data['account_id'])

    if not acc or acc.user_id != get_jwt_identity():
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
@jwt_required()
def get_records():
    user_id = get_jwt_identity()
    user_accounts = Account.query.filter_by(user_id=user_id).all()
    ids = [a.id for a in user_accounts]
    return records_schema.jsonify(Record.query.filter(Record.account_id.in_(ids)).all())
