"""
Hashing helper functions
"""

import hmac
from secret import SECRET


def hash_this(tohash):
    """returns hash from tohash"""
    return '%s|%s' % (tohash, hmac.new(SECRET, tohash).hexdigest())

def check_hash(tovalidate):
    """returns true if tovalidate matches hashed"""
    check = tovalidate.split('|')[0]
    if tovalidate == hash_this(check):
        return check
