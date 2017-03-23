"""
mublog this will need a bit of refactoring to lint
"""
import os
from datetime import date

import webapp2
import jinja2

#from google.appengine.ext import ndb
sitewide_params = {'title':'MUBlog'}

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    """
    Handler is a convience class for parsing params and rendering templates
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

    def get(self):
        """ page get"""
        page = {'title':'Sign up for a free account!'}
        params = {'site':sitewide_params, 'page':page}
        self.render("signup.html", params=params)


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
