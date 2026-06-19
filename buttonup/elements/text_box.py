"""
TextBox.

Display text, and wrap against bounds.

Flow:
1. TextBox is initialized with text and a font.
2. TextBox will pre-render text into words, and calculate how to wrap them based on the width of the TextBox.
3. It will then combine the words into lines, and render each line to a surface.

Potential Problems:
1. If words are too long to fit on a line, they will overflow.
2. Text may overflow vertically if there are too many lines to fit in the height of the TextBox.
3. If the text or font changes, the TextBox will need to re-render everything, which may be expensive.

overflow_behavior: CLIP | ELLIPSIS
wrap_behavior: WORD | CHARACTER
"""
import re
from typing import Optional, SupportsInt, List

import pygame

from ..theme import TextBoxTheme
from .. import constants
from ..buttonup_types import FontLike
from ..elements.element import ResizableElement, ThemedElement, BorderedElement, FontElement, Element
from ..theme import ThemeLike, load_default_theme
from ..utils import ParsingTools
from enum import Enum, auto
from dataclasses import dataclass


ELLIPSIS_STRING = "..."


class TextOverflowBehavior(Enum):
    CLIP = auto()
    ELLIPSIS = auto()


class TextWrapBehavior(Enum):
    WORD = auto()
    CHARACTER = auto()


@dataclass
class LineFragment:
    x: int
    y: int
    text: str
    width: int
    text_surface: Optional[pygame.Surface]


