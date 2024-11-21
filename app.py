from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('login')
        password = request.form.get('password')
        print(email, username, password)
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
