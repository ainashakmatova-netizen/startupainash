from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'productify-secret-key-2026')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

USERS_FILE = 'users.json'


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    return render_template('index.html', user=session.get('user'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password2 = request.form.get('password2', '')

        if not username or not email or not password:
            flash('Заполни все поля!', 'error')
            return render_template('register.html')

        if password != password2:
            flash('Пароли не совпадают!', 'error')
            return render_template('register.html')

        if len(password) < 4:
            flash('Пароль минимум 4 символа!', 'error')
            return render_template('register.html')

        users = load_users()

        for u in users:
            if u['username'] == username:
                flash('Такое имя уже занято!', 'error')
                return render_template('register.html')
            if u['email'] == email:
                flash('Этот email уже зарегистрирован!', 'error')
                return render_template('register.html')

        users.append({
            'username': username,
            'email': email,
            'password': password
        })
        save_users(users)

        session['user'] = username
        flash('Регистрация успешна! Добро пожаловать!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        users = load_users()
        for u in users:
            if u['username'] == username and u['password'] == password:
                session['user'] = username
                flash('Вы вошли в систему!', 'success')
                return redirect(url_for('index'))

        flash('Неверное имя или пароль!', 'error')
        return render_template('login.html')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Вы вышли из системы', 'success')
    return redirect(url_for('index'))


@app.route('/lock')
def lock():
    return render_template('lock.html')


@app.route('/unlock', methods=['POST'])
def unlock():
    text = request.form.get('task')
    file = request.files.get('photo')

    if not text or not file:
        return "Заполни всё!", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    return redirect(url_for('success'))


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
