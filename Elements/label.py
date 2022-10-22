import re
from dataclasses import dataclass
from typing import Any

from .. Elements.element import Element
from .. Utility.program_tools import check_tools, color_tools
from .. Utility.globs import globs
from .. Themes import themes
from .. Tools import colors
from .. import constants

import pygame


class DefaultLabel(Element):
    def __init__(self,
                 pos_x: int,
                 pos_y: int,
                 text: str = "Hi!",
                 text_size: int = 10,
                 font: str = "consolas",
                 theme: themes.Theme = None,
                 antialiasing: bool = True) -> None:

        super().__init__()

        if check_tools.is_num(pos_x):
            self._pos_x = int(pos_x)
        else:
            raise ValueError("position values must be of type <int> or <float>.")

        if check_tools.is_num(pos_y):
            self._pos_y = int(pos_y)
        else:
            raise ValueError("position values must be of type <int> or <float>.")

        if check_tools.is_str(text):
            self._text = str(text)
        else:
            raise ValueError("text argument must be of type <str>.")

        if check_tools.is_negative(text_size):
            raise ValueError("text_size argument must be a positive int.")
        elif check_tools.is_num(text_size):
            self._text_size = int(text_size)
        else:
            raise ValueError("text_size argument must be of type <int> or <float>.")

        # TODO: add font from file support
        if check_tools.is_str(font):
            self._font = pygame.font.SysFont(font, self._text_size)
        else:
            raise ValueError("font argument must be of type <str>.")

        if theme is None:
            self._theme = globs.project_theme
        elif isinstance(theme, themes.Theme):
            self._theme = theme
        elif isinstance(theme, str):
            self._theme = themes.get_theme(str(theme))
        else:
            raise ValueError("theme argument must be of type <str> or <Theme>.")

        if check_tools.is_bool(antialiasing):
            self._antialiasing = antialiasing
        else:
            raise ValueError("antialiasing argument must be of type <bool>.")

        self._color_text = None
        self._create_colors()
        self._text_surface = self._font.render(self._text, self._antialiasing, self._theme.on_background)

    def _create_colors(self) -> None:
        self._color_text = self._theme.on_background

    def render(self, screen: pygame.Surface) -> None:
        """Renders the element to the screen."""
        screen.blit(self._text_surface, (self._pos_x, self._pos_y))

    def update(self, dt: float) -> None:
        """
        Updates the element.
        :param dt: Delta time. Optional for some elements.
        """
        pass

    @property
    def text(self) -> str:
        """
        Get the text
        """
        return self._text

    @text.setter
    def text(self, value: str) -> None:

        # do type checks

        self._text = str(value)
        self._text_surface = self._font.render(self._text, self._antialiasing, self._color_text)

    @property
    def pos(self) -> tuple[int, int]:
        """
        Gets a tuple of the position of the label.
        :return pos: The position.
        """
        return self._pos_x, self._pos_y

    @pos.setter
    def pos(self, value: tuple[int, int]) -> None:
        """
        Sets the position of the label.
        :raises ValueError: If the position is invalid.
        """

        if not check_tools.is_pos(value):
            raise ValueError(f"position must be tuple[int, int] not '{value}'.")

        self._pos_x = value[0]
        self._pos_y = value[1]

    @property
    def x(self) -> int:
        """
        Gets the x value of the label.
        """
        return self._pos_x

    @x.setter
    def x(self, value: int) -> None:
        """
        Set the x value of the label
        :raises ValueError: If the value is not an int or float.
        """
        if check_tools.is_num(value):
            self.pos = int(value), self.pos[1]
        else:
            raise ValueError("x value must be of type <int> or <float>.")

    @property
    def y(self) -> int:
        """
        Gets the x value of the label.
        """
        return self._pos_y

    @y.setter
    def y(self, value: int) -> None:
        """
        Set the x value of the label
        :raises ValueError: If the value is not an int or float.
        """
        if check_tools.is_num(value):
            self.pos = self.pos[0], int(value)
        else:
            raise ValueError("y value must be of type <int> or <float>.")

    @property
    def antialiasing(self) -> bool:
        """
        Get whether the text is antialiased.
        """
        return self._antialiasing

    @antialiasing.setter
    def antialiasing(self, value: bool) -> None:
        """
        Set antialiasing for the text.
        :param value: Antialiasing
        :raises ValueError: If the value is not a bool.
        """
        if check_tools.is_bool(value):
            self._antialiasing = value
        else:
            raise ValueError("antialiasing argument must be of type <bool>.")

        self._text_surface = self._font.render(self._text, self._antialiasing, self._color_text)

    @property
    def text_surface(self) -> pygame.Surface:
        """
        Return the text surface.
        :return:
        """
        return self._text_surface

    def set_color(self, key: str, color: Any) -> None:
        """
        Set a certain color of the button.

        :param key: The requested color. Must be one of: ["text"]. It is case insensitive.
        :param color: The color to set.
        """

        # check if key is correct
        colors_list = ['text']

        if key.lower() not in colors_list:
            raise ValueError(f"Invalid key '{key}'.", "invalid_key")

        if not color_tools.is_color(color):
            raise ValueError(f"Invalid color '{color}'.", "invalid_color")

        key = key.lower()

        if key == 'text':
            self._color_text = color

        self._text_surface = self._font.render(self._text, self._antialiasing, self._color_text)


