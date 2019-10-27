# P4: Flaskit - Reddit, but Simpler

**Assigned**: October 26th

**Due**: November 9th, 11:59 PM

**Late Deadline**: One day after due date, for 10% off: November 10th, 2019, 11:59 PM

## Description

You will finish the creation of a social news aggregation website, similar to Reddit. 
A user should be able to register, login, create a video or a textual post, 
comment on any post, or change their username.

Here's the link to the slides folder, where the project 4 demo and errors demo
are shown: [Drive folder](https://drive.google.com/drive/folders/19t_C_zQDDfC06Ka_1AwwwkWyijcsOUJ5?usp=sharing).

The parts you'll be implementing are the Register/Login system, creating comments, 
and the Content Security Policy (CSP) setup. You'll be required to use Bootstrap
for this project (no new features, stuff we did in `wk9` with forms). You'll
need to use the Bootstrap CDN links and be able to embed YouTube videos,
so the CSP must be modified accordingly. 

Users can either create a post with text **or** with a YouTube video ID.
We've taken care of the validation and form rendering here.

For your testing purposes, we retrieve YouTube video IDs by retrieving the
string at the end of the `'https://youtu.be/'` string:

![YouTube link][youtube_link]

In this case, the video ID is `Lhf9dekzyq4`, and we'll check that the video ID is 11 characters.

We call a function named `dictConfig` near the beginning of `__init__.py`. You won't have
to know what it does for this class, but we are just configuring how the logger will work for when
you are testing out your `Content-Security-Policy`.

## Setup

Activate your virtual environment, and 
`pip install Flask flask-sqlalchemy Flask-WTF flask-login flask-bcrypt flask-talisman` 
if you haven't already.

Optionally, `pip install python-dotenv` to easily set environment variables when working.
For more info on how `python-dotenv` works, look at the end of the week 2 lecture.

## Project

Given Users:

| Username     |        Email         |         Password |
| ------------ | :------------------: | ---------------: |
| harry_potter |    harry@hogw.edu    |   VoldemortSucks |
| gvanrossum   |   guido@python.org   | ilovepython3.8.0 |
| elon_musk    |    elon@tesla.com    |     ILoveCars!90 |
| a_einstein   | albert@princeton.edu |          physics |

We've laid out the infrastructure for displaying posts, creating posts, showing comments,
looking at post details and looking at user details (their entire
history of activity on the site).

A `Post` is either a **text post** *or* **a YouTube video ID**. If you look in `index.html`
`user_detail.html`, or `post_detail.html`, you'll see that we generated the embedded YouTube
video using an HTML `<iframe>` element. 
We limit the preview of each text post to 400 characters, after which we truncate
the post and add the `...` to the end.

For this project, you'll have to finish the files `flask_app/users/routes.py`, `flask_app/users/forms.py`, `register.html`, `account.html`, `post_detail.html`, `models.py` 
and `__init__.py`.

We designed the project so that **your code can be very similar to the code we showed in class.**
That is, the login form, the registration form, and the update form, and their renderings in HTML
should all look similar to the code we showed you in the `wk9` lecture. `models.py` requires
defining a user loader, like we did in the `wk6` notes, but you can also see in `wk8` and `wk9`.


`post_detail.html` currently has no way of creating comments. You can find the `CommentForm`
class under `flask_app/posts/forms`. The part of the page where you create comments
looks similar to the post creation area after you choose to create a text post 
(lines 40-45, `create_post.html`). Only authenticated users should be able to make a comment.

`__init__.py` is fine except for the `csp` variable near the top. Recall that we can
change the `Content-Security-Policy` header during web app requests to block resources
from another source.

In our case, that means we can't load the Bootstrap CSS and JS files with links, or 
even the YouTube videos, so the app will look like this when you start it up:

![csp image failure][csp_blockage]

All you have to do is alter the `csp` variable accordingly
to allow our website to load resources from these sites, and these sites only, i.e.
don't use a `csp` with the value of `*`, because that is just dangerous.

You may notice in your console some large messages, one of them might look like this:

```
[2019-10-27 05:55:02,702] INFO in routes: 
Violated directive: script-src-elem, 
Blocked: https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js, 
Original policy: default-src 'self'; report-uri /csp_error_handling
```

This is simply a logging message system we've provided to you. We setup the report handling
and printing so that you can see if your `csp` is working.

Refer to the `wk7` notes to see how to alter the `csp` to accept the Bootstrap CSS/JS files and
YouTube videos. If you aren't getting any logging errors, you're good to go.

Here's the list of things you should complete, for clarity:

1. `flask_app/users/routes.py` - Finish writing the functions for handling
   user registration and login. Passwords should not be stored in the database as
   plain strings, they should be hashed. This code will look similar to the code
   we've written in class before, so be sure to refer to that.
2. `flask_app/users/forms.py` - Create the RegistrationForm and UpdateForm, 
   with validators to check that an email has not already been registered with, 
   the confirm password matches the password field, and a username that the user is
   trying to use (either a new user or existing) is not already taken. You can
   check the description below to see all of the fields for RegistrationForm.
   Check out the demo videos if you're wondering how anything is supposed to look.
3. `register.html` - Render the login form, LoginForm, with Bootstrap formatting. For
   examples of how to do this, check the `wk9` code and `login.html`. You **should**
   show errors that occurred during registration if there were any.
4. `account.html` - Same as (3), except with the UpdateForm. Check out the demo
   or the description below. You **should** show any errors that occurred during the update.
5. `post_detail.html` - Shows the post, full text if it is a text post,
   and shows a list of comments. You should see the list of comments when you get
   this project. The **CommentForm** has already been created. You just need to
   render it, only if the current user is authenticated. We don't want
   lurkers making comments on our posts.
6. `models.py` - Use the `UserMixin` class of `flask_login` to indicate
   where the class representing your user is. Then, create a function
   that returns a user given an ID, decorating that function with `@login_manager.user_loader`.
7. `__init__.py` - Alter the `csp` variable to allow Bootstrap CSS/JS files and YouTube
   videos to load. **You may want to do this first** so that the website is nicer
   to look at. Refer to `wk7` to understand how to add more to the `csp`. Also, we have
   already configured a logger for you. It will print a message to the console
   every time there is a CSP violation with information on which URL was blocked and
   what the CSP at the time of blocking.

**Forms:**

The **RegistrationForm** should have
- Username,
- Email,
- Password,
- Confirm Password
- Submit Field
- Validators to check that the email is valid, 
  username is not taken, email is not taken, and passwords match

The **UpdateForm** should have
- Username
- Submit Field
- Validators to check that the username is not taken

The **CommentForm** has already been created, but you should remember
that we only want to show the form on the `post_detail.html` page only if
the user of our application is authenticated.

Everything else you need should be imported and ready to use. If you have
any questions or notice any mistakes in our project setup, please let us know.

## Testing

You can run the flask app by setting the environment variable `FLASK_APP` to `run.py`.
Or if you have `python-dotenv` installed, just do `flask_run`.

- Make sure your `models.py` is setup correctly with `flask_login`. That is, 
  you indicated the User class by making it a subclass of `flask_login.UserMixin`
  and you decorated a function that returns a user with `@login_manager.user_loader`.
- Test the comments form, ensure that you can only see it when logged in.
- Test your registering, logging in, logging out, and account update functions to 
  see if they are all behaving as they should. You might find **DB Browser for SQLite**
  useful if you want to checkout your database's values.
- Check that you're not receiving any logged messages in your console because
  of your `csp` configuration. If your `csp` is sufficient, your home page will
  have a similar style to the home page shown in the demo movie, and you'll be able
  to watch all of the YouTube videos.

## Submissions & Grading

Make sure that you've tested parts of your website and that links to the frontpage
exist and are clearly visible, and then zip the `flask_app/` directory, and submit that zip
to the submit server. The submit server will not show test results, but just display "ACCEPTED".

Your project will be graded as follows:

| Requirements                                                              | Points |
| ------------------------------------------------------------------------- | :----: |
| RegistrationForm and UpdateForm created correctly, with validators        |   10   |
| User creation/mutation forms processed correctly (hashed passwords, etc.) |   30   |
| `models.py` setup to allow `flask_login` to work properly                 |   10   |
| CommentForm rendered only when a user is logged in                        |   10   |
| Registration, Login, and Updating username works as shown                 |   20   |
| ValidationErrors thrown are shown to the user                             |   10   |
| CommentForm rendered only when a user is logged in                        |   10   |
| Forms and error messages rendered with Bootstrap                          |   10   |
| Rendered forms have CSRF tokens                                           |   10   |
| CSP modified to load Bootstrap CSS/JS CDN links and YouTube videos        |   20   |
| All other website functions still work                                    |   10   |

If you download Bootstrap and use it for this project, that is not a substitute for 
setting the correct `csp` in `__init__.py`. 

**Tip:** If you `pip install black`, you can then navigate to the `p4/` directory and type `black .`
to reformat and style your code to match convention, uncompromisingly.

The project will be graded out of 150 points. You won't be graded for style, but make
sure your code is readable and clean, and well commented if you are
making a larger, complicated function.


[youtube_link]: ./images/youtube-share.png "YouTube Link Visual"
[csp_blockage]: ./images/csp_blockage.png "CSP Failure Visual"