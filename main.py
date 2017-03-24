"""
mublog this will need a bit of refactoring to lint
"""
import os
import re
import json
from datetime import date

import webapp2
import jinja2
from google.appengine.ext import db

#from google.appengine.ext import ndb

sitewide_params = {'title':'MUBlog'}

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

class BlogPost(db.Model):
    """db blog post entity"""
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    author = db.StringProperty(required=True)
    likes = db.IntegerProperty(required=True)


class Author(db.Model):
    """db author entity"""
    pass


class Handler(webapp2.RequestHandler):
    """
    Handler is a helper class for parsing params and rendering templates
    """

    def write(self, *a, **kw):
        """ convience response"""
        self.response.out.write(*a, **kw)

    def parse_template(self, template, **params):
        """ convience render"""
        j_template = jinja_env.get_template(template)
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
        self.response.headers.add('AMP-Access-Control-Allow-Source-Origin', 'http://localhost:8080')
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
        self.response.out.write(json.dumps(params))


class MainPage(Handler):
    """
    MainPage Route Handler
    """

    def get(self):
        """ page get"""
        page = {'title':'Recent Headlines'}
        params = {'site':sitewide_params, 'page':page}
        self.render("list.html", params=params)


class NewpostPage(Handler):
    """
    NewpostPage Handler
    """

    def get(self):
        """ page get"""
        page = {'title':'Write a new post'}
        params = {'site':sitewide_params, 'page':page}
        self.render("newpost.html", params=params)

    def post(self):
        """page post"""
        params = {}
        subject = self.request.get('subject')
        content = self.request.get('content')
        if content and subject:
            params['error'] = False
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
        params = {'site':sitewide_params, 'page':page}
        self.render("editpost.html", params=params)


class LoginPage(Handler):
    """
    LoginPage Handler
    """

    def get(self):
        """ page get"""
        page = {'title':'Sign in to your account.'}
        params = {'site':sitewide_params, 'page':page}
        self.render("login.html", params=params)


class SignupPage(Handler):
    """
    SignupPage Handler
    """

    page = {'title':'Sign up for a free account!'}
    def get(self):
        """ page get"""
        params = {'site':sitewide_params, 'page':self.page}
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
    HopePage Handler
    """

    def get(self):
        """ main get"""
        page = {'title':'Your Blog Posts'}
        params = {'site':sitewide_params, 'page':page}
        self.render("login.html", params=params)

app = webapp2.WSGIApplication([
    (r'/', MainPage),
    (r'/newpost/?', NewpostPage),
    (r'/blog/?', MainPage),
    (r'/blog/([0-9]+)', EditpostPage),
    (r'/edit/?', MainPage),
    (r'/edit/([0-9]+)', MainPage),
    (r'/delete/([0-9]+)', MainPage),
    (r'/login/?', LoginPage),
    (r'/welcome/?', HomePage),
    (r'/signup/?', SignupPage),
    (r'/logout/?', MainPage),
], debug=True)
