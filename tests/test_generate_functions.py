import unittest
from randcsv import main

class TestGenerateString(unittest.TestCase):

    def test_output_length(self):
        value = main.generate_string()
        self.assertEqual(len(str(value)), 6)


class TestGenerateInteger(unittest.TestCase):

    def test_output_length(self):
        value = main.generate_integer()
        self.assertEqual(len(str(value)), 6)


class TestGenerateFloat(unittest.TestCase):

    def test_output_length(self):
        value = main.generate_float()
        self.assertEqual(len(str(value)), 7)

