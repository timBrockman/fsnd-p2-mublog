#!/usr/bin/env python
''' mostly copy-pasta'd from:
https://github.com/GoogleCloudPlatform/appengine-guestbook-python/blob/master/e2e/test_e2e.py
then slightly modified to fit this project
more extensive tests should be written
should be pep8'd
'''

import uuid
import os
import requests

URL = os.environ.get('MUBLOG_URL')


def test_e2e():
    '''
    tests basic mublog functions
        prints Success if everything works
    '''
    assert URL
    print "Running test against {}".format(URL)
    req = requests.get(URL)
    assert b'Blog' in req.content
    uuid_handle = uuid.uuid4()
    data = {'content': str(uuid_handle)}
    req = requests.post(URL + '/signup', data)
    assert req.status_code == 200
    req = requests.get(URL)
    assert str(uuid_handle).encode('utf-8') in req.content
    print "Success"

if __name__ == "__main__":
    test_e2e()
