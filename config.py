import os
basedir = os.path.abspath(os.path.dirname(__file__))

# sql
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SQLALCHEMY_TRACK_MODIFICATIONS = True
# login
WTF_CSRF_ENABLED = False

SECRET_KEY = 'iskisxfafxnflxia;'

# file uploads
UPLOADED_AVATORS_DEST = 'app/static/avatars'
UPLOADED_PICS_DEST = 'app/static/pics'

