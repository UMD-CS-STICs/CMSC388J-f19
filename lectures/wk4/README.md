# Week 4
### Databases and SQL Injections

The slides for this week are linked on Piazza. 

The code in this directory is what we created in class, plus possibly some
more detail or fixes. This README contains a detailed description of everything.

To run all of the code, make sure to `pip install Flask flask-sqlalchemy`

Optionally, `pip install python-dotenv` to automatically set environment
variables in Python

### Python Classes

First, a brief overview of classes in Python. You know what classes are already,
they're blueprints containing the properties and methods of a certain object.
You've worked with Java and Ruby in your classes and possibly others on your own,
and today we'll be looking at Python classes.

First, there are no formal interfaces in Python. Python does have Abstract
Base Classes (ABCs) that provide methods that must be implemented by subclasses.
There are also 'dunder' methods, methods that have double underscores before
and after a name. These are special methods that are called by built-in functions
and by operators.

Some dunder methods you may have already used are `__len__`, `__mult__`, and `__iter__`.
These methods are called by `len()`, `*`, and `for i in seq` (`seq` is the variable with
`__iter__` defined), respectively. Another example of a dunder method is `__str__`, 
which is called when you try to `print()` an object.

When creating a class, you have to provide an `__init__` method which is the constructor
for the class, and all instance methods of your class should have `self` as the first parameter.
We'll go over static/class methods at another time if they're needed.

Finally, you can use decorators inside classes to decorate methods or you can even
decorate the class as a whole. The same syntax is used in this case.

### Project Structure

To start off, we're restructuring our Flask apps going forward to conform
to Python standards, and to make our code cleaner/easier to read and run.

In this directory you'll see the `flask_app/` directory. This contains all the code
we write to create our app. This directory as an `__init__.py` file, which indicates
that the `flask_app/` directory is a Python package. 

The directory structure of `flask_app/`:
```
├── __init__.py
├── data.py
├── models.py
├── old_app.py
├── routes.py
├── templates
│   ├── about.html
│   ├── base.html
│   ├── feed.html
│   ├── index.html
│   ├── user.html
│   └── user_info.html
└── users.db
```

`old_app.py` contains our application code from week 2 for reference.

In the `__init__.py` file, we import the packages we need to create and
configure our application. Any variables we create in the `__init__.py` file
can be accessed using `from flask_app import var`, where `var` is a variable defined in
`__init__.py`. We'll create and set configuration options for our app in `__init__.py`.

To start off, we'll import `flask` and `sqlite3`. `sqlite3` is a builtin Python
module that will allow us to work with a local database. We'll also create our
application.

```python
from flask import Flask
import sqlite3

app = Flask(__name__)
```

We have our static `posts` data in the same file as our app currently. We'll
separate it into its own Python module for organization. `data.py` contains the
`posts` list of dicts now.

You might be wondering where we configure our routes now; we do it in `routes.py`.
Remember that we can import our app using `from flask_app import app`.
Next, we want to render templates and actually create our pages, so we'll also
import the `render_template` function from `flask`. Finally, we want to use
the `posts` list of dicts in our application, so we can import that from `data.py`, also.
We'll import some extra things from `flask` here and explain how we use them later.

`routes.py`:
``` python
from flask_app import app
from flask import render_template, request, redirect, url_for
from flask_app.data import posts
```

Outside the `flask_app/` directory, in the `wk4/` directory, we'll have a file
named `run.py`. This will be the file that we set to the `FLASK_APP` environment
variable. Using `flask run` in the `wk4/` directory will allow the database route to
work correctly. 

### SQLite Databases (Unsafe) Intro

Let's say we have a scenario where we want to allow visitors to our site to search for
users and get certain info about the users. People accessing our site should be able to get
the user's name and their bio, but not any other information, such as email or location.

First, we need some data in our database. To get a visual guide to create a SQLite database, 
we'll use [DB Browser for SQLite](https://sqlitebrowser.org/). This application also lets you
view the data in your database, so you can use it for visual checking when you're prototyping
your own applications.

In the DB Browser, we'll create a new database using `File -> New Database`. Create a new
database in the `wk4/flask_app/` directory with some desired name. 
We'll call our database `users.db` for clarity. An `Edit table definition` window should pop up:

