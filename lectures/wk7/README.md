# Week 7
### Flask Talisman

This week we'll be looking at a very minimal `Flask` application. It has only
a `Index` and `About` page, and only the `flask_talisman` extension configured.
`flask_talisman` is a small extension, implemented in just 334 (significant) lines
of code. It allows us to more easily set security headers.

Most of the content for this week is in the slides which are linked on Piazza. 

To run the code, make sure to `pip install Flask flask-talisman`.

In `__init__.py`, we add an import statement for `flask_talisman` at the top of the file

`__init__.py`:
```py
from flask import Flask
from flask_talisman import Talisman
```

We setup the configuration of the `app` object the normal way. We don't have to
configure a secret key in this case because `flask_talisman` does not require it
to work. Remember that if you are using `WTForms`, you will need to set the
secret key or the CSRF tokens will not be generated, and you'll simply
get an error when the website is run. 

There are several security headers we discussed in the slides, and by default, 
`flask_talisman` sets all of them. Simply adding the line `Talisman(app)`
to `__init__.py` enables the following:

**Note:** We'll be looking at the `Content-Security-Policy` (CSP) header in detail
further down.

- All connects to be through HTTPS (except localhost)
- `Flask` session cookie set to `secure`, so it can only be sent with an HTTPS request
  - Still **do not** add sensitive information to the cookie
- Sets the session cookie be `httponly`, disallowing the JavaScript `Document.cookie` API from
  accessing your cookie. This helps mitigate XSS attacks.
- Sets `X-Frame-Options` to `'SAMEORIGIN'` to prevent clickjacking, which is where 
  an external website can embed your webpage in an `iframe` HTML tag, and then trick
  you into clicking on things you didn't mean to click on.
  When set to `'SAMEORIGIN'`, only frames embedding the same page they are on are allowed.
- Sets `X-XSS-Protection`. Not really needed if a strong CSP is employed.
- Sets `X-Content-Type-Options`, to enforce media types to be obeyed, and prevent non-executable
  types from being turned into executable ones.
- Sets `X-Download-Options` to tell browser to not allow opening a downloaded file
  in the browser, only really useful for **Internet Explorer**.
- Sets `Content-Security-Policy` to `default-src: 'self'`, meaning we only allow loading content
  from sources with the same host, port, and protocol. This is rather restrictive; 
  what if we want to embed a YouTube video or retrieve audio files we might have stored on a 
  different database? We'll go over how to set your own policies below.
- Sets the `Referrer-Policy` to `strict-origin-when-cross-origin`, meaning we send no
  header with a reference back to our website if we are navigating, through a link, to
  a less secure website.

You **do not** need to know the specifics of what all these headers do. You *should know*
how web app attacks work and how to protect against them, and `flask_talisman` helps
us with protecting our app.

To enable `flask_talisman`, we simply add it to our `__init__.py` like so:

`__init__.py`:
```py
from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app)
```

By default, the `Content-Security-Policy` is set to `default-src: 'self'`, which just
means that we only allow loading resources from sources that have the same host, same port, 
and same protocol (HTTP vs. HTTPS).
This is restrictive, but ensures that the client does not load any malicious code. 

**Note:** `'self'` excludes subdomains of your site.

We can make this explicit with the following code. We define our policy using a dictionary,
and then pass the dictionary as an argument to the `content_security_policy=` keyword
parameter of `Talisman()`.

**Example 1:**
```py
csp = {
    'default-src': '\'self\''
}

Talisman(app, content_security_policy=csp)
```

Now our site accepts resources only from the same origin. To check that we actually
have `flask_talisman` protection enabled, we can use `cURL` to make a simple `GET` request
to the front page of our website. Here are the results:

![curl output][headers]

From now on, we'll omit the last line and just show the security policy dictionary.

**Example 2:**
```py
csp = {
    'default-src': [
        '\'self\'',
        '*.trusted.com'
    ]
}
```

And now our application will only accept resources loaded from the same origin
or from `trusted.com` and `trusted.com`'s subdomains.

**Example 3:**
```py
csp = {
    'default-src': '\'self\'',
    'img-src': '*',
    'media-src': ['media1.com', 'media2.com'],
    'script-src': 'userscripts.example.com'
}
```

