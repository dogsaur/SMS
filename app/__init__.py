from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf.csrf import CsrfProtect
from flask.ext.principal import Principal, Permission, RoleNeed


app = Flask(__name__)
app.config.from_object('config')
csrf = CsrfProtect()
csrf.init_app(app)

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

Principal(app)
admin_permission = Permission(RoleNeed(1))

avators = UploadSet('avators', IMAGES)
configure_uploads(app, avators)

pics = UploadSet('pics', IMAGES)
configure_uploads(app, pics)


from app import views, models
