from utility.program_tools import color_tools, check_tools
import unittest
import pygame


class CheckToolsTesting(unittest.TestCase):
    def test_is_num(self):
        self.assertEqual(check_tools.is_num(0), True)
        self.assertEqual(check_tools.is_num(-1), True)
        self.assertEqual(check_tools.is_num(0.02), True)
        self.assertEqual(check_tools.is_num("a"), False)
        self.assertEqual(check_tools.is_num(0xfffffff), True)
        self.assertEqual(check_tools.is_num(41374781834), True)

    def test_is_str(self):
        self.assertEqual(check_tools.is_str(0), False)
        self.assertEqual(check_tools.is_str("string"), True)
        self.assertEqual(check_tools.is_str(f"{0}"), True)
        self.assertEqual(check_tools.is_str(True), False)

    def test_is_negative(self):
        self.assertEqual(check_tools.is_negative(-10), True)
        self.assertEqual(check_tools.is_negative(10), False)
        self.assertEqual(check_tools.is_negative(-0), False)
        self.assertEqual(check_tools.is_negative(0.1), False)

    def test_is_pos(self):
        self.assertEqual(check_tools.is_pos((4, 3)), True)
        self.assertEqual(check_tools.is_pos((14041, -123)), True)
        self.assertEqual(check_tools.is_pos((1.2, 4.3)), True)
        self.assertEqual(check_tools.is_pos((0,)), False)
        self.assertEqual(check_tools.is_pos("0"), False)
        self.assertEqual(check_tools.is_pos(("0", "2")), False)
        self.assertEqual(check_tools.is_pos("12"), False)
        self.assertEqual(check_tools.is_pos([4, 3]), False)
        self.assertEqual(check_tools.is_pos((4, 3, 56)), False)




class ColorToolsIsColorTest(unittest.TestCase):
    def test_rgb_tuple(self):
        self.assertEqual(color_tools.is_color((0, 0, 0)), True)
        self.assertEqual(color_tools.is_color((-1, 255, 0)), False)
        self.assertEqual(color_tools.is_color((0, 255, 25)), True)
        self.assertEqual(color_tools.is_color((256, 0, 0)), False)
        self.assertEqual(color_tools.is_color((0, 255, -1000)), False)
        self.assertEqual(color_tools.is_color((0, 255, 255)), True)
        self.assertEqual(color_tools.is_color((0, 255, 0)), True)
        self.assertEqual(color_tools.is_color((0, -255, 0)), False)

    def test_hex_string(self):
        self.assertEqual(color_tools.is_color("#9c3932"), True)
        self.assertEqual(color_tools.is_color("#9ch932"), False)
        self.assertEqual(color_tools.is_color("9c3932"), True)
        self.assertEqual(color_tools.is_color("#llllll"), False)
        self.assertEqual(color_tools.is_color("#000"), False)
        self.assertEqual(color_tools.is_color("c3932"), False)
        self.assertEqual(color_tools.is_color("#9c393pp2"), False)

    def test_pygame_color(self):
        self.assertEqual(color_tools.is_color(pygame.Color(0, 0, 0)), True)