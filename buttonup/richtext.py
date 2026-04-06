from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import SupportsInt, Dict, Tuple, List, Union

import pygame

from . import constants
from .buttonup_types import RGB, FontLike, ColorLike
from .elements.element import FontElement
from .utils import ColorTools


@dataclass
class TextStyle:
    color: RGB = None
    background_color: RGB = None
    bold: bool = None
    italic: bool = None
    underline: bool = None
    strikethrough: bool = None

    def get_bold(self) -> bool:
        return self.bold if self.bold is not None else False

    def get_italic(self) -> bool:
        return self.italic if self.italic is not None else False

    def get_underline(self) -> bool:
        return self.underline if self.underline is not None else False

    def get_strikethrough(self) -> bool:
        return self.strikethrough if self.strikethrough is not None else False

    def merge(self, other: 'TextStyle') -> 'TextStyle':
        """
        Merge another TextStyle into this one, with the other style taking precedence for any non-None attributes.
        """
        return TextStyle(
            color=other.color if other.color is not None else self.color,
            background_color=other.background_color if other.background_color is not None else self.background_color,
            bold=other.bold if other.bold is not None else self.bold,
            italic=other.italic if other.italic is not None else self.italic,
            underline=other.underline if other.underline is not None else self.underline,
            strikethrough=other.strikethrough if other.strikethrough is not None else self.strikethrough
        )


@dataclass(slots=True)
class TextSpan:
    text: str
    style: TextStyle


@dataclass(slots=True)
class RenderFormText:
    span: TextSpan
    surface: pygame.Surface
    width: int


