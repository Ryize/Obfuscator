from flask import render_template, request, redirect, url_for

from app import app, db
from business_logic.check_data import check_auth_data
from models import User


@app.route('/')
def index():
    users = User.query.all()
    title = 'Главная страница'
    return render_template('index.html',
                           persons=users,
                           title=title,
                           User=User)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('login')
        password = request.form.get('password')

        if check_auth_data(username, password):
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
