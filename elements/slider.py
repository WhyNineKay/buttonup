"""
Slider
"""
from typing import Union, Callable

from ..themes.themes import Theme
from ..themes import themes
import pygame
from .. import constants as c
from ..elements.element import NewElement
from ..utility.program_tools import check_tools, text_align, color_tools


class DefaultSlider(NewElement):
    def __init__(self,
                 pos_x: int,
                 pos_y: int,
                 width: int = None,
                 height: int = None,
                 thumb_width: int = None,
                 thumb_height: int = None,
                 theme: Union[Theme, str] = None,
                 border_radius: int = None,
                 border_radius_thumb: int = None,
                 border_radius_track: int = None,
                 on_click_function: Callable = None,
                 on_click_function_args: list | tuple = None,
                 on_click_function_kwargs: dict = None,
                 on_hover_function: Callable = None,
                 on_hover_function_args: list | tuple = None,
                 on_hover_function_kwargs: dict = None,
                 cursor_change_hover: bool = None
                 ) -> None:
        """
        :param pos_x: The x position of the slider
        :param pos_y: The y position of the slider
        :param width: The width of the track
        :param height: The height of the track
        :param thumb_width: The width of the thumb
        :param thumb_height: The height of the thumb
        :param theme: The theme.
        :param border_radius: Main border radius.
        :param border_radius_thumb: Thumb border radius. Will use border_radius if None.
        :param border_radius_track: Track border radius. Will use border_radius if None.
        :param on_click_function: The function to call when the slider is clicked.
        :param on_click_function_args: The args to pass to the function.
        :param on_click_function_kwargs: The kwargs to pass to the function.
        :param on_hover_function: The function to call when the slider is hovered over.
        :param on_hover_function_args: The args to pass to the function.
        :param on_hover_function_kwargs: The kwargs to pass to the function.
        :param cursor_change_hover: If the cursor should change when hovered over.
        :raises TypeError: If any of the arguments do not meet the required type.
        :raises ValueError: If any of the arguments are not of the required value.
        """

        super().__init__()

        # -------- POSITION
        if not check_tools.is_int(pos_x):
            try:
                pos_x = int(pos_x)
            except ValueError:
                raise TypeError(f"pos_x must be of type int, not '{type(pos_x)}'.")
            else:
                pass

        self._pos_x = pos_x

        if not check_tools.is_int(pos_y):
            try:
                pos_y = int(pos_y)
            except ValueError:
                raise TypeError(f"pos_y must be of type int, not '{type(pos_y)}'.")
            else:
                pass

        self._pos_y = pos_y

        # -------- GEOMETRY
        if width is None:
            width = 100
        else:
            if not check_tools.is_int(width):
                try:
                    width = int(width)
                except ValueError:
                    raise TypeError(f"width must be of type int, not '{type(width)}'.")
                else:
                    pass

        self._width = width

        if height is None:
            height = 5
        else:
            if not check_tools.is_int(height):
                try:
                    height = int(height)
                except ValueError:
                    raise TypeError(f"height must be of type int, not '{type(height)}'.")
                else:
                    pass

        self._height = height

        # -------- THEME

        if theme is None:
            theme = themes.get_default_theme()
        elif isinstance(theme, str):
            if theme in themes.get_all_themes():
                theme = themes.get_theme(theme)
            else:
                raise ValueError(f"theme '{theme}' does not exist.")
        else:
            if not isinstance(theme, themes.Theme):
                raise TypeError(f"theme must be of type themes.Theme or str, not '{type(theme)}'.")

        self._theme = theme


        # -------- BORDER RADIUS

        if border_radius is None:
            border_radius = 0

        else:
            if not check_tools.is_int(border_radius):
                try:
                    border_radius = int(border_radius)
                except ValueError:
                    raise TypeError(f"border_radius must be of type int, not '{type(border_radius)}'.")
                else:
                    pass

                if border_radius < 0:
                    raise ValueError(f"border_radius must be greater than or equal to 0, not "
                                     f"'{border_radius}'.")

        self._border_radius = border_radius

        if border_radius_thumb is None:
            border_radius_thumb = border_radius

        else:
            if not check_tools.is_int(border_radius_thumb):
                try:
                    border_radius_thumb = int(border_radius_thumb)
                except ValueError:
                    raise TypeError(f"border_radius_thumb must be of type int, not '{type(border_radius_thumb)}'.")
                else:
                    pass

                if border_radius_thumb < 0:
                    raise ValueError(f"border_radius_thumb must be greater than or equal to 0, not "
                                     f"'{border_radius_thumb}'.")

        self._border_radius_thumb = border_radius_thumb

        if border_radius_track is None:
            border_radius_track = border_radius

        else:
            if not check_tools.is_int(border_radius_track):
                try:
                    border_radius_track = int(border_radius_track)
                except ValueError:
                    raise TypeError(f"border_radius_track must be of type int, not '{type(border_radius_track)}'.")
                else:
                    pass

                if border_radius_track < 0:
                    raise ValueError(f"border_radius_track must be greater than or equal to 0, not "
                                     f"'{border_radius_track}'.")



