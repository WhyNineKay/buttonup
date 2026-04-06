import unittest
from typing import Tuple, Any

import pygame

from buttonup.elements.element import ResizableElement
from tests.testing_tools import WillRaise


class TestResizableElement(unittest.TestCase):
    def test_constructor_and_initial_properties(self):
        cases_and_expected = [
            ((1, 2, 3, 4), (3, 4)),
            ((5, 6, 0, 0), (0, 0)),
        ]

        for args, expected in cases_and_expected:
            with self.subTest(args=args):
                x, y, w, h = args
                el = ResizableElement(x, y, w, h)
                self.assertEqual(el.pos, (int(x), int(y)))
                self.assertEqual(el.width, expected[0])
                self.assertEqual(el.height, expected[1])
                self.assertEqual(el.size, expected)
                self.assertEqual(el.rect.size, expected)

    def test_width_setter_updates_size_and_validates(self):
        cases_and_expected = [
            (10, (10, 4)),
            (2.9, (2, 4)),
            ("bad", WillRaise(TypeError)),
            (-1, WillRaise(ValueError)),
        ]

        for value, expected in cases_and_expected:
            with self.subTest(value=value):
                el = ResizableElement(0, 0, 3, 4)
                if isinstance(expected, WillRaise):
                    with self.assertRaises(expected.exception_type):
                        el.width = value  # type: ignore
                else:
                    el.width = value  # type: ignore
                    self.assertEqual(el.width, expected[0])
                    self.assertEqual(el.size, expected)
                    self.assertEqual(el.rect.size, expected)

    def test_height_setter_updates_size_and_validates(self):
        cases_and_expected = [
            (8, (3, 8)),
            (5.5, (3, 5)),
            ("bad", WillRaise(TypeError)),
            (-2, WillRaise(ValueError)),
        ]

        for value, expected in cases_and_expected:
            with self.subTest(value=value):
                el = ResizableElement(0, 0, 3, 4)
                if isinstance(expected, WillRaise):
                    with self.assertRaises(expected.exception_type):
                        el.height = value  # type: ignore
                else:
                    el.height = value  # type: ignore
                    self.assertEqual(el.height, expected[1])
                    self.assertEqual(el.size, expected)
                    self.assertEqual(el.rect.size, expected)

    def test_size_setter_accepts_tuple_and_rejects_invalid(self):
        cases_and_expected = [
            ((5, 6), (5, 6)),
            ((5.9, 6.1), (5, 6)),
            ([5, 6], WillRaise(TypeError)),
            ((5,), WillRaise(TypeError)),
            ((-1, 2), WillRaise(ValueError)),
        ]

        for value, expected in cases_and_expected:
            with self.subTest(value=value):
                el = ResizableElement(0, 0, 3, 4)
                if isinstance(expected, WillRaise):
                    with self.assertRaises(expected.exception_type):
                        el.size = value  # type: ignore
                else:
                    el.size = value  # type: ignore
                    self.assertEqual(el.size, expected)
                    self.assertEqual(el.rect.size, expected)

    def test_center_setter_moves_element_and_validates(self):
        cases_and_expected = [
            ((20, 30), (20 - 4 // 2, 30 - 6 // 2)),
            ((20.9, 30.1), (20 - 4 // 2, 30 - 6 // 2)),
            (("a", "b"), WillRaise(TypeError)),
            ((1,), WillRaise(TypeError)),
        ]

        for value, expected in cases_and_expected:
            with self.subTest(value=value):
                el = ResizableElement(0, 0, 4, 6)
                if isinstance(expected, WillRaise):
                    with self.assertRaises(expected.exception_type):
                        el.center = value  # type: ignore
                else:
                    el.center = value  # type: ignore
                    self.assertEqual(el.pos, expected)
                    self.assertEqual((el.rect.x, el.rect.y), expected)

    def test_centerx_and_centery_setters(self):
        # centerx adjusts x only; centery adjusts y only
        cases_x = [
            (50, (50 - 10 // 2, 0)),
            (50.9, (50 - 10 // 2, 0)),
            ("bad", WillRaise(TypeError)),
        ]

        for value, expected in cases_x:
            with self.subTest(centerx=value):
                el = ResizableElement(0, 0, 10, 4)
                if isinstance(expected, WillRaise):
                    with self.assertRaises(expected.exception_type):
                        el.centerx = value  # type: ignore
                else:
                    el.centerx = value  # type: ignore
                    self.assertEqual(el.pos[0], expected[0])

        cases_y = [
            (60, (0, 60 - 8 // 2)),
            (60.7, (0, 60 - 8 // 2)),
            (None, WillRaise(TypeError)),
        ]

        for value, expected in cases_y:
            with self.subTest(centery=value):
                el = ResizableElement(0, 0, 6, 8)
                if isinstance(expected, WillRaise):
                    with self.assertRaises(expected.exception_type):
                        el.centery = value  # type: ignore
                else:
                    el.centery = value  # type: ignore
                    self.assertEqual(el.pos[1], expected[1])

