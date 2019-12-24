DEBUG = True

import os.path
base_dir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'todolist_db.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'um-nome-bem-seguro'