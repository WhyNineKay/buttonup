"""
Colors for colored labels
"""

from typing import Any

from .. Utility.program_tools import check_tools, color_tools
from .. import constants as c


class ColorPalette:
    """Color palette to reference custom colors and keywords for colored elements involving colored text."""
    def __init__(self) -> None:
        self._keyword_color_dict: dict = {}

    def add_color(self, keyword: str, color: Any) -> None:
        """
        Add a color to the color palette.
        :param keyword: Keyword to reference the color.
        :param color: Color to add.
        :raises ValueError: If the keyword is already in use.
        :raises ValueError: If any of the arguments are invalid.
        """

        # check types

        if not check_tools.is_str(keyword):
            raise ValueError("keyword argument must be of type <str>.")

        if color == c.COLOR_RESET:
            self._keyword_color_dict[keyword] = color

        elif not color_tools.is_color(color):
            raise ValueError(f"color argument must be RGB, HEX, or pygame.Color, not '{color}'.")

        # check if keyword is already in use
        elif keyword in self._keyword_color_dict:
            raise ValueError(f"keyword '{keyword}' is already in use.")

        # add color
        self._keyword_color_dict[keyword] = color

    def add_reset(self, keyword: str) -> None:
        """
        Add a reset color to the color palette.
        :param keyword: Keyword to reference the color.
        :raises ValueError: If the keyword is already in use.
        :raises ValueError: If the keyword argument is invalid.
        """

        self.add_color(keyword, c.COLOR_RESET)

    def get_color(self, keyword: str) -> Any:
        """
        Get a color from the color palette.
        :param keyword: Keyword to reference the color.
        :return: Color.
        :raises ValueError: If the keyword is not in use.
        :raises ValueError: If the keyword argument is invalid.
        """

        # check types
        if not check_tools.is_str(keyword):
            raise ValueError("keyword argument must be of type <str>.")

        # check if keyword is in use
        if keyword not in self._keyword_color_dict:
            raise ValueError(f"keyword '{keyword}' is not in the color palette.")

        # return color
        return self._keyword_color_dict[keyword]

    def remove_color(self, keyword: str) -> None:
        """
        Remove a color from the color palette.
        :param keyword: Keyword to reference the color.
        :raises ValueError: If the keyword is not in use.
        :raises ValueError: If the keyword argument is invalid.
        """

        # check types
        if not check_tools.is_str(keyword):
            raise ValueError("keyword argument must be of type <str>.")

        # check if keyword is in use
        if keyword not in self._keyword_color_dict:
            raise ValueError(f"keyword '{keyword}' is not in the color palette.")

        # remove color
        del self._keyword_color_dict[keyword]

    @property
    def keyword_color_dict(self) -> dict[str, Any]:
        """
        Get the keyword color dictionary.
        :return: Keyword color dictionary.
        """
        return self._keyword_color_dict

