DEBUG = True

import os.path
base_dir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'todolist_db.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = b'\xdd\x8b\xad\x13\xf8\xda-\xfd\xa2c\\B\x1a\xed4\xb1'