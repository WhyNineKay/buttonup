import unittest
from typing import Any, Tuple

import pygame

from buttonup.elements.element import PositionalElement, SizedElement
from tests.testing_tools import WillRaise



class TestPositionalElement(unittest.TestCase):
    def test_constructor_accepts_ints_floats_and_intlike_or_raises(self):
        class IntLike:
            def __init__(self, v: int) -> None:
                self.v = v

            def __int__(self) -> int:
                return int(self.v)

        cases: Tuple[Tuple[Any, Any], ...] = (
            ((1, 2), (1, 2)),
            ((3.9, 4.1), (3, 4)),
            ((IntLike(7), 8), (7, 8)),
            (("a", 1), WillRaise(TypeError)),
            ((1, "b"), WillRaise(TypeError)),
        )

        for (x, y), expected in cases:
            with self.subTest(x=x, y=y):
                if isinstance(expected, WillRaise):
                    with self.assertRaises(expected.exception_type):
                        PositionalElement(x, y)
                else:
                    el = PositionalElement(x, y)
                    self.assertEqual((el.x, el.y), expected)

    def test_set_x_updates_with_int_conversion(self):
        cases_and_expected = [
            (10, (10, 0)),
            (2.9, (2, 0)),
        ]

        for value, expected in cases_and_expected:
            with self.subTest(value=value):
                el = PositionalElement(0, 0)
                el.x = value  # type: ignore
                self.assertEqual((el.x, el.y), expected)

    def test_set_y_updates_with_int_conversion(self):
        cases_and_expected = [
            (5, (0, 5)),
            (6.7, (0, 6)),
        ]

        for value, expected in cases_and_expected:
            with self.subTest(value=value):
                el = PositionalElement(0, 0)
                el.y = value  # type: ignore
                self.assertEqual((el.x, el.y), expected)

    def test_pos_setter_accepts_tuple_of_two_and_rejects_others(self):
        cases = [
            ((1, 2), (1, 2)),
            ((1.9, 2.1), (1, 2)),
            ([1, 2], WillRaise(TypeError)),
            ((1,), WillRaise(TypeError)),
            ("1,2", WillRaise(TypeError)),
        ]

        for value, expected in cases:
            with self.subTest(value=value):
                el = PositionalElement(0, 0)

                if isinstance(expected, WillRaise):
                    with self.assertRaises(expected.exception_type):
                        el.pos = value  # type: ignore
                else:
                    el.pos = value  # type: ignore
                    self.assertEqual(el.pos, expected)

    def test_vec_getter_and_setter_convert_to_int_and_validate_type(self):
        el = PositionalElement(2, 3)
        vec = el.vec
        self.assertIsInstance(vec, pygame.Vector2)
        self.assertEqual((int(vec.x), int(vec.y)), (2, 3))

        # setting with Vector2 should update position (with int conversion)
        el.vec = pygame.Vector2(9.9, 10.1)
        self.assertEqual(el.pos, (9, 10))

        # non-Vector2 should raise
        with self.assertRaises(TypeError):
            el.vec = (1, 2)  # type: ignore


