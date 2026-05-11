from dataclasses import dataclass
from typing import SupportsInt, Optional, List

import pygame

from .element import SizedElement, ThemedElement, FontElement, Element
from .. import constants
from ..buttonup_types import FontLike, RGB, ColorLike
from ..theme import ThemeLike, load_default_theme
from ..utils import ColorTools


@dataclass
class TextFragment:
    x: int
    y: int
    text_surface: pygame.Surface


class Label(SizedElement, ThemedElement, FontElement, Element):
    """
    A text element that can be used to display static text.
    """

    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 text: str = None,
                 theme: ThemeLike = None,
                 font: FontLike = None,
                 font_size: SupportsInt = None
                 ) -> None:
        self._text_fragments: List[TextFragment] = []

        SizedElement.__init__(self, x=x, y=y, width=0, height=0)

        if theme is None:
            theme = load_default_theme()

        self._text_color: Optional[RGB] = None

        ThemedElement.__init__(self, theme=theme)

        if text is None:
            text = ""

        self._text = self._parse_text(text)

        if font_size is None:
            font_size = constants.DEFAULT_FONT_SIZE

        if font is None:
            font = constants.DEFAULT_FONT_NAME

        FontElement.__init__(self, font=font, font_size=font_size)

        self._render_text_surfaces()

    def _parse_text(self, text: str) -> str:
        if not isinstance(text, str):
            raise TypeError(f"Label text must be of type 'str', not '{type(text)}'.")
        return text

    def _update_text(self, text: str) -> None:
        self._text = self._parse_text(text)

    def _init_colors(self) -> None:
        self._text_color = self._theme.label_theme.text_color

    def _update_colors(self) -> None:
        self._init_colors()

    def _get_lines(self) -> List[str]:
        lines = self._text.splitlines()

        if len(lines) == 0:
            lines = [""]

        return lines

    def _render_text_surfaces(self) -> None:
        self._text_fragments = []

        lines = self._get_lines()

        max_width: int = 0
        running_height: int = 0

        for i, line in enumerate(lines):
            current_text_surface = self._font.render(line, True, self._text_color)

            self._text_fragments.append(
                TextFragment(x=self._x, y=self._y + running_height, text_surface=current_text_surface)
            )

            max_width = max(max_width, current_text_surface.get_width())
            running_height += current_text_surface.get_height()

        self._update_dimensions(max_width, running_height)

    def _update_position(self, x: SupportsInt, y: SupportsInt) -> None:
        super()._update_position(x, y)

        running_height: int = 0

        for fragment in self._text_fragments:
            fragment.x = self._x
            fragment.y = self._y + running_height

            running_height += fragment.text_surface.get_height()

    def _update_font_and_size(self, font: FontLike, font_size: SupportsInt) -> None:
        super()._update_font_and_size(font, font_size)
        self._render_text_surfaces()

    def draw(self, surface: pygame.Surface) -> None:
        for fragment in self._text_fragments:
            surface.blit(fragment.text_surface, (fragment.x, fragment.y))

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = self._parse_text(text)
        self._render_text_surfaces()

    @property
    def text_color(self) -> RGB:
        return self._text_color

    @text_color.setter
    def text_color(self, color: ColorLike) -> None:
        if ColorTools.is_color(color):
            self._text_color = ColorTools.to_rgb(color)
            self._render_text_surfaces()
        else:
            raise ValueError(f"Label text color must be a valid color, not '{color}'.")

    def debug_draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (255, 0, 0), self._rect, 1)

    @property
    def text_surfaces(self) -> List[pygame.Surface]:
        return [fragment.text_surface for fragment in self._text_fragments]

    @property
    def text_fragments(self) -> List[TextFragment]:
        return self._text_fragments
