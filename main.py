import string

import cx_Oracle

'''
from fastapi import FastAPI

server = FastAPI()
@server.get('/')
def home():
    return {"login:"}
'''

from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def connectionToDB(username: string):
    connection = cx_Oracle.connect('user_access/1111@localhost/orcl')
    cursor = connection.cursor()
    cursor.execute("select password from admin.users where login = '" + username + "'")
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return row[0]


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
    passw = connectionToDB(username)
    if password == passw:
        return redirect('/dashboard')
    return str(username) + " " + str(password) + " " + str(passw)


@app.route('/dashboard')
def dashboard():
    return 'Welcome to the dashboard'


if __name__ == '__main__':
    app.run()
