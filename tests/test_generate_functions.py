import unittest
from randcsv import main

class TestGenerateString(unittest.TestCase):

    def test_output_length(self):
        value = main.generate_string(4)
        self.assertEqual(len(str(value)), 4)
        value = main.generate_string(5)
        self.assertEqual(len(str(value)), 5)
        value = main.generate_string(6)
        self.assertEqual(len(str(value)), 6)

        with self.assertRaises(ValueError):
            main.generate_string(-1)


class TestGenerateInteger(unittest.TestCase):

    def test_output_length(self):
        value = main.generate_integer(4)
        self.assertEqual(len(str(value)), 4)
        value = main.generate_integer(5)
        self.assertEqual(len(str(value)), 5)
        value = main.generate_integer(6)
        self.assertEqual(len(str(value)), 6)

        with self.assertRaises(ValueError):
            main.generate_integer(-1)


class TestGenerateFloat(unittest.TestCase):

    def test_output_length(self):
        value = main.generate_float(4)
        self.assertEqual(len(str(value)), 4)
        value = main.generate_float(5)
        self.assertEqual(len(str(value)), 5)
        value = main.generate_float(6)
        self.assertEqual(len(str(value)), 6)

        with self.assertRaises(ValueError):
            main.generate_float(-1)

