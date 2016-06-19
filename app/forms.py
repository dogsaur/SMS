from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, \
    PasswordField, FileField, DecimalField, IntegerField, \
    SelectField
from wtforms.validators import DataRequired

from app.models import Supply, Product


class LoginForm(Form):
    username = StringField('username')
    password = PasswordField('password')
    remember_me = BooleanField('remember_me', default=False)


class AddUserForm(Form):
    username = StringField('username')
    password = PasswordField('password')
    user_type = SelectField('user_type', choices=[(1, '管理员'), (2, '收银员')])

class AddCustomerForm(Form):
    customer_name = StringField('customer_name')
    tel = StringField('tel')
    email = StringField('emali')
    is_vip = BooleanField('is_vip', default=False)
    vip_number = StringField('vip_number')


class UserProfileForm(Form):
    name = StringField('username')
    email = StringField('email')
    avator = FileField('avator')
    password = PasswordField('password')
    user_type = SelectField('user_type', choices=[(1, '管理员'), (2, '收银员')])


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
    # banker = StringField('banker')
    customer = StringField('customer')


class StockInventoryForm(Form):
    quantity = IntegerField('quantity')
    inprice = DecimalField('inprice')
    product_id = SelectField('product_id', choices=[(product.id, product.product_name) for product in Product.query.all()])
    supply_id = SelectField('supply_id', choices=[(supply.id, supply.name) for supply in Supply.query.all()])
