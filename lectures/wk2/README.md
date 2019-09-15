# Week 2
### Intro to Flask

The slides for this week are linked on Piazza.

The code in this directory is what we created in class, a more detailed
description of everything going on will added here later.

To run the code, make sure to `pip install Flask` if you haven't already.

##### Decorators

To understand all of the `flask` code we'll be writing, we have to understand
a different Python language feature first: decorators.

Simply put, a decorator is a function that returns another function. That is the
official definition. Practically, a decorator is often used as a function
transformer, using `@{function_name}` in front of a function declaration.

Remembering that functions are first-class objects in Python (so they can
be passed around like other data), let's go over a simple example:

```python
def func_requestor():
    def a_func():
        print('This is a_func here!')
    
    return a_func # The function identifier

func = fun_requestor()
print(type(func))
func()
```

We create a function named `func_requestor`, define an inner function `a_func` that
prints a string, and back in the main function body we return `a_func`. We don't use
parentheses because we want to return the function itself; we don't want to return
the result of the function.

Then we call the `func_requestor` outer method and store the returned function in the
variable `func`. After we print the type of `func` and then actually call `func()`, we get

```python
<class 'function'>
This is a_func here!
```

Now to try something more useful, we can create a decorator that will print some string
before a function is called and after a function is called. 
This is a function transformation; we have a function named `hello_world`, and
we're altering how our `hello_world` function works by decorating it with extra print 
statements. We'll repeat the steps we took above 

```python
def first_decorator(func):
    def wrapper():
        print('This is before func is called')
        func()
        print('This is after')
    return wrapper

def hello_world():
    print('Hello, World!')

func = first_decorator(hello_world)
func()
```

And this prints:

```python
This is before func is called
Hello, World!
This is after
```

Now we can create a decorator that will only execute functions if `sun_is_up`
is `True`.

```python
sun_is_up = True

def decorator(func):
    def wrapper():
        if sun_is_up:
            func()
        else:
            pass
    return wrapper

# This still works, but there's a sugary way
func = decorator(hello_world)

@decorator
def hello_neighbor():
    print('Hello, neighbor!')

hello_neighbor()
```

Which prints:

```py
Hello, neighbor!
```

The `@` symbol applies the decorator function named `decorator` to
the `hello_neighbor` function. This syntactic sugar version is a faster
way of writing `func = decorator(hello_world)`, and you can add it at the
function declaration itself. 

Flask uses decorators extensively for specifying website routes,
and we can use decorators to check for login status and other important states.

##### Flask

All `flask` apps use the `flask.Flask` class which is initialized with `__name__`.
The `__name__` special variable will be set to `__main__` if it accessed 
inside the python file that we run with `python3 file.py`. In other files, 
`__name__` will be set to the module name or directory path relative to the 
main file being run.

To understand some more, let's write a basic hello world app in flask, in a file
named `hello_world.py`.

**Note:** You don't have to name your file what we do in these examples. We do it
for organization and as a guide for people who might want it.

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```

We start by importing the `flask.Flask` class and initializing it with the
`__name__` special variable. Then, in our `hello_world` function we return the
string 'Hello, World!'. Where does this string go? Can it show up on our website?
That's where `app.route()` comes in. We apply `app.route()` to the `hello_world`
function with a parameter specifying where the function's access point will be.

In this case, we set the route to `'/'`, so this function will be run when we
access the index of our website. 

Now to run the application, we need to set the environment variable `FLASK_APP`
to point to our main python file, and then we can run the app.

```zsh
$ export FLASK_APP=hello_world.py
$ flask run
```

Environment variable setting could be different on different systems, so 
here are some alternative ways to set environment variables:

Powershell:

```posh
> $env:FLASK_APP = "hello.py"
```

Command Prompt:

```cmd
set FLASK_APP=hello.py
```

After running, we get this output. Keep in mind that your output may look different,
but as long as it says the app is running and it gives us a url to connect to, you're fine.

```zsh
$ flask run
 * Serving Flask app "hello_world.py"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Connect to `http://127.0.0.1:5000/`, and behold your (possibly) first Flask app!
Press `CTRL+C`, or your system's relative command, when you want to quit.

**Creating more pages**

So you want to create a web application, so you probably want to create more pages 
that your users can navigate to and and see your content. As we have before, we'll
use the `app.route()` decorator on different functions to create new pages.
We can also configure a function to execute at multiple routes by stacking
our `app.route()`s. 

We're modifying and adding to our `hello_world.py` app.

```py
@app.route('/')
@app.route('/index')
def hello_world():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'Hello! Calling from CMSC388J\nI\'m starting to love Flask!'
```

Execute `flask run` and enter your website. Try adding `index` and `about` to the end
of the url and observe what the page looks like. 

