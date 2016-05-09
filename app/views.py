from flask import render_template, request, flash, redirect, session, url_for, g
from flask.ext.login import login_user, logout_user, login_required, current_user
from app import app, db, lm, avators, pics
from .forms import LoginForm, UserProfileForm, ProductInfoForm, AddUserForm
from .models import User, Image, Customer, Product, TradeRecord


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    data = [
        [0, 40],
        [1, 9],
        [2, 6],
        [3, 10],
        [4, 5],
        [5, 17],
        [6, 6],
        [7, 10],
        [8, 7],
        [9, 11],
        [10, 35],
        [11, 9],
        [12, 12],
        [13, 5],
        [14, 3],
        [15, 4],
        [16, 9]
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           data=data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User ' + username + ' not found.')
        return redirect(url_for('index'))
    return render_template('user.html', user=user)

@app.route('/product_info/<product_id>')
@login_required
def product_info(product_id):
    product = Product.query.get(product_id)
    if product_id is None:
        flash('Product ' + product_id + 'not found.')
        return redirect(url_for('index'))
    return render_template('product_info.html', product=product)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
    return render_template("add_user.html", form = form)

@app.route('/edit_profile/<uid>', methods=['GET', 'POST'])
@login_required
def edit_user_profile(uid):
    form = UserProfileForm()
    user = User.query.get(uid)
    if user is None:
        user = User()
    if form.validate_on_submit():
        filename = avators.save(request.files['avator'])
        img = Image(path="avatars/" + filename)
        db.session.add(img)
        db.session.commit()
        user.avator_id = img.id
        db.session.add(user)
        db.session.commit()
        # g.user.store()
        flash('photo saved')
        return redirect(url_for('index'))
    return render_template('edit-user-profile.html', form=form)


@app.route('/trade')
@login_required
def trade():
    trades = TradeRecord.query.all()
    return render_template('trade.html', trades = trades, Product = Product)


@app.route('/customers')
@login_required
def customers():
    customer = Customer.query.get(1)
    return render_template('customers.html', cst=customer)


@app.route('/products')
@login_required
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)


@app.route('/edit_product/<product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get(product_id)
    if product is not None:
        form = ProductInfoForm(name=product.product_name,
                               barcode=product.bar_code,
                               price=product.price,
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
        product.price = form.price.data
        product.bar_code = form.barcode.data
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


@app.route('/staffs')
@login_required
def staffs():
    users = User.query.all()
    return render_template('staffs.html', users = users)


@app.route('/suppliers')
@login_required
def suppliers():
    return render_template('suppliers.html')


@app.route('/project_info')
@login_required
def project_info():
    return render_template('project_info.html')


@lm.user_loader
def load_user(id):
    if id is None:
        return None
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
