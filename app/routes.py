import io
from PIL import Image
import random
from datetime import datetime
from urllib import parse

import requests
import os

from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory, jsonify
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

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_quest():
    form = CreateQuestForm()

    if form.validate_on_submit():
        new_image = request.files['image']

        # Use Pillow to open and process the image
        quest_image = Image.open(new_image)

        # Resize and crop the image to 250x250
        quest_image = quest_image.resize((250, 250), Image.BICUBIC)

        # Convert the image to bytes
        img_byte_array = io.BytesIO()
        quest_image.save(img_byte_array, format='PNG')
        img_byte_array = img_byte_array.getvalue()

        quest = Quest(title=form.quest_name.data, description=form.description.data, image=img_byte_array,
                      user_id=current_user.id)

        db.session.add(quest)

        for i in range(len(form.genres.data)):
            print(form.genres.data[i])
            genre_id = Genre.query.filter_by(genre=form.genres.data[i]).first()
            print(genre_id)
            quest_genre = QuestGenres(quest_id=quest.id, genre_id=genre_id.id)
            db.session.add(quest_genre)

        created_by = QuestsCreatedBy(quest_id=quest.id, user_id=current_user.id)
        db.session.add(created_by)
        db.session.commit()

        flash('Your quest has been submitted!')
        return redirect(url_for('index'))

    return render_template('createQuest.html', title='Create Quest', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    in_progress = QuestsInProgress.query.filter_by(user_id=current_user.id).all()
    completed = QuestsCompleted.query.filter_by(user_id=current_user.id).all()
    created_by = QuestsCreatedBy.query.filter_by(user_id=current_user.id).all()

    return render_template('profile.html', title='Profile Page', current_user=current_user, in_progress=in_progress, completed=completed, created_by=created_by)


#WOuld something like this work? I still keep getting the add button appearing every time, even when it shouldn't
@app.route('/check_quest_status/<int:quest_id>', methods=['GET'])
def check_quest_status(quest_id):
    quest_in_progress = QuestsInProgress.query.filter_by(quest_id=quest_id, user_id=current_user.id).first()
    return jsonify({'quest_in_progress': bool(quest_in_progress)})


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
    #user query to determine whether this quest is already in progress
    quest_in_progress = QuestsInProgress.query.filter_by(quest_id=quest_id, user_id=current_user.id).first()
    completed = QuestsCompleted.query.filter_by(user_id=current_user.id, quest_id=quest_id).first()
    return render_template('questPage.html', title='Quest Page', quest=quest, quest_in_progress=quest_in_progress, completed=completed)


@app.route('/update_quest_status/<int:quest_id>', methods=['POST', 'GET'])
def update_quest_status(quest_id):
    action = request.form.get('action')
    if action == 'add':
        new_quest = QuestsInProgress(quest_id=quest_id, user_id=current_user.id)
        db.session.add(new_quest)
    elif action == 'remove':
        quest_in_progress = QuestsInProgress.query.filter_by(quest_id=quest_id, user_id=current_user.id).first()
        db.session.delete(quest_in_progress)
    db.session.commit()

    return redirect(url_for('quest_page', quest_id=quest_id))


@app.route('/get_quest_status/<int:quest_id>', methods=['GET'])
def get_quest_status(quest_id):
    quest_in_progress = QuestsInProgress.query.filter_by(quest_id=quest_id, user_id=current_user.id).first()
    return jsonify({'quest_in_progress': bool(quest_in_progress)})


@app.route('/update_quest_status_profile/<int:quest_id>', methods=['POST'])
def update_quest_status_profile(quest_id):
    quest_in_progress = QuestsInProgress.query.filter_by(quest_id=quest_id, user_id=current_user.id).first()

    if quest_in_progress:
        db.session.delete(quest_in_progress)
        db.session.commit()

    return redirect(url_for('profile'))

@app.route('/complete_quest_status_profile/<int:quest_id>', methods=['POST'])
def complete_quest_status_profile(quest_id):
    quest_in_progress = QuestsInProgress.query.filter_by(quest_id=quest_id, user_id=current_user.id).first()

    if quest_in_progress:
        db.session.delete(quest_in_progress)
        new_quest = QuestsCompleted(quest_id=quest_id, user_id=current_user.id)
        db.session.add(new_quest)
        db.session.commit()

    return redirect(url_for('profile'))


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

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    #if form.validate_on_submit():
     #   new_image = request.files['image']
      #  image_data = new_image.read()
       # current_user.image = image_data
        #current_user.username = form.username.data
        #current_user.email = form.email.data
        #db.session.commit()
        #flash('Your changes have been saved.')
        #return redirect(url_for('profile'))
    return render_template("editAccount.html", title='Edit Profile', form=form)



@app.route('/populate_database', methods=['GET', 'POST'])
def populate_database():
    Quest.query.delete()
    QuestGenres.query.delete()
    QuestsCreatedBy.query.delete()
    QuestsInProgress.query.delete()
    QuestsCompleted.query.delete()
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
            y = random.randint(1, 150000000000000)
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
