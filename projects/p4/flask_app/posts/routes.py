from flask import (
    render_template,
    url_for,
    redirect,
    request,
    Blueprint,
    session,
    current_app,
)
from flask_login import login_user, current_user, logout_user, login_required

from flask_app import db, bcrypt
from flask_app.models import User, Post, Comment
from flask_app.posts.forms import PostTypeForm, CreatePostForm, CommentForm


posts = Blueprint("posts", __name__)


@posts.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostTypeForm()

    if form.validate_on_submit():
        post_type = form.post_type.data
        session["post_type"] = post_type

        return redirect(url_for("posts.create_post_detail"))

    return render_template(
        "create_post_prelim.html", title="Create Post - Preliminary", form=form
    )


@posts.route("/create_post_detail", methods=["GET", "POST"])
@login_required
def create_post_detail():
    form = CreatePostForm()

    post_type = session["post_type"]
    is_video = True if post_type == "video" else False

    if form.validate_on_submit():

        if is_video:
            content = form.video_id.data
        else:
            content = form.text.data

        post = Post(
            title=form.title.data,
            is_video=is_video,
            content=content,
            author=current_user,
        )

        db.session.add(post)
        db.session.commit()

        return redirect(url_for("main.index"))

    return render_template(
        "create_post.html", title="Create Post", is_video=is_video, form=form
    )


@posts.route("/posts/<title>", methods=["GET", "POST"])
def post_detail(title):
    form = CommentForm()

    post = Post.query.filter_by(title=title).first()

    if form.validate_on_submit():
        comment = Comment(content=form.text.data, author=current_user, post=post)

        db.session.add(comment)
        db.session.commit()

        return redirect(request.path)

    comments = post.comments[::-1]

    return render_template("post_detail.html", post=post, comments=comments, form=form)