class TextBox(ResizableElement, ThemedElement, BorderedElement, FontElement, Element):
    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 width: Optional[SupportsInt] = None,
                 height: Optional[SupportsInt] = None,
                 theme: Optional[ThemeLike] = None,
                 text: Optional[str] = None,
                 font: Optional[FontLike] = None,
                 font_size: Optional[SupportsInt] = None,
                 border_radius: Optional[SupportsInt] = None,
                 border_width: Optional[SupportsInt] = None,
                 padding_left: Optional[SupportsInt] = None,
                 padding_right: Optional[SupportsInt] = None,
                 padding_top: Optional[SupportsInt] = None,
                 padding_bottom: Optional[SupportsInt] = None,
                 overflow_behavior: Optional[TextOverflowBehavior] = None,
                 wrap_behavior: Optional[TextWrapBehavior] = None
                 ) -> None:
        if width is None:
            width = constants.DEFAULT_TEXTBOX_WIDTH

        if height is None:
            height = constants.DEFAULT_TEXTBOX_HEIGHT

        ResizableElement.__init__(self, x=x, y=y, width=width, height=height)

        if theme is None:
            theme = load_default_theme()

        ThemedElement.__init__(self, theme=theme)

        if font_size is None:
            font_size = constants.DEFAULT_FONT_SIZE

        if font is None:
            font = constants.DEFAULT_FONT_NAME

        FontElement.__init__(self, font=font, font_size=font_size)

        if padding_left is None:
            padding_left = constants.DEFAULT_TEXTBOX_PADDING
        if padding_right is None:
            padding_right = constants.DEFAULT_TEXTBOX_PADDING
        if padding_top is None:
            padding_top = constants.DEFAULT_TEXTBOX_PADDING
        if padding_bottom is None:
            padding_bottom = constants.DEFAULT_TEXTBOX_PADDING

        self._padding_left = self._parse_padding(padding_left, name="padding_left")
        self._padding_right = self._parse_padding(padding_right, name="padding_right")
        self._padding_top = self._parse_padding(padding_top, name="padding_top")
        self._padding_bottom = self._parse_padding(padding_bottom, name="padding_bottom")

        if border_radius is None:
            border_radius = constants.DEFAULT_TEXTBOX_BORDER_RADIUS

        if border_width is None:
            border_width = constants.DEFAULT_TEXTBOX_BORDER_WIDTH

        BorderedElement.__init__(self, border_radius=border_radius, border_width=border_width)

        if text is None:
            text = ""

        self._text = self._parse_text(text)

        if overflow_behavior is None:
            overflow_behavior = TextOverflowBehavior.CLIP

        if wrap_behavior is None:
            wrap_behavior = TextWrapBehavior.WORD

        self._overflow_behavior = self._parse_overflow_behavior(overflow_behavior)
        self._wrap_behavior = self._parse_wrap_behavior(wrap_behavior)

        self._lines: List[LineFragment] = []

        self._textbox_theme = self._theme.text_box_theme.copy()

        self._update_layout()

    def debug_draw(self, surface: pygame.Surface) -> None:
        # Draw padding lines (left, right, top, bottom)
        padding_color = (255, 0, 0)  # Red for debugging

        # Left padding line
        pygame.draw.line(
            surface,
            padding_color,
            (self._x + self._padding_left, self._y),
            (self._x + self._padding_left, self._y + self._height),
            1,
        )

        # Right padding line
        pygame.draw.line(
            surface,
            padding_color,
            (self._x + self._width - self._padding_right, self._y),
            (self._x + self._width - self._padding_right, self._y + self._height),
            1,
        )

        # Top padding line
        pygame.draw.line(
            surface,
            padding_color,
            (self._x, self._y + self._padding_top),
            (self._x + self._width, self._y + self._padding_top),
            1,
        )
        # Bottom padding line
        pygame.draw.line(
            surface,
            padding_color,
            (self._x, self._y + self._height - self._padding_bottom),
            (self._x + self._width, self._y + self._height - self._padding_bottom),
            1,
        )

        # Draw line breaks
        line_color = (0, 255, 0)  # Green for debugging

        for line in self._lines:
            pygame.draw.line(
                surface,
                line_color,
                (line.x, line.y),
                (line.x + line.width, line.y),
                1,
            )

        # Draw bounding box
        bounding_box_color = (0, 0, 255)  # Blue for debugging
        pygame.draw.rect(
            surface,
            bounding_box_color,
            (self._x, self._y, self._width, self._height),
            1,
        )

    def draw(self, surface: pygame.Surface) -> None:
        self._draw_background(surface)
        self._draw_border(surface)
        self._draw_text_lines(surface)


    def _draw_text_lines(self, surface: pygame.Surface) -> None:
        for line in self._lines:
            if line.text_surface is not None:
                surface.blit(line.text_surface, (line.x, line.y))

    def _draw_border(self, surface: pygame.Surface) -> None:
        if self._border_width > 0:
            pygame.draw.rect(
                surface,
                self._textbox_theme.border_color,
                self._rect,
                width=self._border_width,
                border_radius=self._border_radius,
            )

    def _draw_background(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self._textbox_theme.base_color, self._rect, border_radius=self._border_radius)


    def _update_colors(self) -> None:
        super()._update_colors()
        self._textbox_theme = self._theme.text_box_theme.copy()

        self._rerender_line_fragments()

    def _parse_overflow_behavior(self, overflow_behavior: TextOverflowBehavior) -> TextOverflowBehavior:
        if not isinstance(overflow_behavior, TextOverflowBehavior):
            raise ValueError(f"Invalid overflow_behavior: {overflow_behavior}")
        return overflow_behavior

    def _parse_wrap_behavior(self, wrap_behavior: TextWrapBehavior) -> TextWrapBehavior:
        if not isinstance(wrap_behavior, TextWrapBehavior):
            raise ValueError(f"Invalid wrap_behavior: {wrap_behavior}")
        return wrap_behavior

    def _parse_text(self, text: str) -> str:
        if not isinstance(text, str):
            raise TypeError(f"TextBox text must be of type 'str', not '{type(text)}'.")
        return text

    def _parse_padding(self, padding: SupportsInt, name: str) -> int:
        return ParsingTools.parse_non_negative_int(padding, name)

    def _update_layout(self) -> None:
        self._lines.clear()

        inner_width = self.inner_width
        inner_height = self.inner_height

        if inner_width <= 0 or inner_height <= 0:
            return

        if not self._text:
            return

        raw_lines = self._wrap_text(self._text, inner_width)

        line_height = self._font.get_linesize()
        max_lines = inner_height // line_height

        if max_lines <= 0:
            return

        visible_lines = raw_lines[:max_lines]

        if (
            self._overflow_behavior == TextOverflowBehavior.ELLIPSIS
            and len(raw_lines) > max_lines
            and visible_lines
        ):
            visible_lines[-1] = self._ellipsise_line(visible_lines[-1], inner_width)

        y = self._y + self._padding_top

        for line in visible_lines:
            surface = self._render_text(line)
            width = surface.get_width()

            self._lines.append(
                LineFragment(
                    x=self._x + self._padding_left,
                    y=y,
                    text=line,
                    width=width,
                    text_surface=surface,
                )
            )

            y += line_height

    def _rerender_line_fragments(self) -> None:
        """
        Rerender the line fragments without recalculating the entire layout.
        """
        for line in self._lines:
            line.text_surface = self._render_text(line.text)

    @property
    def inner_width(self) -> int:
        return self._width - self._padding_left - self._padding_right

    @property
    def inner_height(self) -> int:
        return self._height - self._padding_top - self._padding_bottom

    def _measure_text(self, text: str) -> int:
        return self._font.size(text)[0]

    def _render_text(self, text: str) -> pygame.Surface:
        return self._font.render(
            text,
            True,
            self._textbox_theme.text_color,
        )

    def _wrap_text(self, text: str, max_width: int) -> List[str]:
        wrapped_lines: List[str] = []

        paragraphs = text.split("\n")

        for paragraph in paragraphs:
            if paragraph == "":
                wrapped_lines.append("")
                continue

            if self._wrap_behavior == TextWrapBehavior.WORD:
                wrapped_lines.extend(
                    self._wrap_paragraph_by_words(paragraph, max_width)
                )
            elif self._wrap_behavior == TextWrapBehavior.CHARACTER:
                wrapped_lines.extend(
                    self._wrap_paragraph_by_characters(paragraph, max_width)
                )
            else:
                raise RuntimeError(f"Unhandled wrap behavior: {self._wrap_behavior}")

        return wrapped_lines

    def _wrap_paragraph_by_words(self, text: str, max_width: int) -> List[str]:
        lines: List[str] = []
        current_line = ""

        tokens = self._split_words_preserving_spaces(text)

        for token in tokens:
            if token == "":
                continue

            candidate = current_line + token

            if self._measure_text(candidate) <= max_width:
                current_line = candidate
                continue

            if current_line:
                lines.append(current_line.rstrip())
                current_line = ""

            token = token.lstrip()

            if self._measure_text(token) <= max_width:
                current_line = token
            else:
                broken_parts = self._break_long_token(token, max_width)

                if broken_parts:
                    lines.extend(broken_parts[:-1])
                    current_line = broken_parts[-1]

        if current_line:
            lines.append(current_line.rstrip())

        return lines

    def _wrap_paragraph_by_characters(self, text: str, max_width: int) -> List[str]:
        lines: List[str] = []
        current_line = ""

        for char in text:
            candidate = current_line + char

            if self._measure_text(candidate) <= max_width:
                current_line = candidate
                continue

            if current_line:
                lines.append(current_line)
                current_line = ""

            if self._measure_text(char) <= max_width:
                current_line = char
            else:
                # Extremely rare, but possible if the box is thinner than one glyph.
                # Store it anyway and let rendering/clipping handle it.
                lines.append(char)

        if current_line:
            lines.append(current_line)

        return lines

    def _break_long_token(self, token: str, max_width: int) -> List[str]:
        parts: List[str] = []
        current_part = ""

        for char in token:
            candidate = current_part + char

            if self._measure_text(candidate) <= max_width:
                current_part = candidate
                continue

            if current_part:
                parts.append(current_part)
                current_part = ""

            if self._measure_text(char) <= max_width:
                current_part = char
            else:
                # Box is too narrow for even one character.
                parts.append(char)

        if current_part:
            parts.append(current_part)

        return parts

    @staticmethod
    def _split_words_preserving_spaces(text: str) -> List[str]:
        return re.findall(r"\S+\s*", text)

    def _ellipsise_line(self, text: str, max_width: int) -> str:
        if self._measure_text(ELLIPSIS_STRING) > max_width:
            return ""

        text = text.rstrip()

        while text and self._measure_text(text + ELLIPSIS_STRING) > max_width:
            text = text[:-1]

        return text + ELLIPSIS_STRING

    @property
    def padding_left(self) -> SupportsInt:
        return self._padding_left

    @padding_left.setter
    def padding_left(self, value: SupportsInt) -> None:
        self._padding_left = self._parse_padding(value, name="padding_left")
        self._update_layout()

    @property
    def padding_right(self) -> SupportsInt:
        return self._padding_right

    @padding_right.setter
    def padding_right(self, value: SupportsInt) -> None:
        self._padding_right = self._parse_padding(value, name="padding_right")
        self._update_layout()

    @property
    def padding_top(self) -> SupportsInt:
        return self._padding_top

    @padding_top.setter
    def padding_top(self, value: SupportsInt) -> None:
        self._padding_top = self._parse_padding(value, name="padding_top")
        self._update_layout()

    @property
    def padding_bottom(self) -> SupportsInt:
        return self._padding_bottom

    @padding_bottom.setter
    def padding_bottom(self, value: SupportsInt) -> None:
        self._padding_bottom = self._parse_padding(value, name="padding_bottom")
        self._update_layout()

    @property
    def overflow_behavior(self) -> TextOverflowBehavior:
        return self._overflow_behavior

    @overflow_behavior.setter
    def overflow_behavior(self, value: TextOverflowBehavior) -> None:
        self._overflow_behavior = self._parse_overflow_behavior(value)
        self._update_layout()

    @property
    def wrap_behavior(self) -> TextWrapBehavior:
        return self._wrap_behavior

    @wrap_behavior.setter
    def wrap_behavior(self, value: TextWrapBehavior) -> None:
        self._wrap_behavior = self._parse_wrap_behavior(value)
        self._update_layout()

    def _update_position(self, x: SupportsInt, y: SupportsInt) -> None:
        super()._update_position(x, y)
        self._update_layout()

    def _update_dimensions(self, width: SupportsInt, height: SupportsInt) -> None:
        super()._update_dimensions(width, height)
        self._update_layout()

    def _update_font_and_size(self, font: FontLike, font_size: SupportsInt) -> None:
        super()._update_font_and_size(font, font_size)
        self._update_layout()

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = self._parse_text(value)
        self._update_layout()

    @property
    def text_box_theme(self) -> TextBoxTheme:
        return self._textbox_theme

