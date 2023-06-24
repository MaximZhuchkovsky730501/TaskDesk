import string

import cx_Oracle

from flask import Flask, render_template, request, redirect

app = Flask(__name__)


class User:

    def __init__(self, login: string):
        self.login = login


class WorkWithDB: # содержит набор функций для работы с БД

    def __init__(self):
        self.connection = None

    def open_connection(self): # установка соединения с БД с правами обычного пользователя
        self.connection = cx_Oracle.connect('user_access/1111@localhost/orcl')

    def close_connection(self): # разрыв соединения с БД
        self.connection.close()

    def login(self, login: string, password:string): # проверка введёного пароля
        self.open_connection()
        if password == self.runScript("select password from admin.users where login = '" + login + "'")[0]: # получаем пароль из БД и сравниваем его с введённым
            self.close_connection() # закрываем соединение с БД, что бы не висело пока никаких запросов не выполняется. потом наверное уберу отсюда
            return True
        else:
            self.close_connection()
            return False


    def get_user_info(self, login: string): # запрос на получения пользовательских данных
        script = "select id, firstname, lastname from admin.users where login = '" + login + "'"

    def get_user_privileges(self, id: int): # запрос на привелегий пользователя
        script = f"select privileges_id from ROLE_PRIVILEGES where role_id in (" \
                    f"select role_id from admin.user_roles where user_id = {id})"

    def runScript(self, script: string): # надо было удалить в ветке fixing-errors
        return self.run(script)

    def runScript(self, script: string): # выполняем скрипт, возвращает ответ от БД
        answer = self.run(script)
        return answer

    def run (self, script: string): # выполнение скрипта на БД
        cursor = self.connection.cursor() # получаем курсор (указатель/ссылка соединения)
        cursor.execute(script) # выполняем скрипт
        row = cursor.fetchone() # получаем ответ
        cursor.close()
        return row


workWithDB = WorkWithDB()

# тут уже скорее ты мне будешь объяснять что происходит
@app.route('/')
def index():
    return render_template('login.html') # показываем страницу аутентификации


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username'] # с помощью магии получаем логин и пароль
    password = request.form['password']

    # Validate the form data (e.g. check for empty fields)

    # Authenticate the user (e.g. check the database for the username and password)

    # If the user is authenticated, redirect to the dashboard
    if workWithDB.login(username, password): # проверяем есть ли такой пользователь в БД
        user = User(username)
        return redirect('/dashboard')
    return "no"


@app.route('/dashboard')
def dashboard():
    return 'Welcome to the dashboard'


if __name__ == '__main__':
    app.run()
