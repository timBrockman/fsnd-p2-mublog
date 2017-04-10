"""
start models - uses no reference properties
extend db.Model
  AuthorEntity
"""
from hasher import hash_this, check_hash
from google.appengine.ext import db

class AuthorEntity(db.Model):
    """ db author entity

        :param username: unique string
        :param pw_hash: hashed (pass + SECRET + salt)
        :param email: optional email address
        classmethod
            read_by_id
            read_my_name
            register (create)
            login
    """
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.EmailProperty()

    @classmethod
    def read_by_id(cls, uid):
        """convienient get_by_id method"""
        return AuthorEntity.get_by_id(uid)

    @classmethod
    def read_my_name(cls, username):
        """convienient filter by username method"""
        return AuthorEntity.all().filter('username =', username).get()

    @classmethod
    def register(cls, username, password, email):
        """creates new user (doesn't check if one exsist)"""
        pw_hash = hash_this(password)
        return AuthorEntity(username=username, password=pw_hash, email=email)

    @classmethod
    def login(cls, username, password):
        """logs in user if credentials check out"""
        pass

