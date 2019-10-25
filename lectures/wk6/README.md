# Week 6
### User Management

The slides for this week are linked on Piazza. 

This week we'll look at an app where a user can register/login to our website 
and see all of the posts they've created, as well as look at other user's posts.
We haven't added any functionality to create posts.

The database we provide already has some users and posts in there. The users are:

| Username        | Email           | Password  |
| ------------- |:-------------:| -----:|
| harrypotter      | harry@hogw.edu | VoldemortSucks |
| gvanrossum     | guido@python.org     |   ilovepython3.8.0 |

To run all of the code, make sure to 
`pip install Flask flask-sqlalchemy flask-wtf flask-login flask-bcrypt`

The code in this directory is complete, and allows you to log-in as either of the users
above. It also allows you to create new accounts, but not create new posts. The `My Account`
page shows you all of the posts you created, but will redirect to the `Login` page if
no one is signed in.

We'll go over how we added each component of the login and registration system.

Optionally, `pip install python-dotenv` to automatically set environment
variables in Python.

#### Securing Passwords

When someone visits your site and registers for a new account (perhaps your site
is a e-commerce or bookmarking or image hosting website), they enter a username and password, 
and possibly other information. The **password** gives an attacker the most power over
a certain user; they can get all of the information they want on the user (since they
can authenticate as the user), and they can change your activity on the website. Perhaps
they delete some memorable albums, or start ordering random items off a e-commerce
website, or even elect to deactivate/delete your account.

Therefore, we'll be hashing our passwords. Hashing is a one-way function, and if the
resulting hash is long, then it will be computationally infeasible to find a collision.
For example, no collisions have been found for SHA256.

We'll be using `flask-bcrypt` for this.

To see a simple example of how `flask-bcrypt` works, we'll go into the REPL. There is a
`Bcrypt` class available to use from flask_bcrypt, and we use an instance of this class to
generate password hashes and then check a given password against a hash.

```python
>>> from flask_bcrypt import Bcrypt
>>> bcrypt = Bcrypt()
>>> bcrypt.generate_password_hash('a_password')
b'$2b$12$nz0fVuySYJBzJ.sXocYsuuHfUw5weyLCzOEJHjjLwvf1u/hChnam2'
```

We see that we get a byte string returned to us, so if we want to turn it into a normal
string, we can use the `decode()` function of the `bytes` object. The byte string is
encoded in `UTF-8`, and that is the default decoding.

```python
>>> bcrypt.generate_password_hash('a_password')
b'$2b$12$nz0fVuySYJBzJ.sXocYsuuHfUw5weyLCzOEJHjjLwvf1u/hChnam2'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$TPu20eIGwAl050BcZfd60uFDNpiiob3CYr9lKSuAPCJ0k/MuXML1e'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$Q0c.ZCab7QqPjQ3znxXqK.1xtuUYUhhMhy0GYj8I1r14823D/ZupK'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$HfAZT2hsoY4frIl2R6qDn.HAs6A2VUyplkQs6O9D3ont2t9dS9bEe'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$eIQ8MELmSkZW5kmF1MG/5uz8ufit6KrFXwRGStIM1FkUUxVbFIbMO'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$vGWOxXd/Ee00ubeglwxy7eSY7ryMyGm/1k9MDejvixYkixcChLqe2'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$9AnFKXs66A86ZQUknV4/m.w7zCZB3rLpfZgT7vJnLAQ7D/sl12wHa'
```

Notice how we generate a different hash everytime, even though we're hashing the same
password. This prevents attackers from just going through all combinations of passwords
to find a matching hash. Since `Bcrypt` is a slow hash, parsing through all these combinations
is much slower than for SHA256.

Also look at the first 7 characters in every hash string. The `2b` determines which 
version of `bcrypt` was used, the `12` indicates that `2^12` iterations of the
key derivation function were used (the recommended amount). The next 22 characters
are the 'salt' for this hash. 

A salt is a random string that is combined with the input, the user's password, a
that used as input, along with the password, to the
hashing function. The salt increases the security of all passwords, and especially
that of common passwords.

So how would we check that our password hash is equivalent to the hash of a password the
user enters? There is another function called `check_password_hash`, which takes
a parameter of the hash and of the potential password, and it checks for us.


```python
>>> pass_hash = bcrypt.generate_password_hash('a_password')
>>> pass_hash
b'$2b$12$exCUucO2pcFhvahPR/mDNeM7CJhuoj7cMJ4s1CxHZdzHApsQqbwYq'
>>> bcrypt.check_password_hash(pass_hash, 'a_password')
True
>>> bcrypt.check_password_hash(hash, 'another_password')
False
```

So we can get started using it in our application by adding it to `__init__.py`:

`__init__.py`:
```python
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xa4\x0c\x9c3B\xa8a\xc4\x19<z\x00\xc2\xc9\xcd\x14'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

from flask_app import routes
```

#### Flask-Login

Flask-Login provides user session management in our Flask apps. We can use its functions
to login and logout users, access the current user, and restrict access to pages
on our website which require authentication. 