![Create Table Window shown here][create_table_img]

We'll fill out this table using the values and options as shown in the slides, put
here for reference:

![New Table form filled out][users_table_img]

The top of the window is where we put the name of our new SQLite table. In the middle window,
we specify the name of each row in our table. In our case, we define the rows `id`, `name`,
`bio`, `email`, and `location`. 

`id` is designated as the primary key, which must be a 
unique value to differentiate each record in the table, so we'll just make it an integer
and auto-incrementing. The next four values are text strings, and we want every user
to have a bio, an email, and we want their location. This might be used in an application
for organizating meetups. 

We check off the `NN` option to indicate that we want a value
for each of these rows. We also check off the `U` value for our `email` field
so that two users cannot have the same email registered.

You can see the SQL query that is being generated by the DB Browser app in the bottom section.
This is the query that is executed to create our `Users` table in our database. After clicking
`OK`, your table will be created, and you can add data by going to the `Browse Data`.
In `Browse Data`, we can click the `New Record` button and then fill out the fields.
Here's some sample data that we used:

![Sample user data][user_data_img]

### Search bar - POST request (pt. 1)

Now in our templates directory, we'll create a template for a new page on our website
that will allow us to query user data. On `index.html`, we add the link to the User Info
page using:

``` html
<a href={{ url_for('user_info') }}>User Info Page</a>
```

The `url_for` function calls a routed function named `user_info`. We don't have a `user_info`
currently, so we create the method. In the `app.route()` decorator, we'll specify another
parameter named `methods`. We want a website visitor to be able to submit a form to
search for users and then see their name and bio. To do this, we'll configure the 
function like so:

```python
@app.route('/info', methods=['GET', 'POST'])
def user_info():
    pass
```

The `GET` request verb is automatically included in each routed function, unless its
explicity excluded using the `methods` parameter above. `methods` accepts a list of
HTTP verbs. We're using `GET` and `POST` here, but there are also other
verbs that you can specify by including it into the list to `methods`.
[Wikipedia][http verbs] has a list of these.

When a form on the `/info` page of our website is submitted, our `user_info` function
can access the information by using the global `request` object. We imported this
from `flask` earlier in `routes.py`. 

Let's create the actual form first, so we know what kind of data we'll be working with.

### HTML (unsafe) form

We'll create a new template file named `user_info.html` where we'll create an HTML form
so that site visitors can search for users. After the form is submitted, we want to show 
the results of the visitor's query on the same page. 

Here's our `user_info.html`:
```html
{% extends "base.html" %}
{% block content %}
<h1>User Info</h1>

<b>Enter a User's name to see their bio</b>
<form method="post">
    <input type="text" name="Username"> <br>
    <!-- <input type="text"> -->
    <input type="submit" name="All" value="See all users">
    <input type="submit" value="Submit">
</form>
<br>

Format: <br>
<b>User : Bio</b>
<ul>
{% for info in user_info %}
    <li>{{ info[0] }} : {{ info[1] }}</li>
{% endfor %}
</ul>

<a href={{ url_for('about') }}>About this Website</a>
<a href= {{ url_for('feed') }}>Go to Feed</a>
{% endblock %}
```

We make the form using the `form` HTMl tag, and we specify the method to be `"post"`. This
will send `POST` data to the function that is rendering this template. In our case, 
this form will send data to the `user_info()` function in `routes.py`. We have a text
input field and a submit input. 

At the bottom of the template, we specify the format of returned data and then display
all of our data. `user_info` will be a list of results, so we display all the results
using an unordered list. Finally, we end with links to other parts of our web application.

**Note:** This example is an unsafe way of using forms, because there is no protection against
CSRF (cross-site request forgery) attacks. We'll get into how to prevent those next week.

### Search bar - POST request (pt. 2)

Now, we'd like to update our `user_info()` routed function to handle the form data. Recall from
above that we can access the request data by using the global `request` object
that we imported using `from flask import request`. 

This code won't work yet,
```python
@app.route('/info', methods=['GET', 'POST'])
def user_info():
    if request.method == 'POST':
        return redirect(request.path)
    else:
        return render_template('user_info.html', title='User Info', user_info=user_info_data)
```

