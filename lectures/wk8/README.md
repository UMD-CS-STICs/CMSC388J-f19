# Week 8
### Blueprints

The code for this week is the same as the code presented in the `wk6` notes,
and we'll replicate the description here for convenience.

This week we'll look at an app where a user can register/login to our website 
and see all of the posts they've created, as well as look at other user's posts.
We haven't added any functionality to create posts, as we just wanted to focus
on how to create blueprints. 

To run the code, make sure to run
`pip install Flask flask-sqlalchemy flask-wtf flask-login flask-bcrypt flask-talisman`.

The database we provide already has some users and posts in there. The users are:

| Username        | Email           | Password  |
| ------------- |:-------------:| -----:|
| harrypotter      | harry@hogw.edu | VoldemortSucks |
| gvanrossum     | guido@python.org     |   ilovepython3.8.0 |

The starter code in this directory works, and allows you to log-in as either of the users
above. It also allows you to create new accounts, but not create new posts. The `My Account`
page shows you all of the posts you created, but will redirect to the `Login` page if
no one is signed in.

The main point of *Blueprints* is to help you modularize your applications. Most of the
functionality we need to use blueprints is provided by the `Blueprint` class, which 
we can access using `from flask import Blueprint`.

A `Blueprint` object is similar to a `Flask` object, except you cannot create a stand-alone
application with only a `Blueprint`. `Blueprints` are used to extend and organize your application.
When would we use blueprints? Here are some common use cases:

- Break down an application into several blueprints, registering each with the main `Flask`
  application object.
- Register a blueprint at a certain URL prefix. For example, make a blueprint where all view
  functions automatically have `users/` at the beginning.
- Provide other functionality, not necessarily view functions.

A blueprint, internally, just keeps track of a sequence of operations to execute once it
is registered to an application, and `Flask` will use the registered blueprints to
build URLs and process requests.

The `flask_app` currently has `__init__.py` for setting up our application and all of the necessary
extensions, `forms.py` for our website's forms, `models.py` for our SQLAlchemy models, `routes.py` 
for all of the view functions we have in our application, `templates/` containing all of the
HTML templates we'll be using in our application, and `site.db` which contains some
sample posts and users (listed above):



The `LoginManager` class was explained in the lecture notes for `wk6`, and `flask_talisman`
was explained in the notes for `wk7`. To recap:

- `flask_login` automatically manages user sessions and allows us to restrict parts of our website 
  only to signed-in users.
- `flask_talisman` sets several HTTP headers to help protect against common security issues.

Blueprints cannot be registered with another blueprint, they can only be registered to a
`Flask` object. We can keep our `app` variable creation the same in `__init__.py`, but we'll
get rid of the last line here, the one that sets up all the routes:

`__init__.py`:
```py
""" Omitted setup code """
from flask_app import models
db.create_all()

# Commented out line below
# from flask_app import routes
```

At this point, if we run the application, we get a `404` error on any page we try to
access, as expected. Now it's time to break up `routes.py`.

First, we'll create two new python packages in our `flask_app/` directory. We'll
call the first one something like `users` because it will contain all of the functionality
for creating, manging, and accessing user data. We'll call the second package `main`, and
it will contain functionality for showing our front page and an about page for our website.

Remember that to create a python package, you have to create a folder and then
add an `__init__.py` file inside the folder. It doesn't have to have anything inside (it
can be a completely empty file), but adding it indicates that we have a python package.

We'll make a `routes.py` in each of these packages, too. In each of the `routes.py`, we can
include all of the imports we need from the original `routes.py`, and then include
`from flask import Blueprint`. For example, in our `users/routes.py`, the first
line would become:

`from flask import render_template, url_for, redirect, request, Blueprint`.

And then, in each file, we createt the blueprint using the `Blueprint` class. Here
is the starter code for each of the `routes.py` files:

`users/routes.py`:
```py
from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from flask_app import db, bcrypt
from flask_app.models import User, Post
from flask_app.users.forms import RegistrationForm, LoginForm, UpdateForm

users = Blueprint('users', __name__)
```

`main/routes.py`:
```py
from flask import render_template, Blueprint

from flask_app.models import Post

main = Blueprint('main', __name__)
```

We can remove all the imports from `flask_login` because our view functions in `main`
will not use any of those. Since we're modularizing our application, the user management
stuff will go into another blueprint.

Notice how we aren't importing `app` from `flask_app` anymore; we are instead creating a 
`Blueprint` object, which we'll then import in our `flask_app/__init__.py` file
to register with our `app` object. More on that later.

The `Blueprint` object is created using two arguments here. The first specifies
the name of our `Blueprint`, which will be `'main'`. The second argument
specifies the name of the blueprint's package, and we pass in `__name__`. Note
that this is the same argument we passed into the `Flask` class when creating
a new application object.

The directories located in `flask_app/`:

users
├── __init__.py
└── routes.py

main
├── __init__.py
└── routes.py

Next, we'll move each of the view functions into the appropriate `routes.py` file.
We'll decide where to put each view function based on its functionality: 1) does it
only retrieve and show pages, or 2) does it also manage user sessions or manipulate
the database?

Going function by function:

