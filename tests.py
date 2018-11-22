import unittest
from bot_functions import number_to_unicode


class telegramBotFunctionTests(unittest.TestCase):

    def test_single_number(self):
        self.assertEqual(number_to_unicode(1), '1️⃣')

    def test_zero(self):
        self.assertEqual(number_to_unicode(0), '0️⃣')

    def test_multiple_numbers(self):
        self.assertEqual(number_to_unicode(123), '1️⃣2️⃣3️⃣')

    def test_string_instead_of_number(self):
        # Function should throw an Error if we give something different than a number
        with self.assertRaises(TypeError):
            number_to_unicode('abc')


if __name__ == '__main__':
    unittest.main()
