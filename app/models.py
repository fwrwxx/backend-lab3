from .extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    accounts = db.relationship("Account", backref="user", cascade="all, delete")

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ⚠ посилання на users.id
    name = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    records = db.relationship("Record", backref="account", cascade="all, delete")

class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)  # ⚠ посилання на accounts.id
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # income / expense
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
