
//changer 

from flask import Flask, request, jsonify, make_response
import hashlib
import uuid
import datetime
import sys
import dbHandler
from flask_sqlachemy import SQLAlchemy

app = Flask("TODOAPI")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite.///./task.db'
db+SQLALchemy(app)

class User(db.Model):
        id=db.Column(db.Integer, primary_keys = True)
        public_id=db.Column(db.String(50), unique=True)
        name=db.Column(db.String(50),unique=True)
        password=db.Column(db.String(80))
        admin=db.Column(db.Boolean)
class Task(db.Model):
        id=db.Colmun(db.Integer,primary_keys = True)
        text= db.Column(db.String(500))
        complete=db.Column(db.Boolean)
        user_id = db.Column(db.Integer)

def wrap_user_in_dict(user):
        user_data={}
        user_data['id']=user.id
        user_data['public_id']=user.public_id
        user_data['name']=user.name
        user_data['password']=user.password
        user_data['admin']=user.admin
        return user_data

def wrap_task_in_dict(user):
        task_data={}
        task_data['id']=task.id
        task_data['text']=task.text
        task_data['complete']=task.complete
        task_data['user_id']=task.user_id
        return task_data

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
        rep['message'] = "Welcome to the task API."
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


@app.route('/task', methods=['GET'])
def get_all_tasks():
        #Should only be available to users (not admins)

        output = []
        tasks = Task.query.all()
        for task in tasks:
                output.append(wrap_task_in_dict(task))

        return jsonify({'tasks':output})


@app.route('/task/<task_id>', methods=['GET'])
def get_one_task(task_id):
        #Should only be available to users (not admins)
        task = Task.query.filter_by(id=task_id).first()
        task_data=""
        if task != None:
                task_data=wrap_task_in_dict(task)
        #output = dbHandler.get_one_task(task_id)
        return jsonify({'task':task_data})


@app.route('/task', methods=['POST'])
def create_task():
        #Should only be available to users (not admins)
        current_username = 0
        data = request.get_json()
        new_task = Task((text=data['text'],complete=False,user_id=current_username)
        db.session.add(new_task)
        db.session.commit()
        #dbHandler.create_task(data['text'], current_username)

        return jsonify({'message': 'Task created for ' + current_username})


@app.route('/task/<task_id>', methods=['PUT'])
def complete_task(task_id):
        #Should only be available to users (not admins)
        return jsonify({'message' : 'route complete task is not implemented'})



@app.route('/task/<task_id>', methods=['DELETE'])
def delete_task(task_id):
        #Should only be available to users (not admins)

        return jsonify({'message' : 'route delete task is not implemented'})

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
