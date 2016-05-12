from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, FileField, DecimalField, IntegerField
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
    tel = StringField('tel', validators=[DataRequired()])
    address = StringField('address')
    email = StringField('email')
    manager = StringField('manager')
    payment_method = StringField('payment_method')
    bank_account = StringField('bank_account')
    evidence = StringField('evidence')


class ProductInfoForm(Form):
    name = StringField('name')
    category = StringField('category')
    bar_code = StringField('bar_code')
    size = StringField('size')
    image = FileField('image')
    inprice = DecimalField('inprice')
    price = DecimalField('price')
    supply = StringField('supply')


class AddTradeRecord(Form):
    bar_code = StringField('bar_code')
    quantity = IntegerField('quantity')
    banker = StringField('banker')
    customer = StringField('customer')
