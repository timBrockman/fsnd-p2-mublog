"""
Hashing helper functions
"""

import hashlib
import random
import string
from secret import SECRET


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