It also allows you to add the 'Remember Me' functionality to your website, 
to allow a user to still be logged in if they closed their browser. How it does this
is by storing a cookie in the browser with the user's ID. We won't go over
how to implement this functionality in this class.

When setting up your app, there's a setting we have to specify for `flask_login`,
the `login_view` attribute of a `LoginManager()` object. First, we import the
`LoginManager` class from `flask_login`, and then initialize it and set the attribute.

`__init__.py`:
```py
""" Omitted imports """
from flask_login import LoginManager

""" Omitted setup code """

login_manager = LoginManager(app)
login_manager.login_view = 'login'
```

We create the `login_manager` object similarly to how we worked with the other
`flask` extensions; we pass in our `app` object to `LoginManager()`. Next, we
set `login_manager.login_view = 'login'`. This means that the login page
for our website will be accessed by going to the view function named `'login'`.
When an unauthenticated user tries to access some restricted page on our website,
they are sent to the `'login'` page.

You can rename `login_manager.login_view` to whatever view function that you want,
but the user will be redirected to that view by `flask_login` if authentication
is required to access a page.

Now, if we want to have a login page, then we must have a login form on that
page so that the user can input their data and we can validate it. 
For our website, we'll let the user just login with their unique username
and password. Here's what that form might look like:

`forms.py`:
```py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
""" Omitted forms """
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('That username does not exist in our database.')
```

Notice the new `SubmitField` we're using. We meant to show that in a previous lecture,
when first discussing `WTForms`, but it slipped our mind then. 

Otherwise, we also have a `validate_` function. Every function we create in our form
that starts with `validate_` and ends with the name of the variable we are validating
will be called when we call `form.validate_on_submit()` or `form.validate()`. Notice
that we also raise a `ValidationError`. This does not crash our website; it is 
recorded, literally, as a validation error. This is how we can define custom
validators. 

The `validate_username()` function checks if there exists a user with the
username entered in the form. If no such user exists, then the query returns `None`,
at which point we raise a custom error message. Recall the user table at the top
of the page, and let's try logging in as a user that does not exist in the database.
Here's the result:

![Login failure][login_fail]

You can only create a custom validator for one field at a time, and we'll see
how this is implemented later with a `RegistrationForm`.

How did we get the error message to show up? Each field of a form has a list of errors
that might have been encountered during validation, so given the `username`
field in the above `LoginForm`, we can list the validation errors using the code below.
We will show the errors directly below the rendered field.

`login.html`:
```html
<!-- Omitted HTML -->
{{ form.username }}
{% if form.username.errors %}
<div>
    {% for error in form.username.errors %}
        <span>{{ error }}</span>
    {% endfor %}
</div>
<!-- Omitted HTML -->
```

In Python, when we do `if li: pass`, where `li` is a list, the `__len__()` function of a
`list` object gets called. If a list is empty, then `__len__()` returns 0 and the `if` statement
does not execute its branch of code. 

So in this snippet, if our `errors` list is non-empty, then we go through the list
of errors and print them to the screen, as you can see in the image above.
This is available to every field, so you can add the error-printing snippet
below every field. It isn't really necessary for the `SubmitField`, though.

Before we get to implementing `login()`, we have to modify our `models.py` slightly.
`flask_login` provides us with a global variable called `current_user`. We can
check if the `current_user` is authenticated, active, anonymous, or get their id. 
However, to do this, our User class needs to have the properties:
- `is_authenticated`
- `is_active`
- `is_anonymous`
implemented, along with a `get_id()` function. We can use a shortcut and make the
class that represents our user a subclass of `UserMixin`. `UserMixin` is provided
from `flask_login`, and it implements the above properties and method.
In our case, the User model represents the user, so we can just indicate that the model
is also a subclass of `UserMixin` by changing (in `models.py`)

```py
""" Omitted imports """

class User(db.Model):
    """ Omitted code """
```

to this:

```py
""" Omitted imports """
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """ Omitted code """
```

If you choose not to subclass from `UserMixin` in future applications, you would need to
implement the above properties and function on your class.

Finally, `flask_login` needs to know how to load the user to set the `current_user`
global variable. To give `flask_login` this power, we have to implement a function
that returns a user, and decorate it with `login_manager.user_loader`.

`flask_login` keeps track of the `id` for a user, which should be a unique value. 
We'll import our `login_manager` and use it to create our user-loading function like so:

`models.py`:
```py
from flask_app import login_manager
""" Omitted imports """

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

""" Omitted models """
```

Now `flask_login` calls this function to get a User, and `current_user`
will have access to all of the `Column`s in the model.

Now to implement `login()`, I'll list all of the code first and then explain how it works.

`routes.py`:
```py
from flask_login import login_user, current_user
from flask_app.forms import LoginForm
from flask_app.models import User
""" Omitted imports """

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('account'))

    return render_template('login.html', title='Login', form=form)
```

