import unittest

import pygame

from buttonup.elements.element import SizedElement
from tests.testing_tools import WillRaise


class TestSizedElement(unittest.TestCase):
    """Tests for SizedElement. Each test re-initializes its own element instance."""

    def test_constructor_and_size_properties_and_errors(self):
        cases_and_expected = [
            ((0, 0, 1, 2), (1, 2)),
            ((5, 6, 3.9, 4.1), (3, 4)),
            ((1, 2, 0, 0), (0, 0)),
            ((1, 2, -1, 2), WillRaise(ValueError)),
            ((1, 2, 1, -2), WillRaise(ValueError)),
            ((1, 2, "w", 2), WillRaise(TypeError)),
            ((1, 2, 1, "h"), WillRaise(TypeError)),
        ]

        for args, expected in cases_and_expected:
            with self.subTest(args=args):
                x, y, width, height = args

                if isinstance(expected, WillRaise):
                    with self.assertRaises(expected.exception_type):
                        SizedElement(x, y, width, height)
                else:
                    el = SizedElement(x, y, width, height)
                    self.assertEqual(el.width, expected[0])
                    self.assertEqual(el.height, expected[1])
                    self.assertEqual(el.size, expected)
                    self.assertEqual(el.rect.size, expected)

    def test_set_x_updates_rect_and_pos(self):
        cases_and_expected = [
            (10, (10, 0)),
            (2.9, (2, 0)),
        ]

        for value, expected in cases_and_expected:
            with self.subTest(value=value):
                el = SizedElement(0, 0, 3, 4)
                el.x = value  # type: ignore
                self.assertEqual(el.pos, expected)
                self.assertEqual((el.rect.x, el.rect.y), expected)

    def test_set_y_updates_rect_and_pos(self):
        cases_and_expected = [
            (11, (0, 11)),
            (6.7, (0, 6)),
        ]

        for value, expected in cases_and_expected:
            with self.subTest(value=value):
                el = SizedElement(0, 0, 3, 4)
                el.y = value  # type: ignore
                self.assertEqual(el.pos, expected)
                self.assertEqual((el.rect.x, el.rect.y), expected)

    def test_set_pos_accepts_tuple_and_rejects_others(self):
        cases_and_expected = [
            ((1, 2), (1, 2)),
            ((1.9, 2.1), (1, 2)),
            ([1, 2], WillRaise(TypeError)),
            ((1,), WillRaise(TypeError)),
            ("1,2", WillRaise(TypeError)),
        ]

        for value, expected in cases_and_expected:
            with self.subTest(value=value):
                el = SizedElement(0, 0, 3, 4)
                if isinstance(expected, WillRaise):
                    with self.assertRaises(expected.exception_type):
                        el.pos = value  # type: ignore
                else:
                    el.pos = value  # type: ignore
                    self.assertEqual(el.pos, expected)

    def test_set_vec_accepts_vector2_and_rejects_others(self):
        cases_and_expected = [
            (pygame.Vector2(4.7, 5.2), (4, 5)),
        ]

        for value, expected in cases_and_expected:
            with self.subTest(value=value):
                el = SizedElement(0, 0, 3, 4)
                el.vec = value  # type: ignore
                self.assertEqual(el.pos, expected)
                self.assertEqual((el.rect.x, el.rect.y), expected)

        with self.assertRaises(TypeError):
            el = SizedElement(0, 0, 3, 4)
            el.vec = (1, 2)  # type: ignore

    def test_center_properties(self):
        el = SizedElement(10, 20, 4, 6)
        self.assertEqual(el.centerx, el.rect.centerx)
        self.assertEqual(el.centery, el.rect.centery)
        self.assertEqual(el.center, el.rect.center)

