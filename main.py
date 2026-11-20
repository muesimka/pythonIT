import os

from flask import Flask, request, redirect, url_for, render_template
from werkzeug.security import check_password_hash, generate_password_hash

from databases import Database

app = Flask(__name__)

# Подключение создаётся при запуске приложения, а не при импорте модуля.
# Это позволяет запускать тесты без установленной/запущенной MySQL.
db = None


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    reg_email = request.form.get('reg_email', '').strip()
    reg_password = request.form.get('reg_pass', '')

    if not reg_email or not reg_password:
        return render_template('register.html', error='Заполните все поля')

    try:
        db.insert_users(reg_email, generate_password_hash(reg_password))
    except Exception:
        # Например, адрес уже зарегистрирован или база данных недоступна.
        return render_template('register.html', error='Не удалось зарегистрироваться. Проверьте данные.')

    return render_template('profile.html', class_name=reg_email, places=None, error=None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    user_login = request.form.get('log_name', '').strip()
    user_password = request.form.get('log_pass', '')

    if not user_login or not user_password:
        return render_template('login.html', error='Введите почту и пароль')

    user = db.select_users(user_login)
    if user:
        stored_password = user.get('password', '')
        # Поддерживаем и старые записи с паролем в открытом виде,
        # и новые записи с хешированным паролем.
        password_ok = (
            check_password_hash(stored_password, user_password)
            if stored_password.startswith(('scrypt:', 'pbkdf2:'))
            else stored_password == user_password
        )
        if password_ok:
            return render_template(
                'profile.html', class_name=user_login, places=None, error=None
            )

    return render_template('login.html', error='Неверная почта или пароль')


if __name__ == '__main__':
    db = Database(
        os.getenv('DB_HOST', 'localhost'),
        os.getenv('DB_USER', 'root'),
        os.getenv('DB_PASSWORD', 'admin'),
        os.getenv('DB_NAME', 'academy'),
    )
    app.run(host='0.0.0.0', port=8080, debug=True)
