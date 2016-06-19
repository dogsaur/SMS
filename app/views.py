# encoding: utf-8
import time, datetime
from flask import render_template, request, \
    flash, redirect, session, url_for, g, \
    current_app
from flask.ext.login import login_user, \
    logout_user, login_required, current_user
from flask.ext.principal import Identity, \
    AnonymousIdentity, identity_changed, \
    identity_loaded, RoleNeed, UserNeed
from app import app, db, lm, avators, pics, admin_permission
from .forms import LoginForm, UserProfileForm, \
    ProductInfoForm, AddUserForm, AddSupplyForm, \
    AddTradeRecord, StockInventoryForm,AddCustomerForm
from .models import User, Image, Customer, \
    Product, TradeRecord, Supply, StockRecord


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
#@admin_permission.require()
def index():
    user = g.user
    if user.group == 1:
        data = [1,2,3,4,5,6,7,5,7,1,9]
        return render_template('index1.html',
                               title='Home',
                               user=user,
                               data=data)
    else:
        form = AddTradeRecord()
        commited = False
        if form.validate_on_submit():
            traderecord = TradeRecord()
            bar_code = form.bar_code.data
            product = Product.query.filter_by(bar_code=bar_code).first()
            if product is not None:
                if not commited:
                    traderecord.product_id = product.id
                    traderecord.quantity = form.quantity.data
                    traderecord.userid = g.user.id
                    traderecord.customer_id = Customer.query.filter_by(customer_name=form.customer.data).first().id
                    traderecord.time = datetime.datetime.now()
                    db.session.add(traderecord)
                    db.session.commit()
                    commited = True
                    return render_template("casher_index.html", traderecord=traderecord, form=form)
                else:
                    form = AddTradeRecord()
                    traderecord = TradeRecord()
                    commited = False
        return render_template("casher_index.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.password == form.password.data:
            login_user(user)
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))
            return redirect(url_for('index'))
    return render_template('login.html',
                           title='登陆',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return redirect(url_for('index'))


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'group'):
        print(current_user.id, current_user.group)
        identity.provides.add(RoleNeed(current_user.group))


@app.route('/user/<username>')
@login_required
@admin_permission.require(http_exception=403)
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User ' + username + ' not found.')
        return redirect(url_for('index'))
    return render_template('user.html', user=user)


@app.route('/product_info/<product_id>')
@login_required
@admin_permission.require(http_exception=403)
def product_info(product_id):
    product = Product.query.get(product_id)
    if product_id is None:
        flash('Product ' + product_id + 'not found.')
        return redirect(url_for('index'))
    return render_template('product_info.html', product=product)


