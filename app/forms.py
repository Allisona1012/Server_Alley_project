from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class RegistrationForm (FlaskForm):
    username= StringField('Username', validators=[DataRequired()])
    email= StringField('Email',validators=[DataRequired(),Email()] )
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password= PasswordField('Password',validators=[DataRequired()])
    submit= SubmitField('Login')

class PostForm(FlaskForm):
    title=StringField('Title', validators=[DataRequired()])
    body=StringField('Body', validators=[DataRequired()])
    submit=SubmitField('Post')

class CommentForm(FlaskForm):
    text = StringField('Comment', validators=[DataRequired()])
    submit= SubmitField('Post')