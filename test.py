import unittest
from unittest import TestCase
from app import calc, divide


class TestStringMethods(TestCase):
    def test_calc(self):
        self.assertEqual(calc(1,2), 3)

    def test_divide(self):
        self.assertEqual(divide(1,0), 2)
        with self.assertRaises(ValueError):
            print(ValueError)

if __name__ == '__main__':
    tests = TestStringMethods()
    tests.test_calc()
