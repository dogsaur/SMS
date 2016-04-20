from flask import render_template, request, flash, redirect, session, url_for, g
from flask.ext.login import login_user, logout_user, login_required, current_user
from app import app, db, lm, avators
from .forms import LoginForm, UserProfileForm
from .models import User, Image, Customer, Product



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
        if user.password == form.password.data:
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_user_profile():
    form = UserProfileForm()
    if form.validate_on_submit():
        filename = avators.save(request.files['avator'])
        img = Image(path=filename)
        db.session.add(img)
        db.session.commit()
        g.user.avator_id = img.id
        db.session.add(g.user)
        db.session.commit()
        # g.user.store()
        flash('photo saved')
        return redirect(url_for('index'))
    return render_template('edit-user-profile.html', form=form)


@app.route('/trade')
@login_required
def trade():
    return render_template('trade.html')


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


@app.route('/staffs')
@login_required
def staffs():
    return render_template('staffs.html')


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
