"""
start models - uses no reference properties
extend db.Model
  AuthorEntity
"""
from hasher import hash_pw, check_pw
from google.appengine.ext import db

class AuthorEntity(db.Model):
    """ db author entity

        :param username: unique string
        :param pw_hash: hashed (pass + SECRET + salt)
        :param email: optional email address
        classmethod
            read_by_id
            read_by_name
            register (create)
            login
    """
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.EmailProperty()

    @classmethod
    def read_by_id(cls, uid):
        """convienient get_by_id method"""
        return AuthorEntity.get_by_id(uid)

    @classmethod
    def read_by_name(cls, username):
        """convienient filter by username method"""
        return AuthorEntity.all().filter('username =', username).get()

    @classmethod
    def register(cls, username, password, email):
        """creates new user (doesn't check if one exsist)"""
        pw_hash = hash_pw(username, password)
        return AuthorEntity(username=username, pw_hash=pw_hash, email=email)

    @classmethod
    def login(cls, username, password):
        """returns user obj if credentials check out"""
        user = cls.read_by_name(username)
        if user and check_pw(username, password, user.pw_hash):
            return user