The methods for `login()` are `GET` and `POST` because the form will send a `POST` request
to this function when submitted. The first `if` statement we have checks if
the `current_user` is authenticated, i.e. if  there is a user ID stored in the session.
If so, then we simply redirect to the front page so that logged-in users don't see
the login page.

Next, we create the form. If the form can be validated once it is submitted, we retrieve
the user in the database which has the same username as the one input in the form. 
We check if `user is not None`, which *isn't necessary* since we already have the
`validate_username()` function in `LoginForm`, but we'll be explicit for clarity.

We check the password hash using the `bcrypt.check_password_hash()` function just
as we did earlier in this document, and if everything checks out, we
call the `login_user(user)`, which sets the user session. Behind the scenes, `flask_login`
called the `load_user()` function we defined in `models.py`. In the end, we redirect
to the account page for the user.

Finally, we actually render the login page using `render_template`, just as we have
done before.

The rest of the login page is implemented at `login.html`. If a user does not have
an account, though, we want them to register for a new account. In `login.html` we
included a link to the `register` function, so now we'll implement it.

Here's the form in `forms.py`:
```py
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_user(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is taken')

    def validate_email(self, email):        
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email is taken')
```

We specify `StringField`s and `PasswordField`s. There is a validator on the `confirm_password`
field requiring that its data is equal to the `password` field's data.

There are two custom `validate_` functions defined here. One for username and one for email.
Other then these differences, this is all stuff you've seen before.

Here's what happens if we input some wrong data into our form:

![Registration fail][registration_fail]

Now to implement the `register()` function, here is the code:
```py
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)
```

Again, like with `login()`, we redirect to the index if the user is already authenticated.
If a user is not logged in and we received a valid submission for our form,
we generate the password hash like we did earlier in this document, and we just create
a new User, add them to the database, and commit our changes. We then redirect
the user to the `login()` page so that they can login with their new credentials.

Our last line renders the template like we've done before.

What if the current user of our website wants to logout? `flask_login` provides
a function named `logout_user()` which will clear out the user ID from the session.
Let's implement the `logout()` function:

`routes.py`:
```py
from flask_login import logout_user
""" Omitted imports """

""" Omitted code """
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))
```

Pretty simple. We call the `logout_user()` function and then redirect to the main page.
Standard behavior like we see on other websites.

Now, what if we want to restrict some pages on our website so that a user has to be
logged-in in order to access the page? `flask_login` provides the `login_required`
decorator that we can add on top of any view function to restrict access.

Remember the `login_manager.login_view` variable we set in `__init__.py`? When
an unauthenticated user attempts to access a `login_required` page,
they'll be redirected to the `login()` view function, the value of `login_manager.login_view`.

Here is the code for a user viewing their account details:

`routes.py`
```py
from flask_login import login_required
from flask_app.forms import UpdateForm
""" Omitted imports """

""" Omitted code """
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()

    if form.validate_on_submit():
        current_user.username = form.username.data

        db.session.commit()

        return redirect(url_for('account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
    
    return render_template('account.html', title='Account', form=form)
```

We add the `@login_required` decorator above the function. `flask_login` will take
care of the code for redirecting unauthenticated users away from `/account`. 
We create an `UpdateForm()` (we'll show the code for it shortly); the `UpdateForm()`
simply allows users to update their username to something else that is not taken.

Here's `UpdateForm`:
`forms.py`:
```py
""" Omitted code """
class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('That username is already taken')
```

We only have one field for the new username. The `validate_username()` function
checks if the username is already taken; if so, it raises a `ValidationError`. 

So looking back at our code for the `register()` function, if `UpdateForm()`
was validated and submitted, then we can just change the `current_user`'s username
and commit the change. Since `current_user` is of type `User`, any changes
we make to `current_user` can be commited to the database rightaway. 

We have the `elif request.method == 'GET'` so that we can add the user's username
into the username field on page load. This isn't necessary, it's just a 
feature to make it easier for the user to change their username *slightly* if
that's what they are trying to do. 

Here's what it looks like if the form failed to validate:

![Change username failure][username_failure]

The last line, we render our template like we usually do.

One last thing; `current_user` is immediately available for us to use in templates.
You might notice in the templates that we're calling properties of `current_user`. 
We mainly use `current_user.is_authenticated` to show the current user's 
username on all the pages (`base.html`). We also use it to show
the current user's email on `account.html`.

#### Conclusion

We looked at `flask_login` mainly in these notes. We tried to explain
everything to the best of our ability, giving examples for everything you
might need to implement a user management system for your own website.

If you'd like to learn more about anything presented in this document,
here are some links:

[WTForms Docs](https://wtforms.readthedocs.io/en/stable/index.html)

[Custom validators in WTForms](https://wtforms.readthedocs.io/en/stable/validators.html#custom-validators)

[Flask-Login Docs](https://flask-login.readthedocs.io/en/latest/#flask-login)

[login_fail]: ./images/login_fail.png "Login failure visual"
[registration_fail]: ./images/registration_fail.png "Registration fail visual"
[username_failure]: ./images/username_fail.png "Username fail visual"