Now let's look at another feature of routing. Let's say we want to visit the profile
page of a certain user. We don't want to create a separate view function or a separate
route decorator for every user, that's annoying and error-prone.

As a real-world example, Reddit uses the route `/u/<username>` to go to 
the user page for `username`. Let's do the same. In a new file called 
`users.py`:

```python
# -- Omitted app setup code -- #
@app.route('/')
def info():
    return 'Append "user/{username}" to the end of the url to go to <i>username</i>\'s page'

@app.route('/user/<username>')
def show_profile(username, thing):
    return 'This is %s\'s user profile, %s' % username
```

Try navigating to `/user/` with your name at the end, or `/user/_why` or 
`/user/shepmaster`. In the `info` function, we use the HTML tag `<i>` to italicize the 
string `'username'`. We can return any HTML with these view functions, and we'll try to
explain what we're doing when we use new tags. If you have any questions, just ask us. 
The code in the `show_profile` function returns a C-style formatted string. The 
delimiters like `%s` and `%04d` are the same, and you
can substitute for those values using `% (tuple_of_values)`.

Before we continue on further, there's an easier way to change your code and then see
the resulting app without having to close the server and restart it each time.
We can set the `FLASK_ENVIRONMENT` environment variable to `development`, and
when we reload the relevant changed pages, we'll see the new changes.

**Warning:** You may see this piece of code out in the wild in some Flask apps:

```python
if __name__=='__main__':
    app.run(debug=True)
```

This piece of code in our main flask app file allows us to run the app using
`python app.py` (if this code is present in the `app.py` file), but is badly supported.
The officially recommended way is to set the environment variables and use `flask run`.
If you find it tedious to set the environment variables each time you open up a flask app,
you're not along. At the [end of this document](#optional-config-info), 
we have additional configuration info.

**Templates**

So far we've just been returning strings on our web pages. What if we want
different sized headings, bolded or italicized text, links, lists, or images
on our website? We could write a view function like this:

```python
# -- Omitted setup code -- #
@app.route('/')
@app.route('/index')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Document</title>
    </head>
    <body>
    Hello, this is a <b>good</b> example of a <i>bad</i> way to render HTML documents.
    </body>
    '''
```

This works, but is tedious. What if we want to add a navigation bar, a search bar, pagination,
or just want to write a really long post? Not to mention all the JS code you might want to
add for ✨i n t e r a c t i v i t y ✨. This is where `Jinja2` comes in to play. It's installed
with `flask`, so we can get started using them.

By default, `flask` searches for templates in the `./templates` directory, so we'll
first create an `./app` directory to hold all of our code, and then make the 
`./app/templates/` directory where our HTML templates will reside.

In `base.html`, all the lines before `<body>` are just standard lines in HTML5 
documents. We don't have to worry about most of them; you can change the text in between
the `<title>` tags to change what name is shown in your browser tab for your website.

There are some characters that are not seen in HTMl documents: `{% %}`. These are `Jinja2` 
delimiters. We use these delimiters to create our template, and they allow us to dynamically
change content.

Here's a list of `Jinja2` delimiters and how they might be used:

- `{% ... %} for statements: if, for, set, block
- `{{ ... }} for expressions: call functions, compare/calculate values, or use literals
- `{# ... #} for comments 

`Jinja2` templating code syntactically resembles Python code, and has some more features
than Python specific to templating, and lacks some Python features to make the template
easier to read and to discourage putting too much logic into the template. For example,
list comprehensions are not supported. There are many more ways of customizing the 
templates, but we won't go into detail about them, yet.

Back to `base.html`, if a `message` variable is set to `'Hello'`, then we include a certain heading
in the HTML document. We include `elif` and `else`, and finally end with an `{% endif %}`. We're
required to end control flow statements (if, for) explicitly because HTML documents 
could have arbitrary indentation and it's hard to enforce Pythonic indentation rules. Where does
the `message` variable come from? It's something that we have to pass in to the template
when we render it, which we'll show you how to do later.

Finally we declare a `block` named `content` using `{% block content %}` and similarly to `if`
statements, we end it with `{% endblock %}. A `block` indicates that all of the code 
inside the block can be overridden in another template that `extends` our `base.html` template.
The extending template would be called a 'child' template. 

If we're making a social networking web application, we might have a feed of user's posts.
In `feed.html`, we've created a template for displaying all the posts from a `posts` iterable.
Again, the `posts` iterable is something that we have to pass in to the template when we render
it, and we'll show you how to do that soon.

The first line in a child template has to be `{% extends "parent_template.html" %}`,
where `parent_template.html` in our case would be `base.html`. We get all the HTML
from `base.html`, and we get to insert HTML code into the `content` block. In this case,
we iterate over each of the entries in `posts` and we output some HTML. The `<h2>` tag
creates a smaller heading than `<h1>`, and the `<b>` tag bolds the text in between.
We use `{{ post.user }}` to retrieve the value for `user` in `post`. If `post` is a
dictionary, we can use `{{ post.user }}` or `{{ post['user'] }}` to retrieve the value.
We do the same retrieval for the `text` key, and then end our `for` loop and `content` block.

