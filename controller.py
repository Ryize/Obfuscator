import random
import string

from flask import render_template, request, redirect, url_for, session, \
    make_response, flash, g
from flask_login import login_required, login_user, logout_user, current_user
from flask.wrappers import Response

from app import app, db
from business_logic.check_data import check_auth_data
from models import User, EmailConfirm
from mail import send_email


@app.route('/')
def index():
    users = User.query.all()
    title = 'Главная страница'
    flash({'title': "Регистрация", 'message': "Ошибка регистрации!"}, 'error')
    res = make_response(
        render_template('index.html',
                        persons=users,
                        title=title,
                        User=User)
    )
    res.set_cookie('username', 'John', max_age=60*60*24*3)
    return res


@app.route('/email-confirm/<code>')
def email_confirm(code):
    user_confirm = EmailConfirm.query.filter_by(code=code).first()
    if user_confirm:
        user = User.query.filter_by(login=user_confirm.login).first()
        user.email_confirm = True
        db.session.add(user)
        db.session.delete(user_confirm)
        db.session.commit()
        login_user(user)
    return redirect(url_for('register'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('login')
        password = request.form.get('password')

        if check_auth_data(username, password):
            user = User(email=email, login=username, password=password)
            code = ''.join(
                [random.choice(string.ascii_letters + string.digits) for i in
                 range(32)])
            user_confirm = EmailConfirm(login=username, code=code)

            db.session.add(user)
            db.session.add(user_confirm)
            db.session.commit()

            message = f'Ссылка для подтверждения почты: http://127.0.0.1:5000/email-confirm/{code}'

            send_email(message, email, 'Подтверждение почты')

    return render_template('auth.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email, password=password).first()
    if user and user.email_confirm:
        login_user(user)
        return redirect(session.get('url'))

    print('Ошибка авторизации!')
    return redirect(url_for('register'))


@app.route('/admin')
@login_required
def admin():
    print(request.cookies.get('username'))
    return render_template('admin.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_sign(response: Response):
    if response.status_code == 401:
        session['url'] = request.path
        # print(response.location)
        return redirect(url_for('register'))
    return response
