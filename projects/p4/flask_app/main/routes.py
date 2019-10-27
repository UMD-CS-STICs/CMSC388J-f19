from flask import render_template, request, current_app, Blueprint, redirect, url_for

import json
from flask_app.models import Post, User

main = Blueprint("main", __name__)


@main.route("/")
def index():
    posts = Post.query.all()[::-1]
    return render_template("index.html", title="Home", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About")


@main.route("/user/<username>")
def user_detail(username):
    user = User.query.filter_by(username=username).first()

    return render_template(
        "user_detail.html",
        user=user,
        posts=user.posts[::-1],
        comments=user.comments[::-1],
    )


@main.route("/csp_error_handling", methods=["POST"])
def report_handler():
    """
    Receives POST requests from the browser whenever the Content-Security-Policy 
    is violated. Processes the data and logs an easy-to-read version of the message
    in your console.
    """
    report = json.loads(request.data.decode())["csp-report"]

    # current_app.logger.info(json.dumps(report, indent=2))

    violation_desc = "\nViolated directive: %s, \nBlocked: %s, \nOriginal policy: %s \n" % (
        report["violated-directive"],
        report["blocked-uri"],
        report["original-policy"]
    )

    current_app.logger.info(violation_desc)
    return redirect(url_for("main.index"))
