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

class AddSupplyForm(Form):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city')
    buyer = StringField('buyer')
    order_contact = StringField('order_contact')
    contact_information = StringField('contact_information',validators=[DataRequired()])



class ProductInfoForm(Form):
    name = StringField('name')
    barcode = StringField('barcode')
    image = FileField('image')
    price = DecimalField('price')