Here, you allow your users to include images from anywhere in their content.
Images are distinguished by the `img` HTML tag. We restrict the sources of
audio, video, and subtitle files using the `'media-src'` directive to
`'media1.com'`,`'media2.com'`, and our own site. We don't allow media to be loaded
from the subdomains of these three hosts. Finally, we only allow scripts from 
`'userscripts.example.com'` and our own site. 

**Example 4:**
```py
csp = {
    'default-src': 'https://onlinebanking.jumbobank.com'
}
```

This policy only allows loading resources over HTTPS from the given source. If you
want to ensure that all of your content is only loaded using SSL, so that
no one can eavesdrop on requests that users are making, you would just
have to add in the `https` url for your site.

**Example 5:**
```py
csp = {
    'default-src': [
        '\'self\'',
        '*.mailsite.com'
    ]
    'img-src': '*'
}
```

We allow images from all sources, and all other content must come from the
same origin as your site, or from `'*.mailsite.com'`.

How can you **test** your policies? You can set the `report_uri=` keyword parameter
when you are initializing `Talisman()`. The browser, after detecting a `Content-Security-Policy`
violation, will `POST` to the report_uri. 

Let's say our website is hosted at `http://example.com/`.

In `__init__.py`, we setup the CSP and report_uri:
```py
csp = {
    'default-src': [
        '\'self\'',
        '*.mailsite.com'
    ]
    'img-src': '*'
    'style-src': 'cdn.example.com'
}

Talisman(
    app, 
    content_security_policy=csp, 
    content_security_policy_report_uri='https://mywebsite.com/csp_reports'
)
```

The content security policy is the same as the one in example 5, but with the
added restriction that stylesheets can only come from `'cdn.example.com'`. Let's
say we create a signup HTML page, and it looks roughly like this:

`signup.html`
```html
<!DOCTYPE html>
<html>
  <head>
    <title>Sign Up</title>
    <link rel="stylesheet" href="css/style.css">
  </head>
  <body>
    ... Content ...
  </body>
</html>
```

But, this page violates our CSP. The line `<link rel="stylesheet" href="css/style.css">`
tries to load a stylesheet from the same origin as our site, when we specified in the CSP
that stylesheets can only come from `'cdn.example.com'`. The browser will send a `POST`
request to `'https://mywebsite.com/csp_reports'`, the report_uri, with a JSON document
that looks like this:

**CSP violation report:**
```json
{
  "csp-report": {
    "document-uri": "http://example.com/signup.html",
    "referrer": "",
    "blocked-uri": "http://example.com/css/style.css",
    "violated-directive": "style-src cdn.example.com",
    "original-policy": "default-src 'none'; style-src cdn.example.com; report-uri /_/csp-reports"
  }
}
```

Finally, what if we want to configure `flask_talisman` on a view-by-view basis? Maybe
we want to allow certain parts of our website to be embeddable, maybe an informational page.
This would allow other websites to embed our informational page on their website using 
the `<iframe>`, allowing users of those other websites to see info about our website
without having to navigate separately to our website.

To enable embedding on an `about()` view function, we add the `@talisman()` decorator,
specifying `frame_option=ALLOW_FROM`. Then we also have to specify
`frame_options_allow_from='https://trusteddomain.com/'`, and `flask_talisman` will set
the corresponding security header to allow `'https://trusteddomain.com/'` to embed our
`/about` page on their website.

```py
@app.route('/about')
@talisman(frame_options=ALLOW_FROM, frame_options_allow_from='https://trusteddomain.com/')
def about():
    return render_template('about.html')
```

### Conclusion

This lecture was mostly about security headers and how to configure them using
the `flask_talisman` API.

Many of the examples were taken from the MDN CSP documentation; the link to the page is below.

There are more configuration options:

![Talisman init_app() source][source]

... but you won't be asked to remember how to set them in code. You should
remember how to create a `Content-Security-Policy`.

To understand more about security headers, content security policies, and
`flask_talisman`:

[MDN Security Headers Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)

[MDN CSP Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)

[MDN CSP directives](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy)

[Flask-Talisman README](https://github.com/GoogleCloudPlatform/flask-talisman#talisman-http-security-headers-for-flask)

[Flask-Talisman source code](https://github.com/GoogleCloudPlatform/flask-talisman/blob/master/flask_talisman/talisman.py)


[headers]: ./images/headers.png "Security Headers Image view"
[source]: ./images/talisman_config.png "Talisman config options"