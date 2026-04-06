from typing import Any, Tuple
import unittest

import pygame

from buttonup.utils import ColorTools
from tests.testing_tools import WillRaise


class TestColorTools(unittest.TestCase):
    def test_is_hex_recognizes_valid_and_invalid_strings(self):
        cases_and_expected: Tuple[Tuple[Any, bool], ...] = (
            ("#FFFFFF", True),
            ("FFFFFF", True),
            ("#ffffff", True),
            ("FFF", False),
            ("#GGGGGG", False),
            (123, False),
            (None, False),
        )

        for value, expected in cases_and_expected:
            with self.subTest(value=value):
                self.assertEqual(ColorTools.is_hex(value), expected)

    def test_is_rgb_validates_length_type_and_range(self):
        cases_and_expected: Tuple[Tuple[Any, bool], ...] = (
            ((255, 255, 255), True),
            ((0, 0, 0), True),
            ((-1, 0, 0), False),
            ((256, 0, 0), False),
            ((1, 2), False),
            ((1, 2, 3, 4), False),
            ((1.0, 2, 3), False),
            ([1, 2, 3], False),
            ("1,2,3", False),
        )

        for value, expected in cases_and_expected:
            with self.subTest(value=value):
                self.assertEqual(ColorTools.is_rgb(value), expected)

    def test_is_pygame_color_identifies_pygame_Color_instances(self):
        pg_col = pygame.Color(10, 20, 30, 40)
        self.assertTrue(ColorTools.is_pygame_color(pg_col))
        # other types should be False
        self.assertFalse(ColorTools.is_pygame_color((10, 20, 30)))
        self.assertFalse(ColorTools.is_pygame_color("#0A141E"))

    def test_is_color_is_union_of_supported_types(self):
        self.assertTrue(ColorTools.is_color("#ABCDEF"))
        self.assertTrue(ColorTools.is_color((1, 2, 3)))
        self.assertTrue(ColorTools.is_color(pygame.Color(1, 2, 3)))
        self.assertFalse(ColorTools.is_color(123))

    def test_to_hex_handles_strings_rgb_and_pygame_colors_and_errors(self):
        cases_and_expected = [
            ("#ffffff", "#FFFFFF"),
            ("ffffff", "FFFFFF"),
            ((255, 255, 255), "#FFFFFF"),
            ((15, 16, 17), "#0F1011"),
            (pygame.Color(1, 2, 3, 4), "#010203"),
            (None, WillRaise(TypeError)),
            ("#GGGGGG", WillRaise(TypeError)),
        ]

        for value, expected in cases_and_expected:
            with self.subTest(value=value):
                if isinstance(expected, WillRaise):
                    with self.assertRaises(expected.exception_type):
                        ColorTools.to_hex(value)
                else:
                    result = ColorTools.to_hex(value)
                    self.assertEqual(result, expected)

    def test_to_rgb_converts_hex_rgb_and_pygame_colors_and_raises_on_invalid(self):
        cases_and_expected = [
            ("#ffffff", (255, 255, 255)),
            ("ffffff", (255, 255, 255)),
            ("#0f1011", (15, 16, 17)),
            ((1, 2, 3), (1, 2, 3)),
            (pygame.Color(10, 20, 30, 40), (10, 20, 30)),
            (None, WillRaise(TypeError)),
            ("#GGGGGG", WillRaise(TypeError)),
            ("FFF", WillRaise(TypeError)),
        ]

        for value, expected in cases_and_expected:
            with self.subTest(value=value):
                if isinstance(expected, WillRaise):
                    with self.assertRaises(expected.exception_type):
                        ColorTools.to_rgb(value)
                else:
                    result = ColorTools.to_rgb(value)
                    self.assertEqual(result, expected)


