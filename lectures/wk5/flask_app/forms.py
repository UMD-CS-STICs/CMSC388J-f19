from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length

class WelcomeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=30)])
    location = StringField('Location', validators=[DataRequired(), Length(min=3, max=50)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=1, max=140, message='Must be between 1 and 140')])