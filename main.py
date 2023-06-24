import string

import cx_Oracle

from flask import Flask, render_template, request, redirect

app = Flask(__name__)


class User:

    def __init__(self, login: string):
        self.login = login


class WorkWithDB:

    def __init__(self):
        self.connection = None

    def open_connection(self):
        self.connection = cx_Oracle.connect('user_access/1111@localhost/orcl')

    def close_connection(self):
        self.connection.close()

    def login(self, login: string, password:string):
        self.open_connection()
        if password == self.runScript("select password from admin.users where login = '" + login + "'")[0]:
            self.close_connection()
            return True
        else:
            self.close_connection()
            return False


    def get_user_info(self, login: string):
        script = "select id, firstname, lastname from admin.users where login = '" + login + "'"

    def get_user_privileges(self, id: int):
        script = f"select privileges_id from ROLE_PRIVILEGES where role_id in (" \
                    f"select role_id from admin.user_roles where user_id = {id})"

    def runScript(self, script: string):
        return self.run(script)

    def runScript(self, script: string):
        answer = self.run(script)
        return answer

    def run (self, script: string):
        cursor = self.connection.cursor()
        cursor.execute(script)
        row = cursor.fetchone()
        cursor.close()
        return row


workWithDB = WorkWithDB()
@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Validate the form data (e.g. check for empty fields)

    # Authenticate the user (e.g. check the database for the username and password)

    # If the user is authenticated, redirect to the dashboard
    if workWithDB.login(username, password):
        user = User(username)
        return redirect('/dashboard')
    return "no"


@app.route('/dashboard')
def dashboard():
    return 'Welcome to the dashboard'


if __name__ == '__main__':
    app.run()
