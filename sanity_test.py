import unittest

class SanityTest(unittest.TestCase):
    def setUp(self):
        pass
    def test_true_eq_true(self):
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
