# Week 6
### User Management

The slides for this week are linked on Piazza. 

The code in this directory is what we created in class, plus possibly some
more detail or fixes. This README contains a detailed description of everything.

To run all of the code, make sure to 
`pip install Flask flask-sqlalchemy flask-wtf flask-login flask-bcrypt flask-mail`

Optionally, `pip install python-dotenv` to automatically set environment
variables in Python.

### Securing Passwords

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

**More detail coming**