The `request` object has a property named `method` that indicates what type of request
was made to our application, so we check if its equal to `'POST'`. In this branch
of the `if-else`, we will redirect back to this function using `redirect(request.path)`.

We want to redirect because we're done processing the `POST` request. If we omitted the redirect,
then whenever a visitor reloaded the page after submitting the form, they would be asked
if they are sure they want to reload because form data may need to be resent. To get around that,
we redirect to our function. The path to our function is easily accessible as `request.path`, 
because the `request` object pointed to the `user_info()` function when the form was submitted.
The default HTTP method used is `GET`, so we would go into the `else` clause of the `if-else` 
branch.

The redirect confirmation prompt:
![Redirect confirmation][redirect]

In the `render_template()` function, we're specifying the `user_info` iterable in our template
to use data from some variable named `user_info_data`. That doesn't exist currently, but will
contain the search results once implemented.

How can we add search results to `user_info_data` and have the data persist across the redirect?
A straightforward way is to make it a global variable:

```python
user_info_data = []

@app.route('/info', methods=['GET', 'POST'])
def user_info():
    global user_info_data
    if request.method == 'POST':
        return redirect(request.path)
    else:
        return render_template('user_info.html', title='User Info', user_info=user_info_data)
```

The `global` keyword at the beginning of the function indicates that we want to mutate
the global `user_info_data` list. Trying to mutate a global variable inside of a function
is not possible without the `global` keyword.

Now we want to process the form data, retrieve relevant results from our `Users` table in our
database, and then display the results. To access the database, we'll edit our `__init__.py` file
to use the `sqlite3` database:

```python
from flask import Flask
import sqlite3

app = Flask(__name__)

db_path = 'users.db'
db = sqlite3.connect(db_path)
```

The `db` and `db_path` variables now exist in `flask_app`, but we're only going to use
`db`. Recall that we can import it into other files using `from flask_app import db`.
Back to `routes.py`, we'll edit the first line:

```python
from flask_app import app, db
""" Omitted code """
```

Further down in `routes.py`:

```python
user_info_data = []

@app.route('/info', methods=['GET', 'POST'])
def user_info():
    global user_info_data
    if request.method == 'POST':
        cursor = db.cursor()

        stmt = "SELECT name, bio FROM Users WHERE name = '%s' " % request.form['Username']

        result = cursor.execute(stmt)

        data = []
        for item in result:
            data.append(item)

        user_info_data = data

        print(stmt)
        
        print(request.form['Username'])

        return redirect(request.path)
    else:
        return render_template('user_info.html', title='User Info', user_info=user_info_data)
```

We use the `%s` format specifier in the SQL statement to insert the text input from our form.
Since we are requesting the `name` and `bio` from our `Users` table of our database, a tuple
is returned with this format: `(name, bio)`. 

To run the application, we'll need to edit `__init__.py` slightly, we'll add the line
`from flask_app import routes` at the end, so it looks like this:

`__init__.py`:
```python
from flask import Flask
import sqlite3

app = Flask(__name__)

db_path = 'users.db'
db = sqlite3.connect(db_path)

from flask_app import routes
```


If we run the application in the current
state and enter the string `Harry Potter` into the search field, we'll get a result back:

![Harry Potter result][hp]

This is all fine, but this code is vulnerable to an SQL injection attack. We're
not cleaning the form data before inserting it into our SQL statement. To demonstrate
how we can obtain the location and the email for each user from the `Users` table, also,
we created this statement:

```sql
' UNION SELECT name, location FROM Users UNION SELECT name, email FROM Users '
```

The first `'` character closes the single quotes in our statement. Then, we use the 
`UNION` verb to chain another SQL command. The second SQL command selects the 
`name` and `location` of each user in the `Users` table. We do the same thing again, 
but obtaining the `email` of each user now. 

The reason we can only pick two values at a time is because our statement is already obtaining 2
columns: `name` and `bio`. When we use `UNION`, we can only `SELECT` from two columns at a time,
also. Finally, we end the statement with a `'` character to close out the second single quote.

We'll run the web app and then put in this string for the form data input and click submit. 
You should get output similar to this:

![SQL Injection Results][injection]

