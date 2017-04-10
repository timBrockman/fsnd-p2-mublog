"""
Google app engine made local unit testing a pain
ImportError: No module named appengine.ext
so I'm flying blind on many parts
"""
import unittest
#import main
from app.hasher import hash_this, check_hash

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
