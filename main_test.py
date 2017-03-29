# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import main


'''def test_get():
    """basic get test"""
    app = webtest.TestApp(main.app)
    response = app.get('/')
    assert response.status_int == 200
'''

class HashesTestCase(unittest.TestCase):
    """test cases for hash functions"""
    def hash_functions_should(self):
        """test the hash helper functions"""
        # salt len equal 8
        self.assertEqual(len(main.gen_salt()), 8)
        # hash_this returns str len 72
        test_str = 'test string * stuff'
        test_hash = main.hash_this(test_str)
        self.assertEqual(len(test_hash), 72)
        # check_hash returns true when should else none
        self.assertEqual(main.check_hash(test_str, test_hash), True)
        self.assertEqual(main.check_hash("false case", test_hash), None)

if __name__ == '__main__':
    unittest.main()
