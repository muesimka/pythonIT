import unittest

from app import calc, divide


class TestStringMethods(unittest.TestCase):
    def test_calc(self):
        self.assertEqual(calc(1, 2), 3)

    def test_divide(self):
        self.assertEqual(divide(4, 2), 2)
        with self.assertRaises(ValueError):
            divide(1, 0)


if __name__ == '__main__':
    unittest.main()