class RichText(FontElement):
    def __init__(self, spans: list[TextSpan], font: FontLike = None, font_size: SupportsInt = None, default_text_color: ColorLike = None) -> None:
        if font is None:
            font = constants.DEFAULT_FONT_NAME

        if font_size is None:
            font_size = constants.DEFAULT_FONT_SIZE

        super().__init__(font=font, font_size=font_size)

        if default_text_color is None:
            default_text_color = (255, 255, 255)

        self._default_text_color = self._parse_text_color(default_text_color)

        self._spans = spans

    def _parse_text_color(self, color: ColorLike) -> RGB:
        if ColorTools.is_color(color):
            return ColorTools.to_rgb(color)
        else:
            raise TypeError(f"Default text color must be a valid color format, not '{color}'.")

    def _set_font_parameters(self, style: TextStyle) -> None:
        self._font.set_bold(style.get_bold())
        self._font.set_italic(style.get_italic())
        self._font.set_underline(style.get_underline())

    @staticmethod
    def _apply_strikethrough(surface: pygame.Surface, color: RGB) -> None:
        strike_width = max(1, surface.get_height() // 15)
        strike_y = surface.get_height() // 2

        pygame.draw.line(surface, color, (0, strike_y), (surface.get_width(), strike_y), strike_width)

    def render(self) -> List[RenderFormText]:
        rendered_forms: List[RenderFormText] = []

        for span in self._spans:
            self._set_font_parameters(span.style)
            text_surface = self._font.render(
                span.text,
                True,
                span.style.color if span.style.color is not None else self._default_text_color,
                span.style.background_color
            )

            if span.style.get_strikethrough():
                self._apply_strikethrough(text_surface, self._default_text_color)

            rendered_forms.append(RenderFormText(
                span=span,
                surface=text_surface,
                width=text_surface.get_width()
            ))

        return rendered_forms

    def _update_font_and_size(self, font: FontLike, font_size: SupportsInt) -> None:
        super()._update_font_and_size(font, font_size)
        self.render()


class RichTextParser(ABC):
    @abstractmethod
    def parse(self, text: str) -> List[TextSpan]:
        pass


class InlineDeveloperParser(RichTextParser):
    """
    A simple parser for custom inline markup.

    This is based on the typical Minecraft formatting codes using § or in this case & as the marker, followed by a
    single character code for the style.

    For example:
    &cHello &6world&r!

    would produce "Hello " in red, "world" in gold, and "!" in the default style.

    The legacy codes are implemented by the following mapping:
    - &0: Black
    - &1: Dark Blue
    - &2: Dark Green
    - &3: Dark Cyan
    - &4: Dark Red
    - &5: Dark Magenta
    - &6: Gold
    - &7: Gray
    - &8: Dark Gray
    - &9: Blue
    - &a: Green
    - &b: Cyan
    - &c: Red
    - &d: Magenta
    - &e: Yellow
    - &f: White
    - &l: Bold
    - &o: Italic
    - &n: Underline
    - &m: Strikethrough
    - &r: Reset to default style

    Furthermore, the parser is extended to implement following additional features:

    - &&: Escaped ampersand, produces a literal '&' character without changing the style. Only works if the set
    character is '&'.
    - &B: Background color, followed by a single character code. For example, &B4 would set the background color to dark
    red.
    - &x: Followed by 6 hexadecimal digits, sets the text color to the specified RGB value. For example, &xFF0000
    - &X: Followed by 6 hexadecimal digits, sets the background color to the specified RGB value.
    - &!: Rainbow text
    """

    DEFAULT_OPERATION_CHARACTER = "&"

    COLOR_CODE_MAPPING: Dict[str, RGB] = {
        "0": (0, 0, 0),  # Black
        "1": (0, 0, 170),  # Dark Blue
        "2": (0, 170, 0),  # Dark Green
        "3": (0, 170, 170),  # Dark Cyan
        "4": (170, 0, 0),  # Dark Red
        "5": (170, 0, 170),  # Dark Magenta
        "6": (255, 170, 0),  # Gold
        "7": (170, 170, 170),  # Gray
        "8": (85, 85, 85),  # Dark Gray
        "9": (85, 85, 255),  # Blue
        "a": (85, 255, 85),  # Green
        "b": (85, 255, 255),  # Cyan
        "c": (255, 85, 85),  # Red
        "d": (255, 85, 255),  # Magenta
        "e": (255, 255, 85),  # Yellow
        "f": (255, 255, 255),  # White
    }

    def __init__(self, operation_character: str = None) -> None:
        if operation_character is None:
            operation_character = self.DEFAULT_OPERATION_CHARACTER

        self._operation_character = self._parse_operation_character(operation_character)

    @staticmethod
    def _parse_operation_character(char: str) -> str:
        if not isinstance(char, str) or len(char) != 1:
            raise ValueError(f"Operation character must be a single character string, not '{char}'.")
        return char

    @staticmethod
    def _peek(text: str, index: int) -> str:
        if index < len(text):
            return text[index]
        return ""

    def parse(self, text: str) -> List[TextSpan]:
        # 1. ABSTRACT INTO [TextStyle, str, TextStyle, str, ...]
        styles_and_text: List[Union[TextStyle, str]] = []

        current_text = ""

        in_rainbow = False

        rainbow_index = 0
        rainbow_index_colors = [
            (255, 0, 0),    # Red
            (255, 127, 0),  # Orange
            (255, 255, 0),  # Yellow
            (0, 255, 0),    # Green
            (0, 255, 255),  # Cyan
            (0, 0, 255),    # Blue
            (127, 0, 255)   # Magenta
        ]

        i = 0
        while i < len(text):
            current_char = text[i]

            if current_char == self._operation_character:
                next_char = self._peek(text, i + 1)

                if next_char == self._operation_character:
                    current_text += self._operation_character
                    i += 2

                elif next_char in self.COLOR_CODE_MAPPING:
                    if current_text:
                        styles_and_text.append(current_text)
                        current_text = ""

                    color = self.COLOR_CODE_MAPPING[next_char]
                    styles_and_text.append(TextStyle(color=color))
                    i += 2

                    in_rainbow = False

                elif next_char == "r":
                    if current_text:
                        styles_and_text.append(current_text)
                        current_text = ""

                    styles_and_text.append(TextStyle(color=self.COLOR_CODE_MAPPING["f"], background_color=None, bold=None, italic=None, underline=None, strikethrough=None))
                    i += 2

                    in_rainbow = False

                elif next_char == "B":
                    if current_text:
                        styles_and_text.append(current_text)
                        current_text = ""

                    color_code_char = self._peek(text, i + 2)

                    if color_code_char in self.COLOR_CODE_MAPPING:
                        background_color = self.COLOR_CODE_MAPPING[color_code_char]
                        styles_and_text.append(TextStyle(background_color=background_color))
                        i += 3
                    else:
                        i += 2

                    in_rainbow = False

                elif next_char == "x":
                    if current_text:
                        styles_and_text.append(current_text)
                        current_text = ""

                    if i + 7 < len(text):
                        hex_color = text[i + 2:i + 8]

                        if ColorTools.is_hex(hex_color):
                            color = ColorTools.to_rgb(hex_color)
                            styles_and_text.append(TextStyle(color=color))
                            i += 8
                        else:
                            i += 2

                    else:
                        i += 2

                    in_rainbow = False

                elif next_char == "X":
                    if current_text:
                        styles_and_text.append(current_text)
                        current_text = ""

                    if i + 7 < len(text):
                        hex_color = text[i + 2:i + 8]

                        if ColorTools.is_hex(hex_color):
                            background_color = ColorTools.to_rgb(hex_color)
                            styles_and_text.append(TextStyle(background_color=background_color))
                            i += 8
                        else:
                            i += 2
                    else:
                        i += 2

                elif next_char == "l":
                    if current_text:
                        styles_and_text.append(current_text)
                        current_text = ""

                    styles_and_text.append(TextStyle(bold=True))
                    i += 2

                elif next_char == "o":
                    if current_text:
                        styles_and_text.append(current_text)
                        current_text = ""

                    styles_and_text.append(TextStyle(italic=True))
                    i += 2

                elif next_char == "n":
                    if current_text:
                        styles_and_text.append(current_text)
                        current_text = ""

                    styles_and_text.append(TextStyle(underline=True))
                    i += 2

                elif next_char == "m":
                    if current_text:
                        styles_and_text.append(current_text)
                        current_text = ""

                    styles_and_text.append(TextStyle(strikethrough=True))
                    i += 2

                elif next_char == "!":
                    if current_text:
                        styles_and_text.append(current_text)
                        current_text = ""

                    i += 2

                    in_rainbow = True

                else:
                    current_text += current_char
                    i += 1

            else:
                if in_rainbow:
                    # Placeholder for rainbow color cycling logic
                    styles_and_text.append(TextStyle(color=rainbow_index_colors[rainbow_index % len(rainbow_index_colors)]))
                    rainbow_index += 1
                    current_text += current_char
                    styles_and_text.append(current_text)
                    i += 1
                    current_text = ""
                else:
                    current_text += current_char
                    i += 1

        if current_text:
            styles_and_text.append(current_text)

        # 2. COLLAPSE INTO TextSpan
        spans: List[TextSpan] = []

        current_style = TextStyle()

        for item in styles_and_text:
            if isinstance(item, TextStyle):
                current_style = current_style.merge(item)
            else:
                spans.append(TextSpan(text=item, style=current_style))

        return spans


