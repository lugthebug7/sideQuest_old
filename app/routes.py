import io
import random
from datetime import datetime
from urllib import parse

import requests
import os

from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory
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
    if form.validate_on_submit():
        new_image = request.files['image']
        image_data = new_image.read()
        user = User(username=form.username.data, email=form.email.data, image=image_data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user)
        return redirect(url_for('index'))
    return render_template('createAccount.html', title='Register', form=form)


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('testProfile.html', title='Profile Page', user=user)
    #return render_template('profile.html', title='Profile Page', current_user=user)

#@app.route('/user/<username>', methods=['GET', 'POST'])
#@login_required
#def user(username):
    #user = User.query.filter_by(username=username).first_or_404()
    #posts = [
        #{'author': user, 'body': 'Test post #1'}
    #]
    #return render_template('testProfile.html', user=user, posts=posts)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_quest():
    form = CreateQuestForm()
    if form.validate_on_submit():
        new_image = request.files['image']
        image_data = new_image.read()
        quest = Quest(title=form.quest_name.data, description=form.description.data, image=image_data,
                      user_id=current_user.id)
        db.session.add(quest)
        for i in range(len(form.genres.data)):
            print(form.genres.data[i])
            genre_id = Genre.query.filter_by(genre=form.genres.data[i]).first()
            print(genre_id)
            quest_genre = QuestGenres(quest_id=quest.id, genre_id=genre_id.id)
            db.session.add(quest_genre)
        db.session.commit()
        flash('Your quest has been submitted!')
        return redirect(url_for('index'))
    return render_template('createQuest.html', title='Create Quest', form=form)

@app.route('/quests', methods=['GET', 'POST'])
@login_required
def all_quests():
    # We will later do filtered queries to get quests based on genre, etc.
    filler = Quest.query.filter_by(id=1).first()

    genre1 = db.session.query(Quest, Genre.genre). \
        join(QuestGenres, Quest.id == QuestGenres.quest_id). \
        join(Genre, Genre.id == QuestGenres.genre_id). \
        filter(QuestGenres.genre_id == 1). \
        all()

    genre2 = db.session.query(Quest, Genre.genre). \
        join(QuestGenres, Quest.id == QuestGenres.quest_id). \
        join(Genre, Genre.id == QuestGenres.genre_id). \
        filter(QuestGenres.genre_id == 2). \
        all()

    genre3 = db.session.query(Quest, Genre.genre). \
        join(QuestGenres, Quest.id == QuestGenres.quest_id). \
        join(Genre, Genre.id == QuestGenres.genre_id). \
        filter(QuestGenres.genre_id == 3). \
        all()

    genre4 = db.session.query(Quest, Genre.genre). \
        join(QuestGenres, Quest.id == QuestGenres.quest_id). \
        join(Genre, Genre.id == QuestGenres.genre_id). \
        filter(QuestGenres.genre_id == 4). \
        all()

    genre5 = db.session.query(Quest, Genre.genre). \
        join(QuestGenres, Quest.id == QuestGenres.quest_id). \
        join(Genre, Genre.id == QuestGenres.genre_id). \
        filter(QuestGenres.genre_id == 5). \
        all()

    genre6 = db.session.query(Quest, Genre.genre). \
        join(QuestGenres, Quest.id == QuestGenres.quest_id). \
        join(Genre, Genre.id == QuestGenres.genre_id). \
        filter(QuestGenres.genre_id == 6). \
        all()

    genre7 = db.session.query(Quest, Genre.genre). \
        join(QuestGenres, Quest.id == QuestGenres.quest_id). \
        join(Genre, Genre.id == QuestGenres.genre_id). \
        filter(QuestGenres.genre_id == 7). \
        all()

    genre8 = db.session.query(Quest, Genre.genre). \
        join(QuestGenres, Quest.id == QuestGenres.quest_id). \
        join(Genre, Genre.id == QuestGenres.genre_id). \
        filter(QuestGenres.genre_id == 8). \
        all()

    genre9 = db.session.query(Quest, Genre.genre). \
        join(QuestGenres, Quest.id == QuestGenres.quest_id). \
        join(Genre, Genre.id == QuestGenres.genre_id). \
        filter(QuestGenres.genre_id == 9). \
        all()

    genre10 = db.session.query(Quest, Genre.genre). \
        join(QuestGenres, Quest.id == QuestGenres.quest_id). \
        join(Genre, Genre.id == QuestGenres.genre_id). \
        filter(QuestGenres.genre_id == 10). \
        all()

    genre11 = db.session.query(Quest, Genre.genre). \
        join(QuestGenres, Quest.id == QuestGenres.quest_id). \
        join(Genre, Genre.id == QuestGenres.genre_id). \
        filter(QuestGenres.genre_id == 11). \
        all()

    genre12 = db.session.query(Quest, Genre.genre). \
        join(QuestGenres, Quest.id == QuestGenres.quest_id). \
        join(Genre, Genre.id == QuestGenres.genre_id). \
        filter(QuestGenres.genre_id == 12). \
        all()

    genre13 = db.session.query(Quest, Genre.genre). \
        join(QuestGenres, Quest.id == QuestGenres.quest_id). \
        join(Genre, Genre.id == QuestGenres.genre_id). \
        filter(QuestGenres.genre_id == 13). \
        all()

    genre14 = db.session.query(Quest, Genre.genre). \
        join(QuestGenres, Quest.id == QuestGenres.quest_id). \
        join(Genre, Genre.id == QuestGenres.genre_id). \
        filter(QuestGenres.genre_id == 14). \
        all()

    genre15 = db.session.query(Quest, Genre.genre). \
        join(QuestGenres, Quest.id == QuestGenres.quest_id). \
        join(Genre, Genre.id == QuestGenres.genre_id). \
        filter(QuestGenres.genre_id == 15). \
        all()

    return render_template('quests.html', title='All Quests', genre1=genre1, genre2=genre2,
                           genre3=genre3, genre4=genre4, genre5=genre5, genre6=genre6, genre7=genre7, genre8=genre8,
                           genre9=genre9, genre10=genre10, genre11=genre11, genre12=genre12, genre13=genre13,
                           genre14=genre14, genre15=genre15, filler=filler)


