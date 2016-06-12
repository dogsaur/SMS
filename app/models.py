from app import db
from flask import url_for


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(64), db.ForeignKey('image.id'), index=True, unique=True)
    password = db.Column(db.String(64))
    name = db.Column(db.String)
    email = db.Column(db.String(128), index=True, unique=True)
    avator_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    group = db.Column(db.Integer, default=1)
    right = db.Column(db.Integer, default=1)

    def info_link(self):
        return url_for(str('user'), username=self.username)

    def avatar(self):
        img_id = self.avator_id
        if img_id is None or Image.query.get(img_id) is None:
            return url_for('static', filename='./avatars/default.jpg')
        return Image.query.get(img_id).get_url()

    def __repr__(self):
        return '<User %r, group:%r, right:%r>' % (
            self.username, self.group, self.right)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        try:
            return unicode(self.id)  # for python 2
        except NameError:
            return str(self.id)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String)

    def __repr__(self):
        return '<Image file = %r>' % (self.path)

    def get_url(self):
        return url_for('static', filename=self.path)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String)
    tel = db.Column(db.String)
    email = db.Column(db.String)
    is_vip = db.Column(db.Boolean)
    vip_number = db.Column(db.Integer)

    def __repr__(self):
        return 'Customer<%s %s %s>' % (self.customer_name,
                                       self.email,
                                       self.is_vip)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)
    category = db.Column(db.String)
    bar_code = db.Column(db.Integer)
    size = db.Column(db.String)
    inprice = db.Column(db.Numeric)
    price = db.Column(db.Numeric)
    supply_id = db.Column(db.Integer, db.ForeignKey('supply.id'))
    picture_id = db.Column(db.Integer, db.ForeignKey('image.id'))

    def picture(self):
        picture_id = self.picture_id
        if picture_id is None:
            return url_for('static', filename='./avatars/default.jpg')
        return Image.query.get(picture_id).get_url()

    def supply(self):
        if self.supply_id is not None:
            return Supply.query.get(self.supply_id)
        else:
            return ''

    def __repr__(self):
        return '<Product name=%r, price=%r>' % (self.product_name, self.price)


class TradeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Numeric)
    time = db.Column(db.DateTime)

    def product_name(self):
        product = Product.query.get(self.product_id)
        if product is not None:
            return product.product_name
        return "product_name"

    def product_price(self):
        product = Product.query.get(self.product_id)
        if product is not None:
            return product.price
        return "product_price"

    def get_product(self):
        return Product.query.get(self.product_id)

    def get_customer(self):
        return Customer.query.get(self.customer_id)

    def get_casher(self):
        return User.query.get(self.userid)

    def __repr__(self):
        return "TradeRecord<%s, %s, %s>" % (self.product_name(),
                                            self.product_price(), self.time)


class Supply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer)
    city = db.Column(db.String)
    buyer = db.Column(db.String)
    order_contact = db.Column(db.String)
    tel = db.Column(db.String)
    address = db.Column(db.String)
    email = db.Column(db.String)
    manager = db.Column(db.String)
    payment_method = db.Column(db.String)
    bank_account = db.Column(db.String)
    evidence = db.Column(db.String)

    def __repr__(self):
        return '<Supply name=%r, city=%r>' % (self.name, self.city)
