from flask import Flask, request, abort, redirect, url_for, render_template
from markupsafe import escape
from database import Database

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        login_btn = request.form['login']
        if login_btn == 1:
            return login_get()
        register_btn = request.form['register']
        if register_btn == 2:
            return register_get()
    return render_template('index.html')

def register():
    if request.method == 'POST':
        return register_post()
    else:
        return render_template('register.html')

def register_post():
    reg_email = request.form['reg_email']
    reg_password = request.form['reg_pass']
    db.insert_users(reg_email, reg_password)
    return render_template('profile.html')

def register_get():
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return login_post()
    else:
        return login_get()

def login_get():
    return render_template('login.html')

def login_post():
    user_login = request.form('log_name')
    user_password = request.form ('log_pass')
    data = select_users(user_login)
    valid_password = data['password']
    error = "неверные данные или пароль"
    message = "добро пожаловать"
    if user_password == valid_password:
        return render_template('login.html')
    else:
        return redirect(url_for('login'))


    # def login_post():
    #     user_login = request.form.get('log_name')
    #     user_password = request.form.get('log_pass')
    #
    #     # Ищем пользователя в БД (функция возвращает словарь/кортеж или объект User)
    #     user = select_user(user_login)
    #     error = "Неверные данные или пароль"
    #
    #     # Проверяем, что пользователь найден и пароль совпадает
    #     if user and user['password'] == user_password:
    #         return render_template('profile.html')
    #     else:
    #         return render_template('login.html', error=error)


if __name__ == '__main__':
    db = Database('localhost', 'root', 'admin', 'academy')
    app.run(host='0.0.0.0', port=8080, debug=True)
