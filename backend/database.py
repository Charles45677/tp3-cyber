import random
import hashlib
from datetime import datetime
 
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
 
app = Flask("BANKAPI")
 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banque.db"
db = SQLAlchemy(app)
  
 
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    account = db.relationship("Account", backref="user", uselist=False)
 
 
class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False, default=100.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
 
 
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()
 
 
def new_account_number():
    while True:
        number = str(random.randint(10000000, 99999999))
        if Account.query.filter_by(account_number=number).first() is None:
            return number
 
 
def populate_database():
    default_users = [
        {'username': 'Boromir', 'email': 'boromir@gmail.com', 'password': 'pass1234', 'admin': True, 'balance': 0},
        {'username': 'FLAG-4893895909', 'email': 'flag@gmail.com', 'password': 'pE$t#iEF5jM+@332JlI', 'admin': False, 'balance': 0},
        {'username': 'Pippin', 'email': 'pippin@gmail.com', 'password': 'password123', 'admin': False, 'balance': 500},
        {'username': 'Gandalf', 'email': 'gandalf@gmail.com', 'password': 'oWr2I#34qMO0**7#hU', 'admin': False, 'balance': 500},
        {'username': 'Arwen', 'email': 'arwen@gmail.com', 'password': 'MnU3##iu@9*&u^Y@8JG', 'admin': False, 'balance': 500},
        {'username': 'Galadriel', 'email': 'galadriel@gmail.com', 'password': 'word321', 'admin': False, 'balance': 500},
            ]
    for name, email, password, admin, balance in default_users:
        user = User(name=name, email=email, password=hash_password(password), admin=admin)
        db.session.add(user)
        db.session.flush()
        db.session.add(Account(user_id=user.id, account_number=new_account_number(), balance=balance))
    db.session.commit()
 
 
@app.route("/")
def hello():
    return jsonify({"message": "Welcome to the bank API."})
 
 
@app.route("/search", methods=["GET"])
def search_account():
    username = request.args.get("username", "")
    query = (
        "SELECT users.name, accounts.account_number FROM users "
        "JOIN accounts ON accounts.user_id = users.id "
        f"WHERE users.name = '{username}'"
    )
    try:
        rows = db.session.execute(text(query)).fetchall()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"results": [{"name": r[0], "account_number": r[1]} for r in rows]})
 
 
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if User.query.count() == 0:
            populate_database()
    app.run(debug=True, host="0.0.0.0", port=15555)