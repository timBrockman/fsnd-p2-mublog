"""
Google app engine made local unit testing a pain
ImportError: No module named appengine.ext
so I'm flying blind on many parts
"""
import unittest
#import main
from app.hasher import gen_salt, hash_pw, check_pw, hash_this, check_hash

'''class SanityTest(unittest.TestCase):
    """testing sanity"""
    def setUp(self):
        pass

    def test_true_eq_true(self):
        """crazy?"""
        self.assertEqual(True, True)
'''

class HashesTestCase(unittest.TestCase):
    """test cases for hash functions"""

    def setUp(self):
        pass

    #pw hashers
    def test_gen_salt(self):
        """gen_salt() returns str len 8"""
        self.assertEqual(len(gen_salt()), 8)

    def test_hash_pw(self):
        """hash_pw returns str len 72"""
        test_hashed_pw = hash_pw('bob', 'test pw')
        self.assertEqual(len(test_hashed_pw), 72)

    def test_check_pw_true(self):
        """check_pw() returns true when it should"""
        test_hashed_pw = hash_pw('bob', 'test pw')
        self.assertTrue(check_pw('bob', 'test pw', test_hashed_pw))

    def test_check_pw_false(self):
        """check_pw() returns false when it should"""
        test_hashed_pw = hash_pw('bob', 'test pw')
        self.assertFalse(check_pw('bob', 'bad pw', test_hashed_pw))

    #cookie hashers
    def test_hash_this_len_32(self):
        """hash_this returns str len 32"""
        test_str = 'test string * stuff'
        test_hash = hash_this(test_str)
        self.assertEqual(len(test_hash.split('|')[1]), 32)

    def test_check_hash_for_true(self):
        """check_hash returns test_str when checked"""
        test_str = 'test string * stuff'
        test_hash = hash_this(test_str)
        self.assertEqual(test_str, check_hash(test_hash))

if __name__ == '__main__':
    unittest.main()
