from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, FileField, DecimalField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('username')
    password = PasswordField('password')
    remember_me = BooleanField('remember_me', default=False)

class AddUserForm(Form):
	username = StringField('username')
	password = PasswordField('password')
	
class UserProfileForm(Form):
    name = StringField('username', validators=[DataRequired()])
    avator = FileField('avator')


class ProductInfoForm(Form):
    name = StringField('name')
    barcode = StringField('barcode')
    image = FileField('image')
    price = DecimalField('price')
