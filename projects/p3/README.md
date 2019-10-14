# P3: Open Blogging App

**Assigned**: Week 4, October 1st

**Due**: Week 6, October 16th, 2019, 11:59 PM

**Late Deadline**: One day after due date, for 10% off: October 17th, 2019, 11:59 PM

## Description

You will be creating a website that allows visitors to read blog posts and submit
their own blog post or add a comment to existing blog posts. There won't be any
authentication process, we'll be covering that at the next lecture.

## Setup

Activate your virtual environment, and `pip install Flask requests flask-sqlalchemy Flask-WTF` 
if you haven't already.

Optionally, `pip install python-dotenv` to easily set environment variables when working.
For more info on how `python-dotenv` works, look at the end of the week 2 lecture.

## Project

We've given you starting files, but we have not supplied any forms or any models
for working with `SQLAlchemy`. Instead, we'll tell you specifications for
the tables, and you will create blog posts and comments and users 
to test out your site.

We have given you templates for the three different types of pages that you'll see
on this blog. `index.html` should be a list of blog posts. The template
has all of the formatting taken care of. `post.html` also has all of the formatting
taken care of, you just have to replace the placeholder values
with actual values.

`user.html` does not have the formatting finished. All of the blog posts
created by a certain user should be listed there. Format it the
same way as `index.html` is formatted for listing all of the posts.

In `routes.py`, you're required to implement three functions:

1. `index()` - Shows a list of all of the blog posts created on your website
   
   Routed at: `/`
   Methods: [`GET`, `POST`]

   Display a list of all of the blog posts that have been created, with the
   content of the post being shortened for presentation here, and
   create a form for submitting a new blog post.

   The form for submitting a new blog post should have fields for all the info
   that the user has to provide for their blog post.

   There should be a link on each author's name to go to their user page at `user/<name>`.
   Additionally, there should be a link on each post's title to go to the post's
   detail page at `posts/<post_title>`

   The content synopsis for each blog post here should be limited to 250 characters,
   and should end with an ellipsis (`...`) if the actual content is longer than 250 characters.

2. `profile()` - Shows the user's details and a list of all of the blog posts written by the user
   
   Routed at: `/<name>_<int:user_id>`
   Methods: [`GET`]

   **Update:** The `user_id` parameter was added. This is to differentiate users who might
   have the same name. Sorry for missing this the first time. The `int:` just specifies that
   `user_id` should be an integer.

   Display the user's name, email, the number of posts written, and a list of all
   the blog posts written by the user.

   There should be a link on each blog post's name to go to the post's detail page at
   `posts/<post_title>`. The blog posts should be formatted like they are on the `index.html`
   page. There should also be a link to go back to the index page of your website.

   The content synopsis for each blog post here should be limited to 250 characters,
   and should end with an ellipsis (`...`) if the actual content is longer than 250 characters.

3. `post_detail()` - Shows the full blog post content and a list of comments on that post.
   
   Routed at: `posts/<post_title>`
   Methods: [`GET`, `POST`]

   Display the details of the blog post and the full content of the post, too. There
   should be a form at the bottom for submitting new comments. 

   There should be a link on the author's name to go to their page at `user/<name>`. There
   should also be a link to go back to the index page of your website.

   At the bottom of the page, the comments associated with that blog post should be displayed.
   We provided the formatting. Display the full content of the comment. You don't need to
   have any links in the comments.

   The form at the bottom of the page should include fields for all information
   the user is required to supply to make a comment.

Here, we'll specify the schema of each of the three tables you'll be required
to have in your database. All of the parameters are **non-nullable**.

`User`:
- `id` - integer, primary key
- `Name` - text string
- `Email` - text string - should be validated with a WTForms validator, must be **unique**
  - (Hint: look at the WTForms validators list)
- **Relationship to** `Post` - each user has at least 1 post

`Post`:
- `id` - integer, primary key
- `Title` - text string
- `Author` - text string
- `Date` - datetime object - default value is time of creation
- `Content` - text string
- **Relationship to** `User` - each post belonds to a single user
- **Relationship to** `Comment` - each post has at least 0 comments

`Comment`:
- `id` - integer, primary key
- `Author` - text string
- `Date` - datetime object - default value is time of creation
- `Content` - text string
- **Relationship to** `Post` - each comment belongs to a single post

**Forms:**

`New Post` Form, on `/`:
- `Name`
- `Email`
- `Content`

**Clarifications:** Only the email needs to be unique, that is the constraint
we'll use to distinguish different users.

If a request is made with an email that **already exists** in the database, but
with a different name than the one associated with that email, you should disregard
this `POST` request. You can print out an error message for debugging purposes
if you wish, we will only be checking that the database is not updated.

If a request is made with a name that already exists in the database, but
with a different email that does not exist in the database, this request 
should still go through and create a new user, since we are differentiating users by their email.
  
`New Comment` Form, on `/posts/<post_title>`:
- `Name`
- `Content`

**Clarifications:** There are no restrictions on who can comment, so you don't
have to check for anything here. The `name` is not associated with a user.

Use the examples from the lecture notes if you get confused on how to create 
these tables.

In `templates/`, all of the lines in the files that should be changed are
pointed out to you. Determine how to fix the line with `Jinja` so 
that we can show the data that the placeholder represents.

Your forms should be CSRF protected. To make sure they are CSRF protected, you should
also generate a secure random token and set the `SECRET_KEY` in `__init__.py`.
When rendering your forms, include the CSRF token as the first field.

In `utils.py` we included a function that takes a datetime object and
returns a string representing the object. This will be useful when trying to
display the date!

All other tools you use may need to be imported, such as the validators from `flask_wtf`. 

## Testing

You can run the flask app by setting the environment variable `FLASK_APP` to `run.py`.
Test out all of the forms, check that they are working properly. Ensure 
that all of the links for blog details and user details and going back to the home
page are working. Check that all of the blog post and user details that are
in the template are rendered.

Also, check that your database models are created correctly. Remember to define the
relationships between tables.

## Submissions & Grading

Make sure that you've tested parts of your website and that links to the frontpage
exist and are clearly visible, and then zip the `flask_app/` directory, and submit that zip
to the submit server. The submit server will not show test results, but just display "ACCEPTED".

Your project will be graded as follows:

- 5 pts - All blog posts visible on front page
- 10 pts - Blog post creation form is CSRF-protected and is processed correctly
- 10 pts - Comment creation form is CSRF-protected and is processed correctly 
- 5 pts - Links to a blog author's page work on index page.
- 5 pts - Links to a blog author's page work on post detail page.
- 15 pts - 5 pts for each correct route
- 15 pts - 5 pts for each correctly created `Model`
- 5 pts - Secret key created and set
- 5 pts - All required details for blog posts are visible on index page, and content synopsis
          is limited to 250 characters, and link to index page at `/` exists.
- 5 pts - All required details for blog posts are visible on user page, and content synopsis is
          limited to 250 characters, and link to index page at `/` exists
- 5 pts - All required details for comments and the current post are visible on post detail page.
- 5 pts - Redirects after a post requests to avoid the "resend data again?" prompt
- 5 pts - Dates formatted similarly to `September 01, 2019`.
- 5 pts - `__repr__` method implemented for each `Model`

The project will be graded out of a 100 points. You won't be graded for style, but make
sure your code is readable and clean, and well commented if you are
making a larger function




