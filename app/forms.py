from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, FileField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('username')
    password = PasswordField('password')
    remember_me = BooleanField('remember_me', default=False)


class UserProfileForm(Form):
    name = StringField('username', validators=[DataRequired()])
    avator = FileField('avator')
