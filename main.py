"""
mublog
    This will probably be stuck with the old nasty monolith structure until I have
    some refactor time. It should have been a q/d project but ended up just dirty.
    I think appengine datastore is alright, but I wouldn't have made these choices
    without a project specifying them. It's nice to be exposed to different things.
"""

import datetime
import json
import os
import re
import ssl

import webapp2
import jinja2
from google.appengine.ext import db
from app.hasher import gen_salt, hash_this, check_hash
from app.entities import   PostEntity, AuthorEntity, LikeEntity, CommentEntity


# current host url for cors
CURRENT_HOST = "http://localhost:8080, https://localhost:8080, https://fsnd-2.appspot.com/"

# jinja2 Environment constants
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)

# sitewide constants (modelish)
SITEWIDE_PARAMS = {'title':'MUBlog'}



"""
start handlers
"""

class Handler(webapp2.RequestHandler):
    """
    Handler is a helper class for parsing params and rendering templates
    """

    def write(self, *a, **kw):
        """ convience response"""
        self.response.out.write(*a, **kw)

    def parse_template(self, template, **params):
        """ convience render"""
        j_template = JINJA_ENV.get_template(template)
        return j_template.render(params)

    def render(self, template, **kw):
        """ convience write parse"""
        self.write(self.parse_template(template, **kw))

    def set_secure_cookie(self, cookie_name, cookie_val):
        """sets a hashed cookie"""
        pass

    def read_secure_cookie(self):
        """reads the cookie"""
        pass

    def login(self):
        """login"""
        pass

    def logout(self):
        """logout"""
        pass

    def xhr_json(self, params):
        """ handles the json shtuff
                adds cors for json post requests
            params will be json dumped
            params.error
                if error: will respond with 400
                error can be used for a message
        """
        self.response.headers.add('Access-Control-Allow-Origin', '*')
        self.response.headers.add('AMP-Access-Control-Allow-Source-Origin', CURRENT_HOST)
        self.response.headers.add('Access-Control-Expose-Headers',
                                  'AMP-Access-Control-Allow-Source-Origin, AMP-Redirect-To')
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers.add('Access-Control-Allow-Headers',
                                  'Origin, X-Requested-With, Content-Type, Accept')
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
        if params['error']:
            self.response.set_status(400)
        elif params['redirect']:
            self.response.headers.add('AMP-Redirect-To', params['redirect'])
            self.redirect(params['redirect'])
        self.response.out.write(json.dumps(params))

# controllers

class MainPage(Handler):
    """
    MainPage Route Handler
    """
    def get(self):
        """ page get"""
        posts = PostEntity.all().order('-created')
        page = {'subject':'Recent Headlines'}
        params = {'site':SITEWIDE_PARAMS, 'page':page, 'posts':posts}
        self.render("list.html", params=params)


class SinglepostPage(Handler):
    """
    Single blog post Handler
    """
    def get(self, post_id):
        """page get"""
        current_post = PostEntity.get_by_id(int(post_id))
        params = {'site':SITEWIDE_PARAMS, 'page':current_post}
        self.render("single.html", params=params)

class NewpostPage(Handler):
    """
    NewpostPage Handler
    """

    def get(self):
        """ page get"""
        page = {'subject':'Write a new post'}
        params = {'site':SITEWIDE_PARAMS, 'page':page}
        self.render("newpost.html", params=params)

    def post(self):
        """page post"""
        params = {}
        subject = self.request.get('subject')
        content = self.request.get('content')
        post_time_stamp = datetime.datetime.now()

        if content and subject:
            params['error'] = False
            blog_posts = PostEntity(subject=subject,
                                    content=content,
                                    created=post_time_stamp,
                                    author="testuser",
                                    like_total=0)
            blog_posts.put()
            params['redirect'] = 'https://localhost:8080/' # blog/' + str(post.key().id())
        else:
            params['error'] = "The subject and content are both required."
        params['subject'] = subject
        params['content'] = content
        self.xhr_json(params)

class EditpostPage(Handler):
    """
    EditpostPage Handler
    """

    def get(self, post_id):
        """ page get"""
        title = 'Edit post ' + post_id
        permalink = '/blog/'+ post_id
        page = {'subject':title,
                'permalink':permalink}
        params = {'site':SITEWIDE_PARAMS, 'page':page}
        self.render("editpost.html", params=params)


class LoginPage(Handler):
    """
    LoginPage Handler
    """

    def get(self):
        """ page get"""
        page = {'subject':'Sign in to your account.'}
        params = {'site':SITEWIDE_PARAMS, 'page':page}
        self.render("login.html", params=params)


class SignupPage(Handler):
    """
    SignupPage Handler
    """

    page = {'subject':'Sign up for a free account!'}
    def get(self):
        """ page get"""
        params = {'site':SITEWIDE_PARAMS, 'page':self.page}
        self.render("signup.html", params=params)

    def post(self):
        """ handle ajax signup form submission"""
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")

        if username and password and (password == verify):
            error = False
        else:
            error = "there are plenty of problems"
        params = {}
        params['username'] = username
        params['password'] = password
        params['error'] = error
        self.xhr_json(params)


class HomePage(Handler):
    """
    HomePage Handler
    """

    def get(self):
        """ main get"""
        page = {'subject':'Your Blog Posts'}
        params = {'site':SITEWIDE_PARAMS, 'page':page}
        self.render("login.html", params=params)

"""
start simple router
    (this will never lint)
"""

app = webapp2.WSGIApplication([
    (r'/', MainPage),
    (r'/newpost/?', NewpostPage),
    (r'/blog/?', MainPage),
    (r'/blog/([0-9]+)', SinglepostPage),
    (r'/edit/?', MainPage),
    (r'/edit/([0-9]+)', EditpostPage),
    (r'/delete/([0-9]+)', MainPage),
    (r'/login/?', LoginPage),
    (r'/welcome/?', HomePage),
    (r'/signup/?', SignupPage),
    (r'/logout/?', MainPage),
], debug=True)

