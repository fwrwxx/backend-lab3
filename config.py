import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:password123@localhost:5432/expense_tracker"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
