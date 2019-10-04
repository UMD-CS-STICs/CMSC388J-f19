from flask_app.models import User

# External
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired, Length, ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up!')

    # We put our uniqueness checks here, because its easier to check here rather than
    # catching the exception the database would raise later on
    def validate_user(self, name):
        if len(User.query.filter_by(username=name.data).all()) > 0:
            raise ValidationError('The username you entered is taken, please try another one.')
    def validate_email(self, email):
        if len(User.query.filter_by(email=email.data).all()) > 0:
            raise ValidationError('The email you entered is taken, please try another one.') 
