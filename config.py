import os

DATABASE_URL = 'sqlite:///database.db'
EMAIL_LOGIN = os.environ.get('EMAIL_LOGIN')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')