@dataclass
class _Chunk:
    keyword: str | None
    text: str

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.keyword!r}:{self.text!r}"


class ColoredLabel(Element):
    def __init__(self,
                 pos_x: int,
                 pos_y: int,
                 text: str = "Hi!",
                 text_size: int = 10,
                 font: str = "consolas",
                 theme: themes.Theme = None,
                 antialiasing: bool = True,
                 color_palette: colors.ColorPalette = None) -> None:

        super().__init__()

        if check_tools.is_num(pos_x):
            self._pos_x = int(pos_x)
        else:
            raise ValueError("position values must be of type <int> or <float>.")

        if check_tools.is_num(pos_y):
            self._pos_y = int(pos_y)
        else:
            raise ValueError("position values must be of type <int> or <float>.")

        if check_tools.is_str(text):
            self._text = str(text)
        else:
            raise ValueError("text argument must be of type <str>.")

        if check_tools.is_negative(text_size):
            raise ValueError("text_size argument must be a positive int.")
        elif check_tools.is_num(text_size):
            self._text_size = int(text_size)
        else:
            raise ValueError("text_size argument must be of type <int> or <float>.")

        # TODO: add font from file support
        if check_tools.is_str(font):
            self._font = pygame.font.SysFont(font, self._text_size)
            self._font_name = font
        else:
            raise ValueError("font argument must be of type <str>.")

        if theme is None:
            self._theme = globs.project_theme
        elif isinstance(theme, themes.Theme):
            self._theme = theme
        elif isinstance(theme, str):
            self._theme = themes.get_theme(str(theme))
        else:
            raise ValueError("theme argument must be of type <str> or <Theme>.")

        if check_tools.is_bool(antialiasing):
            self._antialiasing = antialiasing
        else:
            raise ValueError("antialiasing argument must be of type <bool>.")

        if color_palette is None:
            self._color_palette = colors.ColorPalette()
        elif isinstance(color_palette, colors.ColorPalette):
            self._color_palette = color_palette
        else:
            raise ValueError("color_palette argument must be of type <ColorPalette>.")

        self._labels = []

        self._create_colors()
        self._create_labels()

    def _create_colors(self) -> None:
        """
        Creates the colors for the text.
        """
        self._color_text = self._theme.on_background

    def _create_labels(self) -> None:
        """
        Create individual labels with colors
        """

        keywords = list(self._color_palette.keyword_color_dict.keys())
        keywords_regex_safe = [re.escape(keyword) for keyword in keywords]
        string = self._text

        # split string into chunks
        string_chunks = re.split(r"(" + "|".join(keywords_regex_safe) + ")", string)
        chunks: list[_Chunk] = []
        self._labels.clear()

        key = None
        for chunk in string_chunks:

            if chunk in keywords:
                key = keywords[keywords.index(chunk)]
            else:

                chunks.append(_Chunk(key, chunk))

        # create labels
        current_x = self._pos_x

        for chunk in chunks:
            if chunk.keyword is None:
                color = self._color_text
            else:
                color = self._color_palette.keyword_color_dict[chunk.keyword]

            if color == constants.COLOR_RESET:
                color = self._color_text

            label = DefaultLabel(pos_x=current_x, pos_y=self._pos_y, text=chunk.text, text_size=self._text_size,
                                 font=self._font_name, theme=self._theme, antialiasing=self._antialiasing)

            label.set_color("text", color)

            self._labels.append(label)

            current_x += label.text_surface.get_width()

    def _on_prop_update(self) -> None:
        """
        Executes when a property updates, such as position change, or text change.
        """
        self._create_labels()

    def render(self, surface: pygame.Surface) -> None:
        """
        Render the text to the surface.
        :param surface: Surface to render to.
        """
        for label in self._labels:
            label.render(surface)

    def update(self, dt: float) -> None:
        """
        Updates the element.
        :param dt: Delta time. Optional for some elements.
        """
        pass

    @property
    def text(self) -> str:
        """
        Get the text of all the labels. Includes color keywords.
        :return: The text.
        """
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        """
        Set the text of the label.
        You can use color keywords in the text.
        :param text: The text.
        """

        if check_tools.is_str(text):
            self._text = str(text)
        else:
            raise ValueError("text argument must be of type <str>.")

        self._on_prop_update()

    @property
    def keywordless_text(self) -> str:
        """
        Get the text of all the labels, excluding any color keywords.
        :return: The text.
        """
        return "".join([label.text for label in self._labels])

    @property
    def pos(self) -> tuple[int, int]:
        """
        Gets a tuple of the position of the label.
        :return pos: The position.
        """
        return self._pos_x, self._pos_y

    @pos.setter
    def pos(self, value: tuple[int, int]) -> None:
        """
        Sets the position of the label.
        :raises ValueError: If the position is invalid.
        """

        if not check_tools.is_pos(value):
            raise ValueError(f"position must be tuple[int, int] not '{value}'.")

        self._pos_x = value[0]
        self._pos_y = value[1]

        self._on_prop_update()

    @property
    def x(self) -> int:
        """
        Gets the x value of the label.
        """
        return self._pos_x

    @x.setter
    def x(self, value: int) -> None:
        """
        Set the x value of the label
        :raises ValueError: If the value is not an int or float.
        """
        if check_tools.is_num(value):
            self.pos = int(value), self.pos[1]
        else:
            raise ValueError("x value must be of type <int> or <float>.")

        self._on_prop_update()

    @property
    def y(self) -> int:
        """
        Gets the x value of the label.
        """
        return self._pos_y

    @y.setter
    def y(self, value: int) -> None:
        """
        Set the x value of the label
        :raises ValueError: If the value is not an int or float.
        """
        if check_tools.is_num(value):
            self.pos = self.pos[0], int(value)
        else:
            raise ValueError("y value must be of type <int> or <float>.")

        self._on_prop_update()

    @property
    def antialiasing(self) -> bool:
        """
        Get whether the text is anti-aliased.
        """
        return self._antialiasing

    @antialiasing.setter
    def antialiasing(self, value: bool) -> None:
        """
        Set whether the text is anti-aliased.
        """
        if check_tools.is_bool(value):
            self._antialiasing = value
        else:
            raise ValueError("antialiasing must be of type <bool>.")

        self._on_prop_update()

    @property
    def individual_labels(self) -> list[DefaultLabel]:
        """
        Get the individual labels that construct the text colors.
        :return: The labels.
        """
        return self._labels

    @property
    def width(self) -> int:
        """
        Get the width of the text.
        :return: The width.
        """
        return sum([label.width for label in self._labels])

    @property
    def height(self) -> int:
        """
        Get the height of the text.
        :return: The height.
        """
        return max([label.text_surface.get_height() for label in self._labels])

    @property
    def size(self) -> tuple[int, int]:
        """
        Get the size of the text.
        :return: The size.
        """
        return self.width, self.height

    @property
    def color_palette(self) -> colors.ColorPalette:
        """
        Get the color palette.
        :return: The color palette.
        """
        return self._color_palette

    @color_palette.setter
    def color_palette(self, value: colors.ColorPalette) -> None:
        """
        Set the color palette.
        :param value: The color palette.
        """

        if check_tools.is_color_palette(value):
            self._color_palette = value
        else:
            raise ValueError("color_palette must be of type <ColorPalette>.")

        self._on_prop_update()

    @property
    def text_size(self) -> int:
        """
        Get the text size.
        :return: The text size.
        """
        return self._text_size

    @text_size.setter
    def text_size(self, value: int) -> None:
        """
        Set the text size.
        :param value: The text size.
        """

        if check_tools.is_num(value):
            self._text_size = int(value)
        elif check_tools.is_negative(value):
            raise ValueError("text_size must be a positive number.")
        else:
            raise ValueError("text_size must be of type <int> or <float>.")

        self._on_prop_update()

    @property
    def theme(self) -> themes.Theme:
        """
        Gets the current theme that the object is using.
        :return: Theme object.
        """
        return self._theme

    @theme.setter
    def theme(self, value: themes.Theme | str) -> None:
        """
        Sets the theme and reloads the colors.
        Returns the default theme if it is not found.

        :param value: Theme object or the name of the theme.
        :raises ValueError: If theme object is not a valid theme.
        """

        if not isinstance(value, themes.Theme) and not isinstance(value, str):
            raise ValueError("Invalid theme. Use a Theme object theme or a string of the name of the theme.")

        if isinstance(value, themes.Theme):
            theme = value

        elif isinstance(value, str):
            # it is a string
            theme = themes.get_theme(value)

        else:
            theme = themes.get_default_theme()

        self._theme = theme

        self._create_colors()
        self._on_prop_update()
