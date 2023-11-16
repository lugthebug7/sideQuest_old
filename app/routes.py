import io
from datetime import datetime
from urllib import parse

from flask import render_template, redirect, url_for, flash, request, send_file
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


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_quest():
    form = CreateQuestForm()
    print(1)
    if form.validate_on_submit():
        print(2)
        new_image = request.files['image']
        #new_image = form.image.data
        image_data = new_image.read()
        quest = Quest(title=form.quest_name.data, description=form.description.data, image=image_data, user_id=current_user.id)
        db.session.add(quest)
        db.session.commit()
        flash('Your quest has been submitted!')
        return redirect(url_for('index'))
    return render_template('createQuest.html', title='Create Quest', form=form)


@app.route('/quests', methods=['GET', 'POST'])
@login_required
def all_quests():
    #We will later do filtered queries to get quests based on genre, etc.
    quests = Quest.query.all()
    return render_template('quests.html', title='All Quests', quests=quests)


@app.route('/quest_page/<quest_id>', methods=['GET', 'POST'])
@login_required
def quest_page(quest_id):
    quest = Quest.query.filter_by(id=quest_id).first()
    image = send_file(io.BytesIO(quest.image), mimetype='image/jpeg')

    #query = (
     #   db.session.query(Quest.name.label('quest_name'), Quest.description.label('quest_description'), Quest.image.label('quest_image'), QuestGenres.genre.label('quest_genre'))
      #  .join(QuestGenres, Quest.id == QuestGenres.quest_id)
       # .filter(Quest.id == quest_id)
    #)
    #results = query.all()
    return render_template('questPage.html', title='Quest Page', quest=quest)




@app.route('/image/<int:quest_id>')
def image(quest_id):
    quest = Quest.query.get(quest_id)

    if quest and quest.image:
        return send_file(io.BytesIO(quest.image), mimetype='image/jpeg')
    else:
        flash('Image not found')
        return redirect(url_for('index'))



#@app.route('/quest_page/<quest_id>', methods=['GET', 'POST'])
#@login_required
#def quest_page(quest_id):



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