If we want to prevent this while using `sqlite3`, we can edit a few lines to prevent this:

`routes.py`:
```python
""" Omitted code """
    """ Inside user_info() """
        stmt = 'SELECT name, bio FROM Users WHERE name = ?'
        result = cursor.execute(stmt, (request.form['Username'],))
```

And if we reload the web app and try the injection attack again, it won't work. The
`?` character is a placeholder. We pass in a tuple of values as the second parameter
to `cursor.execute()` and they will be substituted in for the question marks and 
automatically escaped to reduce the risk of an injection attack.

### SQLAlchemy

We just went over how an SQL injection attack would be executed and how to
prevent it when using `sqlite3` or another module to execute raw SQL statements.

There is a safer and more convenient way to work with database tables, and we don't
have to change our database-specific operations if, for example, we wanted to
use SQLite for prototyping our application locally and then use Postgres
for a production server. 

We'll use `SQLAlchemy` from now on, specifically through the `flask_sqlalchemy`
extension. Today, we'll go over a simple example of how to work with SQLAlchemy. 
To set the URI, which is just an identifier for our database, we use:

`__init__.py`:
```python
""" Omitted code """
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
""" Omitted code """
```

We want to use a `sqlite` database for prototyping. If we put 3 slashes after 
`sqlite:` then we create a database on a relative path. In this case, we
connect to `users.db` in the same directory as `__init__.py`, so we connect
to our previously created `sqlite` database.

If we use 4 slashes, we can specify an absolute path on our system; if we use 2
slashes, we create an in-memory database, so we can only poll and modify the database
while the application is running.

We'll also specify another option:

`__init__.py`:
```python
""" Omitted code """
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
""" Omitted code """
```

We disabled an option that wasn't needed; it'll just take extra memory.

Finally, we'll create our `db` variable with `flask_sqlalchemy`. We'll delete
all of our `sqlite3` code from `__init__.py` and add our new configuration code, so
it'll look like this now:

`__init__.py`:
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Relative Path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from flask_app import routes
from flask_app.models import *
```

`flask.models` is a module that will contain our `SQLAlchemy` model classes. We'll
create a class called `Users` that has the same schema as the data already
in the database. The name has to be `Users` to match up with the table already in
the database.

`models.py`:
```python
from flask_app import db

class Users(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    bio = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return 'User: %s' % self.name
```

Every table we want to create has to be a subclass of `db.Model`, where you could replace
`db` with the name of your database variable.

Now how can we use this in place of `sqlite3` in our application? `Users` is now a `Model`
class, so it has an attribute named `query`. This attribute allows you to access all records
represented by the class, and then we can pick out certain records by using the `filter()`
method of our `query` object. After that, we can use the `all()` method to get all matching
records.

`routes.py`:
```python
from flask.models import *

""" Omitted code """
user_info_data = []

@app.route('/info', methods=['GET', 'POST'])
def user_info():
    global user_info_data
    if request.method == 'POST':
        user_info_data = Users.query.filter_by(name=request.form['Username']).all()

        return redirect(request.path)
    else:
        return render_template('user_info.html', title='User Info', user_info=user_info_data)
""" Omitted code """
```

Now we can edit the for loop in `user_info.html`. We access the `name`, `bio`, and other
attributes of each record by using dot syntax, so `info.name` or `info.bio`.

`user_info.html`:
```html
{% for info in user_info %}
    <li>{{ info.name }}: {{ info.bio }}</li>
{% endfor %}
```

Running the app in the current state will cause it to run exactly the same way as
before, except now its safer and cleaner to work with.

### Conclusion

In this lecture we showed how to work with `sqlite3` databases a low-level way, 
what could go wrong with injection attacks, and an introduction to using `SQLAlchemy`.
There are more features of `SQLAlchemy` that we'll cover as we need them in coming weeks.



[create_table_img]: ./images/create_table.png "Create Table Window"
[users_table_img]: ./images/users_table.png "Specify Users table"
[user_data_img]: ./images/sample_data.png "Sample Users Data"
[http verbs]: https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods
[redirect]: ./images/redirect.png "Redirect prompt"
[hp]: ./images/hp.png "Harry Potter search results"
[injection]: ./images/injection.png "SQL Injection sample attack"