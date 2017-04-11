"""
mublog
    this version only addresses the user login and auth
    other routes will or requests will set to serve
"""

import datetime
import json
import os
import re
import ssl

import webapp2
import jinja2
from google.appengine.ext import db
from app.hasher import hash_this, check_hash
from app.entities import AuthorEntity


# current host url for cors
CURRENT_HOST = """http://localhost:8080, https://localhost:8080,
                  https://fsnd-2.appspot.com, https://fsnd-2.appspot.com/newpost"""

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
        secure_cookie = hash_this(cookie_val)
        self.response.headers.add('Set-Cookie', '%s=%s; Path=/' % (cookie_name, secure_cookie))

    def read_secure_cookie(self, cookie_name):
        """reads the cookie"""
        cookie_val = self.request.cookies.get(cookie_name)
        return cookie_val and check_hash(cookie_val)

    def login(self, user):
        """login"""
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        """logout"""
        self.response.headers.add('Set-Cookie', 'user_id=; Path=/')

    def xhr_json(self, params):
        """ handles the json stuff
                adds cors for json post requests
            params will be json dumped
            params.error
                if error: will respond with 400
                error can be used for a message
        """
        self.response.headers.add('Access-Control-Allow-Origin', CURRENT_HOST)
        self.response.headers.add('Access-Control-Expose-Headers',
                                  'AMP-Access-Control-Allow-Source-Origin, AMP-Redirect-To')
        self.response.headers.add('Access-Control-Allow-Credentials', 'true')
        self.response.headers.add('Access-Control-Allow-Headers',
                                  'Origin, X-Requested-With, Content-Type, Accept')
        #self.response.headers.add('AMP-Access-Control-Allow-Source-Origin', CURRENT_HOST)
        self.response.headers['AMP-Same-Origin'] = 'true'
        self.response.headers['AMP-Access-Control-Allow-Source-Origin'] = 'http://localhost:8080'
        self.response.headers['TURD-Face'] = 'poop-header'
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
        if params['error']:
            self.response.set_status(400)
            self.response.out.write(json.dumps(params))
        elif params['redirect']:
            self.response.headers['AMP-Redirect-To'] = params['redirect']
            #self.redirect(params['redirect'])

# controllers

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

    page = {'subject':"Sign up! It's pretty sweet!"}
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
            redirect = 'http://localhost:8080/login/'
        else:
            error = "there are plenty of problems"
            redirect = ''
        params = {}
        params['username'] = username
        params['password'] = password
        params['error'] = error
        params['redirect'] = redirect
        self.xhr_json(params)


class WelcomePage(Handler):
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
"""

app = webapp2.WSGIApplication([
    (r'/login/?', LoginPage),
    (r'/welcome/?', WelcomePage),
    (r'/signup/?', SignupPage)
], debug=True)