@app.route('/quest_page/<quest_id>', methods=['GET', 'POST'])
@login_required
def quest_page(quest_id):
    quest = Quest.query.filter_by(id=quest_id).first()

    # query = (
    #   db.session.query(Quest.name.label('quest_name'), Quest.description.label('quest_description'), Quest.image.label('quest_image'), QuestGenres.genre.label('quest_genre'))
    #  .join(QuestGenres, Quest.id == QuestGenres.quest_id)
    # .filter(Quest.id == quest_id)
    # )
    # results = query.all()
    return render_template('questPage.html', title='Quest Page', quest=quest)


@app.route('/image/<int:quest_id>')
def image(quest_id):
    quest = Quest.query.get(quest_id)

    if quest and quest.image:
        return send_file(io.BytesIO(quest.image), mimetype='image/jpeg')
    else:
        flash('Image not found')
        return redirect(url_for('index'))

@app.route('/userimage/<int:user_id>')
def profile_pic(user_id):
    user = User.query.get(user_id)

    if user and user.image:
        return send_file(io.BytesIO(user.image), mimetype='image/jpeg')
    else:
        flash('Image not found')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/populate_database', methods=['GET', 'POST'])
def populate_database():
    Quest.query.delete()
    QuestGenres.query.delete()
    db.session.commit()
    y = random.randint(1, 1500000000000000000000000000000)
    name = 'Coming Soon ' + str(y)

    # Assuming the image file is in the 'static' folder
    image_path = "app/static/MORE-COMING-SOON.png"

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    new_quest = Quest(title=name, description="More Quests Coming Soon!", image=image_data)
    db.session.add(new_quest)
    db.session.commit()

    for i in range(1, 96):
        image_url = f'https://picsum.photos/250/250/?random={i}'
        response = requests.get(image_url)
        if response.status_code == 200:
            y = random.randint(1, 1500000000000000000000000000000)
            name = 'Quest' + str(y)
            description = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt "
                           "ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation "
                           "ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in "
                           "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur "
                           "sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id "
                           "est laborum.")
            new_image = response.content
            new_quest = Quest(title=name, description=description, image=new_image)
            db.session.add(new_quest)
            db.session.commit()
            x = random.randint(1, 15)
            quest_genre = QuestGenres(quest_id=new_quest.id, genre_id=x)
            db.session.add(quest_genre)
            x = random.randint(1, 15)
            quest_genre = QuestGenres(quest_id=new_quest.id, genre_id=x)
            db.session.add(quest_genre)
            db.session.commit()
    return render_template('index.html', title='Home')
