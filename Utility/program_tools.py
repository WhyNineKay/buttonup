"""
This file holds all the necessary tools for the program.
"""
import colorsys
import pygame
from typing import Any


def empty_function():
    pass


def clamp(val: float, min_val: float, max_val: float) -> float:
    return max(min(val, max_val), min_val)


def make_positive(val: float | int) -> float | int:
    return val if val > 0 else 0


class CheckTools:

    @staticmethod
    def is_num(case: Any) -> bool:
        """
        Check if a case is an int or float.
        """

        return isinstance(case, int) or isinstance(case, float)

    @staticmethod
    def is_str(case: Any) -> bool:
        return isinstance(case, str)

    @staticmethod
    def is_negative(case: Any) -> bool:
        return case < 0.0

    @staticmethod
    def is_int(case: Any) -> bool:
        return isinstance(case, int)

    @staticmethod
    def is_bool(case: Any) -> bool:
        return isinstance(case, bool)

    @staticmethod
    def is_pos(case: Any, accept_floats: bool = True) -> bool:
        """
        Is the case a tuple[int, int].
        """

        if not isinstance(case, tuple):
            return False

        if len(case) != 2:
            return False

        if accept_floats:
            if isinstance(case[0], int) or isinstance(case[0], float):
                pass
            else:
                return False

            if isinstance(case[1], int) or isinstance(case[1], float):
                pass
            else:
                return False

            return True

        else:
            if isinstance(case[0], int):
                pass
            else:
                return False

            if isinstance(case[1], int):
                pass
            else:
                return False

            return True


check_tools = CheckTools()


class ColorTools:
    @staticmethod
    def correct_rgb_tuple(rgb: tuple) -> tuple:
        # TODO: add support for rgba

        rgb = list(rgb)

        for i in range(3):
            rgb[i] = int(clamp(rgb[i], 0, 255))

        return tuple(rgb)

    def rgb_to_hex(self, rgb: tuple) -> str:
        return "#%02x%02x%02x" % self.correct_rgb_tuple(rgb)

    @staticmethod
    def hex_to_rgb(hex_string: str) -> tuple:
        hex_string = hex_string.lstrip('#')
        rgb = tuple(int(hex_string[i:i + 2], 16) for i in (0, 2, 4))

        return rgb

    def hex_to_hls(self, hex_string: str) -> tuple:
        return colorsys.rgb_to_hls(*self.hex_to_rgb(hex_string))

    def change_hex_brightness(self, hex_value: str, brightness_amount: int) -> str:
        """
        Brightness amount should be -255 to 255.
        """

        rgb = list(self.hex_to_rgb(hex_value))

        rgb[0] += brightness_amount
        rgb[1] += brightness_amount
        rgb[2] += brightness_amount

        return self.rgb_to_hex(tuple(rgb))

    def is_color(self, color: Any) -> bool:
        """
        Check if a color is a valid color.
        """

        # check rgb
        if isinstance(color, tuple) or isinstance(color, list):
            if 3 > len(color) > 4:
                return False

            for i in color:
                if i < 0:
                    return False
                elif i > 255:
                    return False

            return True

        # check hex
        elif isinstance(color, str):
            if color.startswith("#"):
                color = color[1:]

            if not len(color) == 6:
                return False

            try:
                int(color, 16)
            except ValueError:
                return False

            return True

        elif isinstance(color, pygame.Color):
            return True

        return True


color_tools = ColorTools()


