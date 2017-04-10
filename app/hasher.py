"""
Hashing helper functions
"""
from string import letters
import random
import hashlib

import hmac
from secret import SECRET

def gen_salt(length=8):
    """returns random 8 char string"""
    return ''.join(random.choice(letters) for x in xrange(length))

def hash_pw(username, password, salt=None):
    """returns hashed password"""
    if salt is None:
        salt = gen_salt()
    return hashlib.sha256(username + password + salt).hexdigest() + salt

def check_pw(username, password, hashed_pw):
    """returns true if valid"""
    salt = hashed_pw[-8:]
    return hashed_pw == hash_pw(username, password, salt)

def hash_this(tohash):
    """returns hash from tohash"""
    return '%s|%s' % (tohash, hmac.new(SECRET, tohash).hexdigest())

def check_hash(tovalidate):
    """returns true if tovalidate matches hashed"""
    check = tovalidate.split('|')[0]
    if tovalidate == hash_this(check):
        return check