@app.route('/add_user', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def add_user():
    form = AddUserForm()
    if form.is_submitted():
        user = User()
        user.username = form.username.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
    return render_template("add_user.html", form=form)

@app.route('/add_customer', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def add_customer():
    form = AddCustomerForm()
    if form.validate_on_submit():
        customer = Customer()
        customer.customer_name = form.customer_name.data
        customer.tel = form.tel.data
        customer.email = form.email.data
        customer.is_vip = form.is_vip.data
        customer.vip_number = form.vip_number.data
        db.session.add(customer)
        db.session.commit()
    return render_template("add_customer.html", form=form)


@app.route('/remove_customer/<customer_id>', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def remove_customer(customer_id):
    cu = Customer.query.get(customer_id)
    if cu is not None:
        db.session.delete(cu)
        db.session.commit()
    return redirect(url_for('customers'))


@app.route('/remove_supply/<supply_id>', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def remove_supply(supply_id):
    supply = Supply.query.get(supply_id)
    if supply is not None:
        db.session.delete(supply)
        db.session.commit()
    return redirect(url_for('suppliers'))

@app.route('/remove_user/<user_id>', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def remove_user(user_id):
    user = User.query.get(user_id)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('staffs'))

@app.route('/remove_product/<product_id>', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def remove_product(product_id):
    product = Product.query.get(product_id)
    if product is not None:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('products'))


@app.route('/add_supply', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def add_supply():
    form = AddSupplyForm()
    if form.validate_on_submit():
        supply = Supply()
        supply.name = form.name.data
        supply.city = form.city.data
        supply.buyer = form.buyer.data
        supply.order_contact = form.order_contact.data
        supply.tel = form.tel.data
        db.session.add(supply)
        db.session.commit()
    return render_template("add_supply.html", form=form)


@app.route('/add_traderecord', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def add_traderecord():
    form = AddTradeRecord()
    if form.validate_on_submit():
        traderecord = TradeRecord()
        bar_code = form.bar_code.data
        product = Product.query.filter_by(bar_code=bar_code)
        if product is not None:
            traderecord.product_id = product.id
            traderecord.quantity = form.quantity.data
            traderecord.banker = form.banker.data
            traderecord.customer = form.customer.data
            traderecord.time = time.localtime(time.time())
            db.session.add(traderecord)
            db.session.commit()
            return render_template("add_traderecord.html", traderecord=traderecord)
    return render_template("add_traderecord.html", form=form)


@app.route('/edit_profile/<uid>', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def edit_user_profile(uid):
    user = User.query.get(uid)
    if user is None:
        user = User()
    form = UserProfileForm(name=user.name,
                           email=user.email,
                           password=user.password,
                           user_type=user.group)
    if form.is_submitted():
        app.logger.error('edit_user validate')
        filename = avators.save(request.files['avator'])
        img = Image(path="avatars/" + filename)
        db.session.add(img)
        db.session.commit()
        user.avator_id = img.id

        if form.name is not None:
            user.name = form.name.data
        if form.email is not None:
            user.email = form.email.data
        if form.password is not None:
            user.password = form.password.data
        if form.user_type is not None:
            user.group = form.user_type.data
        db.session.add(user)
        db.session.commit()
        # g.user.store()
        flash('photo saved')
        return redirect(url_for('index'))
    return render_template('edit-user-profile.html', form=form)


@app.route('/trade')
@login_required
@admin_permission.require(http_exception=403)
def trade():
    trades = TradeRecord.query.all()
    return render_template('trade.html', trades=trades, Product=Product)


@app.route('/customers')
@login_required
@admin_permission.require(http_exception=403)
def customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)


@app.route('/products', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def products():
    products = Product.query.all()
    stock_form = StockInventoryForm()
    app.logger.error('before stock_form validate')
    app.logger.error(stock_form.errors)
    app.logger.error(stock_form.is_submitted())
    app.logger.error(stock_form.validate_on_submit())
    if stock_form.is_submitted():
        app.logger.error('stock_form validate')
        stock_record = StockRecord()
        stock_record.quantity = stock_form.quantity.data
        stock_record.supply_id = stock_form.supply_id.data
        stock_record.inprice = stock_form.inprice.data
        stock_record.product_id = stock_form.product_id.data

        app.logger.error(stock_record)
        product = Product.query.get(stock_record.product_id)
        if product.inventory is None:
            product.inventory = 0
        product.inventory += stock_record.quantity
        try:
            db.session.add(stock_record)
            db.session.commit()
        except Exception as e:
            app.logger.error(e)

        app.logger.error(stock_form.supply_id)
    return render_template('products.html',
                           products=products,
                           stock_form=stock_form)


@app.route('/edit_product/<product_id>', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def edit_product(product_id):
    product = Product.query.get(product_id)
    if product is not None:
        form = ProductInfoForm(name=product.product_name,
                               category=product.category,
                               bar_code=product.bar_code,
                               size=product.size,
                               inprice=product.inprice,
                               price=product.price,
                               supply=product.supply,
                               image=product.picture())
    else:
        form = ProductInfoForm()

    app.logger.error('start')
    app.logger.error(form.errors)
    if form.validate():
        app.logger.error('validate')

    if form.validate_on_submit():
        if product is None:
            product = Product()
        product.product_name = form.name.data
        product.category = form.category.data
        product.bar_code = form.bar_code.data
        product.size = form.size.data
        product.inprice = form.inprice.data
        product.price = form.price.data
        product.supply = form.supply.data
        try:
            filename = pics.save(request.files['image'])
            img = Image(path="pics/" + filename)
            db.session.add(img)
            db.session.commit()
            product.picture_id = img.id
        except Exception as e:
            app.logger.error(e)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('products'))
    return render_template('edit_product.html', form=form)


@app.route('/edit_supply/<supply_id>', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def edit_supply(supply_id):
    supply = Supply.query.get(supply_id)
    if supply is not None:
        form = AddSupplyForm(name=supply.name,
                             city=supply.city,
                             buyer=supply.buyer,
                             order_contact=supply.order_contact,
                             tel=supply.tel,
                             address=supply.address,
                             email=supply.email,
                             payment_mathod=supply.payment_method,
                             bank_account=supply.bank_account,
                             evidence=supply.evidence)
    else:
        form = AddSupplyForm()

    app.logger.error('start')
    app.logger.error(form.errors)
    if form.validate():
        app.logger.error('validate')

    if form.validate_on_submit():
        if supply is None:
            supply = Supply()

        supply.name = form.name.data
        supply.city = form.city.data
        supply.buyer = form.buyer.data
        supply.order_contact = form.order_contact.data
        supply.tel = form.tel.data
        supply.address = form.address.data
        supply.email = form.email.data
        supply.payment_mathod = form.payment_method.data
        supply.bank_account = form.bank_account.data
        supply.evidence = form.evidence.data
        db.session.add(supply)
        db.session.commit()
        return redirect(url_for('suppliers'))
    return render_template('edit_supply.html', form=form)


@app.route('/supply_detail/<supply_id>')
@login_required
@admin_permission.require(http_exception=403)
def supply_detail(supply_id):
    supply = Supply.query.get(supply_id)

    return render_template('supply_detail.html', supply=supply)


@app.route('/staffs')
@login_required
@admin_permission.require(http_exception=403)
def staffs():
    users = User.query.all()
    return render_template('staffs.html', users=users)


@app.route('/suppliers')
@login_required
@admin_permission.require(http_exception=403)
def suppliers():
    suppliers = Supply.query.all()
    return render_template('suppliers.html', suppliers=suppliers)


@app.route('/project_info')
@login_required
@admin_permission.require(http_exception=403)
def project_info():
    return render_template('project_info.html')


@app.errorhandler(403)
def forbidden(e):
    return render_template('page_403.html')


@lm.user_loader
def load_user(id):
    if id is None:
        return None
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
