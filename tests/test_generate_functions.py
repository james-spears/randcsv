import unittest
from randcsv import value_generators as vg

class TestGenerateString(unittest.TestCase):

    def test_output_length(self):
        value = vg.generate_string(4)
        self.assertEqual(len(str(value)), 4)
        value = vg.generate_string(5)
        self.assertEqual(len(str(value)), 5)
        value = vg.generate_string(6)
        self.assertEqual(len(str(value)), 6)

        with self.assertRaises(ValueError):
            vg.generate_string(-1)


class TestGenerateInteger(unittest.TestCase):

    def test_output_length(self):
        value = vg.generate_integer(4)
        self.assertEqual(len(str(value)), 4)
        value = vg.generate_integer(5)
        self.assertEqual(len(str(value)), 5)
        value = vg.generate_integer(6)
        self.assertEqual(len(str(value)), 6)

        with self.assertRaises(ValueError):
            vg.generate_integer(-1)


class TestGenerateFloat(unittest.TestCase):

    def test_output_length(self):
        value = vg.generate_float(4)
        self.assertEqual(len(str(value)), 4)
        value = vg.generate_float(5)
        self.assertEqual(len(str(value)), 5)
        value = vg.generate_float(6)
        self.assertEqual(len(str(value)), 6)

        with self.assertRaises(ValueError):
            vg.generate_float(-1)