```html
{% extends "base.html" %}
{% block content %}
{% for post in posts %}
    <h2>{{ post.user }}</h2>
    <b> {{ post.text }}</b>
{% endfor %}
{% endblock %}
```

We'll add to this later in this README, the full version is already in `feed.html`.

Back to our main flask app file, we'll create some sample content:

```python
posts = [
    {
        'user': 'Elon Musk',
        'text': 'The sun is a theronuclear explosion fyi',
        'location': 'California',
        'likes': 3_000_000,
    },
    {
        'user': 'John Smith',
        'text': 'Excited for school!!!!',
        'location': 'College Park',
        'likes': 5
    }
]
```

We also created a `about.html` file which extends `base.html` and adds another string.

Now to render our templates, we'll use the `render_template` function that's part of
the `flask` module. The first argument to `render_template` is the template file. If your
template file is located in the `templates/` base directory, you can just enter the name 
of the file. Then, we can pass in an arbitrary amount of variables that should be available
to our template. Remember the `message` and `posts` variables we used in our templates?
We can pass them in here.

```python
from flask import Flask, render_template
# -- Omitted code -- #
@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', message='hello')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/feed')
def feed():
    return render_template('feed.html', message='feed', posts=posts)
```

Since both `feed.html` and `about.html` extend `base.html`, we can pass in the `message`
variable that was used in `base.html` to these two templates and the appropriate heading
will be output. Some heading will always be output, because we have an `{% else %}` clause
in `base.html`.

Now we can make our feed a little spicier by including the location from where 
the posts were made and the number of likes that each post got. We'll alter our
`feed.html` slightly:

```
{% extends "base.html" %}
{% block content %}
{% for post in posts %}
    <h3>{{ post.user }}</h6>
    <h4>> {{ post.text }}</h4>
    ❤ <b>{{ post.likes }} <span>&#183;</span> {{ post.location }}</b>
{% endfor %}
{% endblock %}
```

The `<h3>` and `<h4>` tags are differently sized headings, and `&#183;` is the 
HTML code for a vertically-centered dot. If we run `app.py` now and navigate to
`/feed`, we'll see all of our posts there.

As one last modification, let's make the users' names as clickable links that
will redirect a visitor on our site to the user's profile page. There's a
special function in `flask` and `Jinja2` called `url_for`; the first argument
has to be the name of a routed function. The other arguments are all of the arguments
to pass to the routed function. In this case, we'll be calling a function named 
`profile` which takes as an argument a `username`. This is the example with the usernames
that we did above. Since `url_for` returns a string, it is an expression, and we
surround it with double curly braces.

The `<a>` tag is for links, and we have to specify the `href` attribute to point to
another route on our website. We use `url_for`.

```html
{% extends "base.html" %}
{% block content %}
{% for post in posts %}
    <a href= {{ url_for('profile', username=post.user) }} ><h3>{{ post.user }}</h6></a>
    <h4>> {{ post.text }}</h4>
    ❤ <b>{{ post.likes }} &#183; {{ post.location }}</b>
{% endfor %}
{% endblock %}
```

With this knowledge, let's add a link to go to the feed on the `base.html` template.
We'll put the link in the `content` block so that child templates that override
this block won't get the unecessary link to the feed.

`base.html`:
```html
<!-- Omitted code -->
{% block content %}
<a href= {{ url_for('feed') }}>Go to Feed</a>
{% endblock %}
<!-- Omitted code -->
```

Try running this and clicking on our new link. It will go our feed, where we can click
on links to go to each user's profile page.

These are the starting notes for Flask, and what you'll need to know for the project.

##### Optional Config Info

If you name your `flask` app `app.py`, then you don't need to specify the 
environment variable `FLASK_APP`, though it's still good practice.

If your main `flask` file is named something else, or if you want debug mode turned
on, you might think it's too tedious to set the environment variables every time to
sit down to work on a `flask` project.

We can define the environment variables in a file named `.flaskenv` or `.env`. The
`.env` has higher priority than `.flaskenv`, but for our purposes, the difference
doesn't really matter. To use this file automatically when you type `flask run`, 
you need `python-dotenv` installed, which you can do with `pip install python-dotenv`.
Flask automatically detects that `python-dotenv` is installed and will look for `.env`
or `.flaskenv` files, but will pass with no behavior if they don't exist.

A simple `.flaskenv` that we can define is the following:

```zsh
FLASK_APP=app.py
FLASK_ENV=development
```

This file will automatically be made available in future projects.
