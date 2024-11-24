from datetime import datetime

from flask import Flask, render_template, request
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


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('login')
        password = request.form.get('password')

        # CRUD:
        # C - Create
        # R - Read
        # U - Update
        # D - Delete

        # Создание данных
        user = User(email=email, login=username, password=password)

        db.session.add(user)
        db.session.commit()
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Чтение данных
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            print(f'Успешная авторизация! {user.email}, {user.password}')
            return render_template('index.html')

        # Обновление данных
        # user.email = 'admin@gmail.com'
        # db.session.add(user)
        # db.session.commit()

        # Удаление данных
        # db.session.delete(user)
        # db.session.commit()

        print('Ошибка авторизации!')

    return render_template('login.html')


if __name__ == '__main__':
    app.run()
