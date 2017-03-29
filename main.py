"""
mublog
    This will probably be stuck with the old nasty monolith structure until I have
    some refactor time. It should have been a q/d project but ended up just dirty.
    I think appengine datastore is alright, but I wouldn't have made these choices
    without a project specifying them. It's nice to be exposed to different things.
"""

import datetime
import hashlib
import json
import os
import random
import re
import ssl
import string
from secret import SECRET

import webapp2
import jinja2
from google.appengine.ext import db

#  jinja2 Environment constants
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)

#sitewide contsants (modelish)
SITEWIDE_PARAMS = {'title':'MUBlog'}

"""
Hashing helper functions
"""
def gen_salt():
    """returns 8 letter string"""
    return ''.join(random.choice(string.letters) for x in xrange(8))

def hash_this(tohash, salt=None):
    """returns hash + salt from tohash"""
    if salt is None:
        salt = gen_salt()
    return hashlib.sha256(str(tohash) + SECRET + salt).hexdigest() + salt

def check_hash(tovalidate, hashed):
    """returns true if tovalidate matches hashed"""
    salt = hashed[-8:]
    check = hash_this(tovalidate, salt)
    return hashed == check


"""
start models
"""

class PostEntity(db.Model):
    """ db blog post entity
        properties
            subject: blog post title
            content: blog post body
            created: timestamp in normal y-m-d h:m:s
            author: author username
            likes: number of likes
    """
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(required=True)
    author = db.StringProperty(required=True)
    likes = db.IntegerProperty(required=True)
    # liked_by = db.StringListProperty(required=True) # could be child entity


class AuthorEntity(db.Model):
    """ db author entity
        properties
            username: unique string
            username_lc: unique string lowercase version of username
            password: hashed pass + SECRET + salt
            email: optional email address
    """
    username = db.StringProperty(required=True)
    username_lc = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()

class LikeEntity(db.Model):
    """ like entity keeps track of individual likes
        ReferenceProperty for PostEntity
        Must have AuthorEntity id and username as well
        properties
            parent = PostEntity id
    """
    for_post = db.ReferenceProperty(PostEntity, collection_name="likes")
    author = db.ReferenceProperty(AuthorEntity, collection_name="likes")
    author_username = db.StringProperty(required=True) # for quick reference only


class CommentEntity(db.Model):
    """ db comments
        properties
    """
    coment_text = db.TextProperty(required=True)
    for_post = db.ReferenceProperty(PostEntity, collection_name="comments")
    author = db.ReferenceProperty(AuthorEntity, collection_name="comments")
    author_username = db.StringProperty(required=True) # for quick reference only


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

    def xhr_json(self, params):
        """ handles the json shtuff
                adds cors for json post requests
            params will be json dumped
            params.error
                if error: will respond with 400
                error can be used for a message
        """
        self.response.headers.add('Access-Control-Allow-Origin', '*')
        self.response.headers.add('AMP-Access-Control-Allow-Source-Origin',
                                  'http://localhost:8080, https://localhost:8080')
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
        permalink = post_time_stamp.strftime('%s')

        if content and subject:
            params['error'] = False
            blog_posts = PostEntity(permalink=permalink,
                                    subject=subject,
                                    content=content,
                                    created=post_time_stamp,
                                    author="testuser",
                                    likes=0,
                                    liked_by=["testuser"])
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

