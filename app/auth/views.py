from flask import render_template,request, redirect, url_for, flash, abort
from . import auth
from .forms import SignupForm, LoginForm
from ..models import User
from .. import db
from ..email import mail_message
from flask_login import login_user, logout_user, login_required, current_user

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        
        mail_message('Hello from The J Blog', 'email/email', user.email, user=user)
        
        return redirect(url_for('auth.login'))
        
    title = "New Account"
    return render_template('auth/signup.html', signupform=form, title=title)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    title="Login"
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.rememberMe.data)
            return redirect(url_for('main.index'))
       
        flash('Invalid username or password')
        
    return render_template('auth/login.html', loginform=form, title=title)

# def subscribed():
#     form =


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     title="Login"
#     form = LoginForm()
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             user = User.query.filter_by(username=form.username.data).first()
#             if user:
#                 if bcrypt.check_password_hash(user.password, form.password.data):
#                     login_user(user)
#                 # is not None and user.verify_password(form.password.data):
#                     return redirect(url_for('main.index'))
#                 # return redirect(request.args.get('next') or url_for('main.index'))
#             else:
#                 flash('Invalid username or password')
        
#     return render_template('auth/login.html', loginform=form, title=title)