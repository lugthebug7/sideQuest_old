from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, SelectField, SelectMultipleField, BooleanField, \
    PasswordField, FileField
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


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CreateQuestForm(FlaskForm):
    quest_name = StringField('SideQuest Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    genre1 = BooleanField('Stay-At-Home', validators=[DataRequired()])
    genre2 = BooleanField('Transportation Necessary', validators=[DataRequired()])
    genre3 = BooleanField('Free', validators=[DataRequired()])
    genre4 = BooleanField('Paid', validators=[DataRequired()])
    genre5 = BooleanField('21+')
    genre6 = BooleanField('Good for Couples')
    genre7 = BooleanField('Good for Teens')
    genre8 = BooleanField('Good for Solo')
    genre9 = BooleanField('Good for Friends')
    genre10 = BooleanField('Good for Dates')
    genre11 = BooleanField('Good for Parties')
    genre12 = BooleanField('Good for Introverts')
    genre13 = BooleanField('Good for Extroverts')
    genre14 = BooleanField('Good for Locals')
    genre15 = BooleanField('Good for Tourists')
    submit = SubmitField('Create')

    def validate_(self):
        if not any([
            self.genre1.data, self.genre2.data, self.genre3.data,
            self.genre4.data, self.genre5.data, self.genre6.data,
            self.genre7.data, self.genre8.data, self.genre9.data,
            self.genre10.data, self.genre11.data, self.genre12.data,
            self.genre13.data, self.genre14.data, self.genre15.data
        ]):
            raise ValidationError('Pick at least one genre.')
        return False
