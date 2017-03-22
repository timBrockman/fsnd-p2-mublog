import os
from datetime import date

import webapp2
import jinja2

#from google.appengine.ext import ndb
#will be config
sitewide_params = {'title':'MUBlog'}

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def parse_template(self, template, **params):
        j_template = jinja_env.get_template(template)
        return j_template.render(params)

    def render(self, template, **kw):
        self.write(self.parse_template(template, **kw))

class MainPage(Handler):
    def get(self):
        page = {'title':'Recent Headlines'}
        params = {'site':sitewide_params, 'page':page}
        self.render("list.html", params=params)

class NewpostPage(Handler):
    def get(self):
        page = {'title':'Write a new post'}
        params = {'site':sitewide_params, 'page':page}
        self.render("newpost.html", params=params)

class LoginPage(Handler):
    def get(self):
        page = {'title':'Sign in to your account.'}
        params = {'site':sitewide_params, 'page':page}
        self.render("login.html", params=params)

class SignupPage(Handler):
    def get(self):
        page = {'title':'Sign up for a free account!'}
        params = {'site':sitewide_params, 'page':page}
        self.render("signup.html", params=params)

class HomePage(Handler):
    def get(self):
        page = {'title':'Your Blog Posts'}
        params = {'site':sitewide_params, 'page':page}
        self.render("login.html", params=params)

app = webapp2.WSGIApplication([
    (r'/', MainPage),
    (r'/newpost/?', NewpostPage),
    (r'/blog/?', MainPage),
    (r'/blog/(\d+)', MainPage),
    (r'/edit/(\d+)', MainPage),
    (r'/delete/(\d+)', MainPage),
    (r'/login/?', LoginPage),
    (r'/welcome/?', HomePage),
    (r'/signup/?', SignupPage),
    (r'/logout/?', MainPage),
], debug=True)