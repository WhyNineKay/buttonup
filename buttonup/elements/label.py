from typing import SupportsInt, Optional, Union

import pygame

from .element import SizedElement, ThemedElement, FontElement, Element
from .. import constants
from ..theme import ThemeLike, load_default_theme
from ..buttonup_types import FontLike, RGB, ColorLike
from ..utils import ColorTools


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

        self._text_surface: pygame.Surface = None
        self._render_text_surface()

    def _parse_text(self, text: str) -> str:
        if not isinstance(text, str):
            raise TypeError(f"Label text must be of type 'str', not '{type(text)}'.")
        return text

    def _update_text(self, text: str) -> None:
        self._text = self._parse_text(text)

    def _update_colors(self) -> None:
        self._text_color = self._theme.label_theme.text_color

    def _render_text_surface(self) -> None:
        self._text_surface = self._font.render(self._text, True, self._text_color)
        self._update_dimensions(
            width=self._text_surface.get_width(),
            height=self._text_surface.get_height()
        )

    def _update_font_and_size(self, font: FontLike, font_size: SupportsInt) -> None:
        super()._update_font_and_size(font, font_size)
        self._render_text_surface()

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._text_surface, (self._x, self._y))

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = self._parse_text(text)
        self._render_text_surface()

    @property
    def text_color(self) -> RGB:
        return self._text_color

    @text_color.setter
    def text_color(self, color: ColorLike) -> None:
        if ColorTools.is_color(color):
            self._text_color = ColorTools.to_rgb(color)
            self._render_text_surface()
        else:
            raise ValueError(f"Label text color must be a valid color, not '{color}'.")

    def debug_draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (255, 0, 0), self._rect, 1)

    @property
    def text_surface(self) -> pygame.Surface:
        return self._text_surface
