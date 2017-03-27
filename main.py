"""
mublog
    this will probably never lint and be stuck with the old nasty
    webapp2 reccommended monolith structure
"""

import datetime
import json
import os
import re
import ssl

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
            liked_by: list of strings of usernames
    """
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(required=True)
    author = db.StringProperty(required=True)
    likes = db.IntegerProperty(required=True)
    liked_by = db.StringListProperty(required=True)


class AuthorEntity(db.Model):
    """ db author entity
        properties
            username: unique string
            password: hashed pass
            email: optional email address
            maybe blogposts: StringListProperty of permalinks
            maybe likes: StringListProperty of liked permalinks
    """
    pass

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
        """posts = db.GqlQuery("SELECT * FROM PostEntity ORDER BY created DESC ")"""
        posts = PostEntity.all().order('-created')
        page = {'title':'Recent Headlines'}
        params = {'site':SITEWIDE_PARAMS, 'page':page, 'posts':posts}
        self.render("list.html", params=params)


class SinglepostPage(Handler):
    """
    Single blog post Handler
    """
    def get(self, post_id):
        """page get"""
        current_post = PostEntity.get_by_id(post_id)
        params = {'site':SITEWIDE_PARAMS, 'current_post':current_post}
        self.render("single.html", params=params)

class NewpostPage(Handler):
    """
    NewpostPage Handler
    """

    def get(self):
        """ page get"""
        page = {'title':'Write a new post'}
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
        page = {'title':title,
                'permalink':permalink}
        params = {'site':SITEWIDE_PARAMS, 'page':page}
        self.render("editpost.html", params=params)


class LoginPage(Handler):
    """
    LoginPage Handler
    """

    def get(self):
        """ page get"""
        page = {'title':'Sign in to your account.'}
        params = {'site':SITEWIDE_PARAMS, 'page':page}
        self.render("login.html", params=params)


class SignupPage(Handler):
    """
    SignupPage Handler
    """

    page = {'title':'Sign up for a free account!'}
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
        page = {'title':'Your Blog Posts'}
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