- `register()` uses a `RegistrationForm` to create new users, input them into the database,
  and then redirect to the login page. This should go in **users**
- `login()` uses a `LoginForm` to login a user, then redirects to the account page. This
  should go into **users**.
- `logout()` simply logs the user out, manipulating the user session, so it will go in **users**
- `account()` allows a logged-in user to changed their username. We added a decorator on top:
  `@login_required`, so we'll say this view function goes into **users** because it depends on
  `flask_login` to work.
- `user_detail()` only accesses values from a database with `User` and then shows an HTML page,
  so we put it into **main**.
- `index()` retrieves values from the `Post` table of our database and shows an HTML page,
  so we put it into **main**.
- `about()` returns an HTML page, so we put it into **main**.

Now, after moving the appropriate functions around, we can delete `routes.py`
and all of our functions should be in `users/routes.py` and `main/routes.py`. 
A quick directory overview:

flask_app
├── __init__.py
├── forms.py 
├── main
│   ├── __init__.py
│   └── routes.py
├── models.py
├── site.db
├── templates - *not expanded*
└── users
    ├── __init__.py
    └── routes.py

At this point, `users/routes.py` should look like:
```py
""" Omitted imports """

users = Blueprint('users', __name__)

@app.route("/register", methods=['GET', 'POST'])
def register():
    """ Omitted code """

@app.route("/login", methods=['GET', 'POST'])
def login():
    """ Omitted code """

@app.route("/logout")
def logout():
    """ Omitted code """

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """ Omitted code """
```

And similarly for `main/routes.py`, but with the functions designated to be
part of the `main` blueprint above.

At this point, if you were to run the flask application, it wouldn't work, 
because we removed the `from flask_app import app` import. We still don't
want to add it. Instead, starting off in `users/routes.py`, we can
change our code: wherever it says `@app`, we change it to `@users`, the name of
our `Blueprint` object.

We should've changed four functions to accomplish this, and here is
our `users/routes.py` now:

```py
""" Omitted imports """

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    """ Omitted code """

@users.route("/login", methods=['GET', 'POST'])
def login():
    """ Omitted code """

@users.route("/logout")
def logout():
    """ Omitted code """

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """ Omitted code """
```

And we do the renaming operation similarly in `main/routes.py`: change wherever
the code has `@app` to `@main`.

Notice that `forms.py` has forms only for registering, logging-in, and changing
names for users, so all of these forms can be placed into our `users/` package.
While this isn't necessary for the app to work, we are learning how to
modularize our application so we'll move it into `users/`. Because we do this,
we'll have to change an import line near the top of `users/routes.py`:

```py
""" Omitted imports """

from flask_app.users.forms import RegistrationForm, LoginForm, UpdateForm

""" Omitted code """
```

This changes the path to access `forms.py` to reflect the file movement
we just did. 

There's one final change we have to make. We created the blueprints, registered
our view functions with the blueprints, and made sure all of the imports needed exist
in either file. In `__init__.py`, we'll have to import both of the blueprints
and register them with our `app` object. 

`__init__.py`:
```py
""" Omitted setup and extensions code """

from flask_app import models

db.create_all()

from flask_app.main.routes import main
from flask_app.users.routes import users

app.register_blueprint(main)
app.register_blueprint(users)
```

We imported the `Blueprint` object from each of the `routes.py` files,
and we call the `register_blueprint()` function of our `app` object. 
Only instances of the `Flask` class have `register_blueprint()`. The `Blueprint`
class does not have the ability to register new blueprints.

At this point, we have successfully modularized our application with Blueprints.
These concepts can be extended indefinitely with new blueprints. Your app
can also contain multiple packages of blueprints, holding view functions
or templates or static files. 

**Extra stuff**:

One useful functionality of blueprints (that you won't have to know for this class)
is we can specify the `url_prefix=` keyword argument for `register_blueprint()`.
If we changed the last line to be `app.register_blueprint(users, url_prefix='/users')`,
then all of the view functions in the `users` blueprint would have `/users` prepended.

We can check what all of our endpoints are easily by importing our `app` object
in the command line and calling the `url_map` attribute:

```py
>>> from flask_app import app
>>> 
>>> app.url_map
Map([<Rule '/users/register' (POST, GET, HEAD, OPTIONS) -> users.register>,
 <Rule '/users/account' (POST, GET, HEAD, OPTIONS) -> users.account>,
 <Rule '/users/logout' (GET, HEAD, OPTIONS) -> users.logout>,
 <Rule '/users/login' (POST, GET, HEAD, OPTIONS) -> users.login>,
 <Rule '/about' (GET, HEAD, OPTIONS) -> main.about>,
 <Rule '/' (GET, HEAD, OPTIONS) -> main.index>,
 <Rule '/static/<filename>' (GET, HEAD, OPTIONS) -> static>,
 <Rule '/user/<username>' (GET, HEAD, OPTIONS) -> main.user_detail>])
```

Here we see a map with all of the endpoint rules. Each of the URL endpoints
has certain HTTP verbs associated with them, and the rules also tell us
which function provided us with the appropriate rule. The `/static/<filename>`
endpoint is something you haven't seen before; it is an endpoint `Flask` creates
in order to find static files, we don't have to worry about it.
