
//changer 

from flask import Flask, request, jsonify, make_response
import hashlib
import uuid
import datetime
import sys
import dbHandler
from flask_sqlachemy import SQLAlchemy

app = Flask("TODOAPI")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite.///./account.db'
db+SQLALchemy(app)

class User(db.Model):
	id=db.Column(db.Integer, primary_keys = True)
	public_id=db.Column(db.String(50), unique=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	name=db.Column(db.String(50),unique=True)
	password=db.Column(db.String(80))
	admin=db.Column(db.Boolean)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	accounts = db.relationship('Account', backref='user', lazy=True)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False, default=100.0)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Token(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	code=db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
	used = db.Column(db.Boolean)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FaqMessage(db.Model);
	id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(200), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Account(db.Model):
        id=db.Column(db.Integer,primary_keys = True)
        text= db.Column(db.String(500))
        complete=db.Column(db.Boolean)
        user_id = db.Column(db.Integer)

def wrap_user_in_dict(user):
        user_data={}
        user_data['id']=user.id
        user_data['email']=user.email
        user_data['name']=user.name
        user_data['password']=user.password
        user_data['admin']=user.admin
        user_data['created_at']=user.created_at
        user_data['accounts']=user.accounts
        return user_data

def wrap_account_in_dict(account):
        account_data={}
        account_data['id']=account.id
        user_data['public_id']=user.public_id
        account_data['account_number']=account.account_number
        account_data['balance']=account.balance
		account_data['created_at']=account.created_at
        account_data['user_id']=account.user_id
        return account_data

def generate_password_hash(password):
        hash = hashlib.md5(password.encode())
        print(hash.hexdigest(), flush=True)
        return hash.hexdigest()

def getInitialClientIP(request):
        print("trying to get IP", flush=True)
        ip = None

        if(request.data):
                if request.is_json:
                        data = request.get_json()
                        if 'ip' in data:
                                ip = data['ip']
                else:
                        print("not in json", flush=True)

        if ip == None: #No Ip found in the request json body, so the request should come directly from client.
                ip = request.remote_addr
        return ip


@app.route('/')
def hello():
        rep = dict()
        rep['message'] = "Welcome to the account API."
        ip = getInitialClientIP(request)
        rep['ip'] = ip

        print(str(rep), flush=True)
        return rep

@app.route('/user', methods=['GET'])
def get_all_users():
        #Should only be available to admin
        print("get all user route", flush=True)
        users = User.query.all()
        output = []
        for user in users:
                output.append.(wrap_user_in_dict(user))
        return jsonify({'users': output})

@app.route('/user/<p_id>', methods=['GET'])
def get_one_user(p_id):
        #Should only be available to admin and the actual user p_id

        return jsonify({'message' : 'route get one user is not implemented'})


@app.route('/user', methods=['POST'])
def create_user():
        #Should only be available to admin

        data = request.get_json()
        hashed_password = generate_password_hash(data['password'])
        new_user  = User(public_id=str(uuid.uuid4())), name = data['name'], password =  hashed_password,admin=False)
        db.session.add(new_user)
        db.session.commit()
        #dbHandler.create_user(str(uuid.uuid4()), data['name'], hashed_password, False)
        return jsonify({'message': 'new user created'})

@app.route('/user/<p_id>', methods=['PUT'])
def promote_user(p_id):
        #Should only be available to admin

        return jsonify({'message' : 'route promote user is not implemented'})


@app.route('/user/<p_id>', methods=['DELETE'])
def delete_user(p_id):
        #Should only be available to admin

        return jsonify({'message' : 'route delete user is not implemented'})


@app.route('/account', methods=['GET'])
def get_all_accounts():
        #Should only be available to users (not admins)

        output = []
        accounts = Account.query.all()
        for account in accounts:
                output.append(wrap_account_in_dict(account))

        return jsonify({'accounts':output})


@app.route('/account/<account_id>', methods=['GET'])
def get_one_account(account_id):
        #Should only be available to users (not admins)
        account = Account.query.filter_by(id=account_id).first()
        account_data=""
        if account != None:
                account_data=wrap_account_in_dict(account)
        #output = dbHandler.get_one_account(account_id)
        return jsonify({'account':account_data})


@app.route('/account', methods=['POST'])
def create_account():
        #Should only be available to users (not admins)
        current_username = 0
        data = request.get_json()
        new_account = Account((text=data['text'],complete=False,user_id=current_username)
        db.session.add(new_account)
        db.session.commit()
        #dbHandler.create_account(data['text'], current_username)

        return jsonify({'message': 'Account created for ' + current_username})


@app.route('/account/<account_id>', methods=['PUT'])
def complete_account(account_id):
        #Should only be available to users (not admins)
        return jsonify({'message' : 'route complete account is not implemented'})



@app.route('/account/<account_id>', methods=['DELETE'])
def delete_account(account_id):
        #Should only be available to users (not admins)

        return jsonify({'message' : 'route delete account is not implemented'})

@app.route('/login', methods=['post'])
def login():
        return jsonify({'message' : 'login route is not implemented'})


if __name__ == '__main__':
        with app.app.context():
                db.create_all() #Just need to be executed on first run to create the actual DB, but subsequent execution are harmless as far the de demo is concerned.
        if len(sys.argv) > 2:
                print("Too many arguments. Use 0 for normal use, 1 (password for Admin account) for creating DB... aborting.")
        if len(sys.argv) == 2:
                #We have an argument so we'll try to initialize the DB
                #TODO We could check to make sure the Admin user does not already exists...
                print("Admin password will be: " + sys.argv[1])
                hashed_password = generate_password_hash(sys.argv[1])
                new_user = User(public_id=str(uuid.uuid4()), name='Admin', password=hashed_password, admin=True)
                db.session.add(new_user)
                db.session.commit()

        app.run(debug=True, host='0.0.0.0', port=15555)
