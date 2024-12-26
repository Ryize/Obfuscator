from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_toastr import Toastr
from flask_debugtoolbar import DebugToolbarExtension

from config import DATABASE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = 'hbdwhdwhdwhudw'
app.config['TOASTR_POSITION_CLASS'] = 'toast-bottom-left'
app.config['TOASTR_TIMEOUT'] = 3000
app.config['DEBUG_TB_ENABLED'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
db = SQLAlchemy(app)
manager = LoginManager(app)
toastr = Toastr(app)
toolbar = DebugToolbarExtension(app)
