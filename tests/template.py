import unittest
from buttonup.utils import ColorTools
from tests.testing_tools import WillRaise


class ColorTest(unittest.TestCase):
    def test_to_hex(self):
        cases_and_expected = [
            ("#FFFFFF", "#FFFFFF"),
            ((255, 255, 255), "#FFFFFF"),
            (None, WillRaise(TypeError)),
        ]

        for value, expected in cases_and_expected:
            with self.subTest(value=value):
                if isinstance(expected, WillRaise):
                    with self.assertRaises(expected.exception_type):
                        ColorTools.to_hex(value)
                else:
                    result = ColorTools.to_hex(value)
                    self.assertEqual(result, expected)


