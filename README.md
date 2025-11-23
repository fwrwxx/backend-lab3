# Expense Tracker


## Setup (Windows + PostgreSQL 15)

1. Встановити PostgreSQL
2. Створити БД: expense_tracker
3. У config.py прописати пароль
4. Встановити пакети:
pip install -r requirements.txt
5. Створити міграції:
flask db init
flask db migrate
flask db upgrade
6. Запустити:
flask run