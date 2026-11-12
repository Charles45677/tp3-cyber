import sqlite3

def create_connection():
        db_file = "./tasks.db"
        conn = None
        try:
                conn = sqlite3.connect(db_file)
        except Error as e:
                print(e)
        return conn

def get_all_account():
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM task")

        rows = cur.fetchall()
        accounts = []
        for row in rows:
                account_data = {}
                account_data['id'] = row[0]
                account_data['text'] = row[1]
                account_data['complete'] = row[2]
                account_data['user_id'] = row[3]
                account.append(task_data)
        conn.close()
        return accounts

def get_one_account(account_id):
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM task WHERE id = " + task_id)

        row = cur.fetchall()[0]
        print("ROW:" + str(row))
        task_data = {}
        task_data['id'] = row[0]
        task_data['text'] = row[1]
        task_data['complete'] = row[2]
        task_data['user_id'] = row[3]
        conn.close()
        return task_data

def create_account(text, user_id):
        conn = create_connection()
        cur = conn.cursor()
        cur.executescript("INSERT INTO task (text, complete, user_id) VALUES('" + text + "', 'False', '" + user_id + "');")
        conn.commit()
        conn.close()

def get_all_users():
        print("In get all users.", flush=True)
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM user;")

        rows = cur.fetchall()
        users = []
        print("nb rows: " + str(len(rows)), flush=True)
        for row in rows:
                print("another user", flush=True)
                user_data = {}
                user_data['id'] = row[0]
                user_data['public_id'] = row[1]
                user_data['name'] = row[2]
                user_data['admin'] = row[4]
                users.append(user_data)
        conn.close()
        return users

def create_user(uuid, name, password, isAdmin):
        conn = create_connection()
        cur = conn.cursor()
        cur.executescript("INSERT INTO user (public_id, name, password, admin) VALUES('" + uuid + "', '" + name + "', '" + password + "', False);")
        conn.commit()
        conn.close()
