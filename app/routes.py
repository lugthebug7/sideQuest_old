from datetime import datetime
from urllib import parse

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from sqlalchemy.orm import aliased

from werkzeug.urls import url_parse


from app import app
from app.forms import *
from app.models import *




@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = NewUserForm()
    print(1)
    if form.validate_on_submit():
        print(2)
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user)
        return redirect(url_for('index'))
    return render_template('createAccount.html', title='Register', form=form)





#@app.route('/quest_page/<quest_id>', methods=['GET', 'POST'])
#@login_required
#def quest_page(quest_id):



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


