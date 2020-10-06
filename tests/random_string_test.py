import unittest
from randcsv import main

class TestRandomString(unittest.TestCase):

    def test_random_string(self):
        value = main.random_string()
        self.assertEqual(len(str(value)), 6)
