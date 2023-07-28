from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import Length, Email, InputRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=7)])


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=7)])
    first_name = StringField('First Name', validators=[
                             InputRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[
                            InputRequired(), Length(max=30)])
    email = StringField('Email', validators=[
                        InputRequired(), Length(max=50), Email])


class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    content = StringField('content', validators=[InputRequired()])


class DeleteForm(FlaskForm):