class AlignText:
    @staticmethod
    def top_left(text_rect: pygame.Rect, area_rect: pygame.Rect, margin: int = 10) -> pygame.Rect:
        """
        This function aligns the text to the top left.
        area_rect is the rect of the area.
        text_rect is the rect of the text.

        x - -
        - - -
        - - -
        """

        new_x = area_rect.x + margin
        new_y = area_rect.y + margin
        text_rect.x = new_x
        text_rect.y = new_y
        return text_rect

    @staticmethod
    def top_center(text_rect: pygame.Rect, area_rect: pygame.Rect, margin: int = 10) -> pygame.Rect:
        """
        This function aligns the text to the top center.
        area_rect is the rect of the area.
        text_rect is the rect of the text.

        - x -
        - - -
        - - -
        """
        new_x = area_rect.x + (area_rect.width / 2) - (text_rect.width / 2)
        new_y = area_rect.y + margin
        text_rect.x = new_x
        text_rect.y = new_y
        return text_rect

    @staticmethod
    def top_right(text_rect: pygame.Rect, area_rect: pygame.Rect, margin: int = 10) -> pygame.Rect:
        """
        This function aligns the text to the top right.
        area_rect is the rect of the area.
        text_rect is the rect of the text.

        - - x
        - - -
        - - -
        """
        new_x = area_rect.x + area_rect.width - text_rect.width - margin
        new_y = area_rect.y + margin
        text_rect.x = new_x
        text_rect.y = new_y
        return text_rect

    @staticmethod
    def center_left(text_rect: pygame.Rect, area_rect: pygame.Rect, margin: int = 10) -> pygame.Rect:
        """
        This function aligns the text to the center left.
        area_rect is the rect of the area.
        text_rect is the rect of the text.

        - - -
        x - -
        - - -
        """
        new_x = area_rect.x + margin
        new_y = area_rect.y + (area_rect.height / 2) - (text_rect.height / 2)
        text_rect.x = new_x
        text_rect.y = new_y
        return text_rect

    @staticmethod
    def center_center(text_rect: pygame.Rect, area_rect: pygame.Rect) -> pygame.Rect:
        """
        This function aligns the text to the center center.
        area_rect is the rect of the area.
        text_rect is the rect of the text.

        !!! Does not accept margin argument. !!!

        - - -
        - x -
        - - -
        """
        new_x = area_rect.x + (area_rect.width / 2) - (text_rect.width / 2)
        new_y = area_rect.y + (area_rect.height / 2) - (text_rect.height / 2)
        text_rect.x = new_x
        text_rect.y = new_y
        return text_rect

    @staticmethod
    def center_right(text_rect: pygame.Rect, area_rect: pygame.Rect, margin: int = 10) -> pygame.Rect:
        """
        This function aligns the text to the center right.
        area_rect is the rect of the area.
        text_rect is the rect of the text.

        - - -
        - - x
        - - -
        """
        new_x = area_rect.x + area_rect.width - text_rect.width - margin
        new_y = area_rect.y + (area_rect.height / 2) - (text_rect.height / 2)
        text_rect.x = new_x
        text_rect.y = new_y
        return text_rect

    @staticmethod
    def bottom_left(text_rect: pygame.Rect, area_rect: pygame.Rect, margin: int = 10) -> pygame.Rect:
        """
        This function aligns the text to the bottom left.
        area_rect is the rect of the area.
        text_rect is the rect of the text.

        - - -
        - - -
        x - -
        """
        new_x = area_rect.x + margin
        new_y = area_rect.y + area_rect.height - text_rect.height - margin
        text_rect.x = new_x
        text_rect.y = new_y
        return text_rect

    @staticmethod
    def bottom_center(text_rect: pygame.Rect, area_rect: pygame.Rect, margin: int = 10) -> pygame.Rect:
        """
        This function aligns the text to the bottom center.
        area_rect is the rect of the area.
        text_rect is the rect of the text.

        - - -
        - - -
        - x -
        """
        new_x = area_rect.x + (area_rect.width / 2) - (text_rect.width / 2)
        new_y = area_rect.y + area_rect.height - text_rect.height - margin
        text_rect.x = new_x
        text_rect.y = new_y
        return text_rect

    @staticmethod
    def bottom_right(text_rect: pygame.Rect, area_rect: pygame.Rect, margin: int = 10) -> pygame.Rect:
        """
        This function aligns the text to the bottom right.
        area_rect is the rect of the area.
        text_rect is the rect of the text.

        - - -
        - - -
        - - x
        """
        new_x = area_rect.x + area_rect.width - text_rect.width - margin
        new_y = area_rect.y + area_rect.height - text_rect.height - margin
        text_rect.x = new_x
        text_rect.y = new_y
        return text_rect

    def align(self, area_rect: pygame.Rect, text_rect: pygame.Rect, text_align_x: str = "center",
              text_align_y: str = "center", margin: int = 10) -> pygame.Rect:
        """
        This function aligns the text to the given position.
        :param area_rect: Rect of the given area.
        :param text_rect: The rect of the text to move.
        :param text_align_x: String of alignment. Must be in ["left", "center", "right"]
        :param text_align_y: String of alignment. Must be in ["top", "center", "bottom"]
        :raises ValueError: If the text alignments are not correct.
        """

        text_align_x = text_align_x.lower()
        text_align_y = text_align_y.lower()

        cases = ["left", "center", "right", "top", "bottom"]

        # I have no excuse for this code
        # it just doesn't work without flipping x and y

        if text_align_x == "top":
            if text_align_y == "left":
                return self.top_left(text_rect, area_rect, margin)
            elif text_align_y == "center":
                return self.top_center(text_rect, area_rect, margin)
            elif text_align_y == "right":
                return self.top_right(text_rect, area_rect, margin)

        elif text_align_x == "center":
            if text_align_y == "left":
                return self.center_left(text_rect, area_rect, margin)
            elif text_align_y == "center":
                return self.center_center(text_rect, area_rect)
            elif text_align_y == "right":
                return self.center_right(text_rect, area_rect, margin)

        elif text_align_x == "bottom":
            if text_align_y == "left":
                return self.bottom_left(text_rect, area_rect, margin)
            elif text_align_y == "center":
                return self.bottom_center(text_rect, area_rect, margin)
            elif text_align_y == "right":
                return self.bottom_right(text_rect, area_rect, margin)
        else:
            raise ValueError("the text alignments must be one of the following: " + str(cases), "INVALID_ALIGNMENT")


text_align = AlignText()
