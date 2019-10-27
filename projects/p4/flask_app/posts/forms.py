from flask import session
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    RadioField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from flask_app.models import User


class PostTypeForm(FlaskForm):
    post_type = RadioField(
        "What type of post do you want to create?",
        validators=[DataRequired()],
        choices=[("video", "YouTube Video Link"), ("text", "Text Post")],
    )

    submit = SubmitField("Head to Post Creation page!")


class CreatePostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=5, max=100)])

    text = TextAreaField("Text")
    video_id = StringField("YouTube Video ID")

    submit = SubmitField("Submit Post!")

    def validate_video_id(self, video_id):
        if session["post_type"] == "video":
            if len(video_id.data.strip()) != 11:
                raise ValidationError("The YouTube video ID must be 11 characters long")


class CommentForm(FlaskForm):
    text = TextAreaField("Comment:", validators=[Length(min=1)])

    submit = SubmitField("Submit Comment")
