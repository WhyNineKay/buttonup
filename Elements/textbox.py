from .. Utility.program_tools import check_tools
from .. Elements import element
from .. Themes import themes

import pygame

raise NotImplementedError("Textbox class has not yet been updated.")

class DefaultTextBox(element.Element):
    def __init__(self,
                 pos_x: int,
                 pos_y: int,
                 width: int = 300,
                 height: int = 200,
                 text: str = "Hi!",
                 text_size: int = 10,
                 font: str = "consolas",
                 theme: themes.Theme = None,
                 antialiasing: bool = True,
                 line_spacing: int = 5,
                 rounded_corners_amount: int = None,
                 margin_from_left: int = 10,
                 margin_from_right: int = 10,
                 margin_from_top: int = 10,
                 ) -> None:

        super().__init__()

        if check_tools.is_num(pos_x):
            self._pos_x = int(pos_x)
        else:
            raise ValueError("position values must be of type <int> or <float>.")

        if check_tools.is_num(pos_y):
            self._pos_y = int(pos_y)
        else:
            raise ValueError("position values must be of type <int> or <float>.")

        if check_tools.is_num(width):
            self._width = int(width)
        else:
            raise ValueError("size values must be of type <int> or <float>.")

        if check_tools.is_num(height):
            self._height = int(height)
        else:
            raise ValueError("size values must be of type <int> or <float>.")

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

        if check_tools.is_str(font):
            self._font = pygame.font.SysFont(font, self._text_size)
        else:
            raise ValueError("font argument must be of type <str>.")

        if theme is None:
            self._theme = themes.get_default_theme()
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

        if check_tools.is_num(line_spacing):
            self._line_spacing = int(line_spacing)
        else:
            raise ValueError("line_spacing argument must be of type <int> or <float>.")

        if check_tools.is_num(margin_from_left):
            self._margin_from_left = int(margin_from_left)
        else:
            raise ValueError("margin arguments must be of type <int> or <float>.")

        if check_tools.is_num(margin_from_right):
            self._margin_from_right = int(margin_from_right)
        else:
            raise ValueError("margin arguments must be of type <int> or <float>.")

        if check_tools.is_num(margin_from_top):
            self._margin_from_top = int(margin_from_top)
        else:
            raise ValueError("margin arguments must be of type <int> or <float>.")

        if not check_tools.is_num(rounded_corners_amount) and rounded_corners_amount is not None:
            raise ValueError("rounded_corners_amount must be of type <int> or <float>.")

        if rounded_corners_amount is None:
            self._rounded_corners_amount = -1
        elif rounded_corners_amount == -1:
            self._rounded_corners_amount = -1
        else:
            self._rounded_corners_amount = int(rounded_corners_amount)

        self._create_colors()

        self._rect = pygame.rect.Rect(self._pos_x, self._pos_y, self._width, self._height)

        self._processed_text = ""

        self._create_lines()

    def _create_colors(self) -> None:
        self._color_text = self._theme.on_surface
        self._color_surface = self._theme.surface

    def _create_lines(self) -> None:
        words = self._text.split(" ")  # Get words by separating spaces.

        # loop through words, create a surface, check the width to see if it is out of the box.
        # if it is, make the current word to a new line.

        text = ""

        current_width = 0
        current_line = ""
        whitespace_width = self._font.render(" ", self._antialiasing, (0, 0, 0)).get_width()

        for i, word in enumerate(words):
            # create word surface (for width)
            word_surface = self._font.render(word, self._antialiasing, (0, 0, 0))

            if "\n" in word:
                text += current_line

                current_line = ""

                # add it to current line
                current_line += word + " "

                # reset and add to current width
                current_width = self._margin_from_left
                current_width += word_surface.get_width() + whitespace_width

                if i == len(words) - 1:
                    text += current_line + "\n"

            # check if it is in the restrictions
            elif word_surface.get_width() + current_width + self._margin_from_left < self._width - self._margin_from_right:
                # it is not outside the textbox

                # add it to current line
                current_line += word + " "

                # add to current width
                current_width += word_surface.get_width() + whitespace_width

            else:
                # current word is outside the textbox

                # add to _lines and reset current lines
                text += current_line + "\n"

                current_line = ""

                # add it to current line
                current_line += word + " "

                # reset and add to current width
                current_width = self._margin_from_left
                current_width += self._font.render(current_line, True, (0, 0, 0)).get_width()

        text += current_line + "\n"

        self._processed_text = text

    def update(self, dt: float) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self._color_surface, self._rect, border_radius=self._rounded_corners_amount)

        for i, line in enumerate(self._processed_text.split("\n")):
            text_surface = self._font.render(line, self._antialiasing, self._color_text)
            screen.blit(text_surface, (self._pos_x + self._margin_from_left, self._pos_y +
                                       (text_surface.get_height() + self._line_spacing) * i + self._margin_from_top))

    @property
    def text(self) -> str:
        return self._processed_text

    @text.setter
    def text(self, text: str) -> None:
        if check_tools.is_str(text):
            self._text = str(text)
            self._create_lines()
        else:
            raise ValueError("text argument must be of type <str>.")
