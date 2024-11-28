from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(48), unique=True)
    login = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('login')
        password = request.form.get('password')

        user = User(email=email, login=username, password=password)

        db.session.add(user)
        db.session.commit()
    return render_template('auth.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email, password=password).first()
    if user:
        print(f'Успешная авторизация! {user.email}, {user.password}')
        return redirect(url_for('index'))

    print('Ошибка авторизации!')
    return redirect(url_for('register'))


if __name__ == '__main__':
    app.run()

    # MVC:
    # M - Model (models.py)
    # V - Views (templates)
    # C - Controller (controller.py)

    # Обязательно:
    # main.py (запуск проект)
    # errors.py (обработку ошибок. 404)
    # mail.py (работа с почтой)
    # business_logic(.py?), так как это может быть директорию с кучей файлов
    # бизнес логики

    # Не обязательно:
    # admin.py (админ-панель сайта)
    # config.py (секреты)
