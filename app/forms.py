from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, SelectField, SelectMultipleField, BooleanField, \
    PasswordField, FileField, validators, RadioField, widgets
from wtforms.validators import DataRequired, ValidationError, Optional, Email, EqualTo

from app.models import *


class NewUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[DataRequired()], render_kw={'rows': 6})
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CreateQuestForm(FlaskForm):
    quest_name = StringField('SideQuest Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    genre_choices = ['Stay at home', 'Transportation Necessary', 'Free', 'Paid', '21+', 'Best for couples',
                     'Best for teens', 'Best for solo', 'Best for friends', 'Best for dates', 'Best for parties',
                     'Best for introverts', 'Best for extroverts', 'Best for locals', 'Best for tourists']
    genres = SelectMultipleField('Genres', choices=genre_choices, widget=widgets.ListWidget(prefix_label=False),
                                 option_widget=widgets.CheckboxInput())

    submit = SubmitField('Create')

    def validate_genres(self, genres):
        if not genres.data:
            raise ValidationError('Choose at least one genre.')


