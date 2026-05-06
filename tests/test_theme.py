import unittest
from pathlib import Path

import pygame

from buttonup import theme as theme_module
from buttonup.theme import Theme
from tests.testing_tools import WillRaise


class TestThemeModule(unittest.TestCase):
    def test_get_file_name_returns_path_inside_themes_dir(self):
        path = theme_module._get_file_name("dark")
        self.assertIsInstance(path, Path)
        self.assertTrue(str(path).endswith("themes\\dark.json") or str(path).endswith("themes/dark.json"))

    def test_is_builtin_theme_and_load_builtin_theme_dict(self):
        # existing builtin 'dark' is present in repository
        cases = [
            ("dark", True),
            ("not-a-theme", False),
        ]

        for name, expected in cases:
            with self.subTest(name=name):
                self.assertEqual(theme_module._is_builtin_theme(name), expected)

        data = theme_module._load_builtin_theme_dict("dark")
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get("name"), "Dark")
        self.assertIn("elements", data)
        self.assertIn("label", data["elements"])
        self.assertEqual(data["elements"]["label"]["text_color"], "#FFFFFF")

    def test_load_theme_with_string_uses_cache_and_returns_theme(self):
        # ensure cache empty for test determinism
        theme_module._theme_cache.clear()

        t1 = theme_module.load_theme("dark")
        self.assertIsInstance(t1, Theme)
        self.assertEqual(t1.name, "Dark")
        self.assertEqual(t1.label_theme.text_color, (255, 255, 255))

        # second load should return the cached object
        t2 = theme_module.load_theme("dark")
        self.assertIs(t1, t2)

    def test_load_theme_with_unknown_string_and_invalid_type(self):
        cases = [
            ("not-a-theme", WillRaise(ValueError)),
            (123, WillRaise(TypeError)),
        ]

        # ensure deterministic cache state
        theme_module._theme_cache.clear()

        for value, expected in cases:
            with self.subTest(value=value):
                if isinstance(expected, WillRaise):
                    with self.assertRaises(expected.exception_type):
                        theme_module.load_theme(value)
                else:
                    self.assertEqual(theme_module.load_theme(value), expected)

    def test_get_element_dict_validation_errors(self):
        cases = [
            ({}, WillRaise(ValueError)),
            ({"elements": "nope"}, WillRaise(ValueError)),
            ({"elements": {}}, WillRaise(ValueError)),
            ({"elements": {"label": "nope"}}, WillRaise(ValueError)),
        ]

        for value, expected in cases:
            with self.subTest(value=value):
                if isinstance(expected, WillRaise):
                    with self.assertRaises(expected.exception_type):
                        Theme._get_element_dict(value, "label")
                else:
                    self.assertEqual(Theme._get_element_dict(value, "label"), expected)

    def test_parse_element_color_valid_and_invalid(self):
        cases = [
            ({"text_color": "#0F1011"}, (15, 16, 17)),
            ({"text_color": (1, 2, 3)}, (1, 2, 3)),
            ({"text_color": pygame.Color(5, 6, 7, 8)}, (5, 6, 7)),
            ({}, WillRaise(ValueError)),
            ({"text_color": 123}, WillRaise(ValueError)),
        ]

        for value, expected in cases:
            with self.subTest(value=value):
                if isinstance(expected, WillRaise):
                    with self.assertRaises(expected.exception_type):
                        Theme._parse_element_color(value, "label", "text_color")
                else:
                    result = Theme._parse_element_color(value, "label", "text_color")
                    self.assertEqual(result, expected)

    def test_parse_name_validation(self):
        cases = [
            ({}, WillRaise(ValueError)),
            ({"name": 123}, WillRaise(ValueError)),
        ]

        for value, expected in cases:
            with self.subTest(value=value):
                if isinstance(expected, WillRaise):
                    with self.assertRaises(expected.exception_type):
                        Theme._parse_name(value)
                else:
                    self.assertEqual(Theme._parse_name(value), expected)


