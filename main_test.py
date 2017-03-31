"""
Holy shit! Google app engine made local unit testing a pain
ImportError: No module named appengine.ext
so I'm flying blind on many parts
"""
import unittest
#import main
from app.helpers.hasher import gen_salt, hash_this, check_hash

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

    def test_salt_len_8(self):
        """salt len equal 8"""
        self.assertEqual(len(gen_salt()), 8)

    def test_hash_this_len_72(self):
        """hash_this returns str len 72"""
        test_str = 'test string * stuff'
        test_hash = hash_this(test_str)
        self.assertEqual(len(test_hash), 72)

    def test_check_hash_for_true(self):
        """check_hash returns true when match"""
        test_str = 'test string * stuff'
        test_hash = hash_this(test_str)
        self.assertTrue(check_hash(test_str, test_hash))

    def test_check_hash_for_false(self):
        """check_hash returns false when no match"""
        test_str = 'test string * stuff'
        test_hash = hash_this(test_str)
        self.assertFalse(check_hash("false case", test_hash))

if __name__ == '__main__':
    unittest.main()
