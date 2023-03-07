from ..Utility.program_tools import check_tools, color_tools
from ..Elements.element import NewElement
from ..Themes import themes
from typing import Union, Tuple, Any
import pygame


class DefaultLabel(NewElement):
    """
    Simple label.

    Makes using text in pygame a lot easier to use and manage.
    """

    def __init__(self,
                 pos_x: int, pos_y: int, theme: Union[themes.Theme, str] = None, text: str = None,
                 text_size: int = None, font: Union[pygame.font.Font, str] = None, text_antialiasing: bool = None,
                 ) -> None:
        """
        :param pos_x: X position of the label.
        :param pos_y: Y position of the label.
        :param theme: Theme to use for the label.
        :param text: Text to display.
        :param text_size: Size of the text. Will become redundant if font parameter is used.
        :param font: Font to use for the text.
        :param text_antialiasing: Whether to use antialiasing for the text.

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

        # -------- TEXT

        if text is None:
            text = ""
        else:
            if not check_tools.is_str(text):
                raise TypeError(f"text must be of type str, not '{type(text)}'.")

        self._text = text

        if text_size is None:
            text_size = 20
        else:
            if not check_tools.is_int(text_size):
                try:
                    text_size = int(text_size)
                except ValueError:
                    raise TypeError(f"text_size must be of type int, not '{type(text_size)}'.")
                else:
                    pass

        self._text_size = text_size

        # -------- FONT

        self._font_name: str | None = None

        if font is None:
            # font = self.theme.font (not implemented yet)
            self._font_name = "Consolas"
            font = pygame.font.SysFont(self._font_name, self._text_size)

        elif isinstance(font, str):
            self._font_name = font

            if font in pygame.font.get_fonts():
                font = pygame.font.SysFont(font, self._text_size)
            else:
                raise ValueError(f"font '{font}' does not exist in the system fonts.")
        else:

            if not isinstance(font, pygame.font.Font):
                raise TypeError(f"font must be of type pygame.font.Font, not '{type(font)}'.")

        self._font = font

        if check_tools.is_bool(text_antialiasing):
            self._text_antialiasing = text_antialiasing

        elif text_antialiasing is None:
            self._text_antialiasing = True

        else:
            raise TypeError(f"text_antialiasing must be of type bool, not '{type(text_antialiasing)}'.")

        # -------- COLORS

        self._color_text: str | None = None

        # -------- MISC

        self._text_surface: pygame.Surface | None = None
        self._text_rect: pygame.Rect | None = None

        self._load_colors()
        self._render_text_surface()

    def _load_colors(self) -> None:
        """
        Loads the colors for the label.
        """

        self._color_text = self.theme.label_data.text_base

    def _render_text_surface(self) -> None:
        """
        Renders/reloads the text surface.
        """

        self._text_surface = self._font.render(self._text, self._text_antialiasing, self._color_text)
        self._text_rect = self._text_surface.get_rect()

        self._text_rect.x = self._pos_x
        self._text_rect.y = self._pos_y

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the label onto the surface.

        :param surface: Surface to draw the label onto.
        """

        surface.blit(self._text_surface, self._text_rect)

    @property
    def pos_x(self) -> int:
        return self._pos_x

    @property
    def pos_y(self) -> int:
        return self._pos_y

    @property
    def pos(self) -> Tuple[int, int]:
        return self._pos_x, self._pos_y

    @pos_x.setter
    def pos_x(self, value: int) -> None:
        if not check_tools.is_int(value):
            raise TypeError(f"pos_x must be of type int, not '{type(value)}'.")

        self._pos_x = value
        self._render_text_surface()

    @pos_y.setter
    def pos_y(self, value: int) -> None:
        if not check_tools.is_int(value):
            raise TypeError(f"pos_y must be of type int, not '{type(value)}'.")

        self._pos_y = value
        self._render_text_surface()

    @pos.setter
    def pos(self, pos: Tuple[int, int]) -> None:

        # type checks

        if not check_tools.is_tuple(pos):
            raise TypeError(f"pos must be of type tuple, not '{type(pos)}'.")

        # it is tuple

        if len(pos) != 2:
            raise ValueError(f"pos must contain two integers, not '{pos}'.")

        # it is len 2

        if not check_tools.is_int(pos[0]) or not check_tools.is_int(pos[1]):
            raise TypeError(f"pos must contain two integers, not '{pos}'.")

        # it is int tuple

        self._pos_x = pos[0]
        self._pos_y = pos[1]

        self._render_text_surface()

    @property
    def center_x(self) -> int:
        return self._text_rect.centerx

    @property
    def center_y(self) -> int:
        return self._text_rect.centery

    @property
    def center(self) -> Tuple[int, int]:
        return self._text_rect.center

    @center_x.setter
    def center_x(self, value: int) -> None:
        if not check_tools.is_int(value):
            raise TypeError(f"center_x must be of type int, not '{type(value)}'.")

        self._text_rect.centerx = value
        self._pos_x = self._text_rect.x

        self._render_text_surface()

    @center_y.setter
    def center_y(self, value: int) -> None:
        if not check_tools.is_int(value):
            raise TypeError(f"center_y must be of type int, not '{type(value)}'.")

        self._text_rect.centery = value
        self._pos_y = self._text_rect.y

        self._render_text_surface()

    @center.setter
    def center(self, pos: Tuple[int, int]) -> None:

        # type checks

        if not isinstance(pos, tuple):
            raise TypeError(f"center must be of type tuple, not '{type(pos)}'.")

        # it is tuple

        if len(pos) != 2:
            raise ValueError(f"center must contain two integers, not '{pos}'.")

        # it is len 2

        if not check_tools.is_int(pos[0]) or not check_tools.is_int(pos[1]):
            raise TypeError(f"center must contain two integers, not '{pos}'.")

        # it is int tuple

        self._text_rect.center = pos
        self._pos_x = self._text_rect.x
        self._pos_y = self._text_rect.y

        self._render_text_surface()

    @property
    def theme(self) -> themes.Theme:
        return self._theme

    @theme.setter
    def theme(self, theme: themes.Theme) -> None:
        if not isinstance(theme, themes.Theme):
            raise TypeError(f"theme must be of type Theme, not '{type(theme)}'.")

        self._theme = theme
        self._load_colors()
        self._render_text_surface()

    @property
    def width(self) -> int:
        return self._text_rect.width

    @property
    def height(self) -> int:
        return self._text_rect.height

    @property
    def size(self) -> Tuple[int, int]:
        return self._text_rect.size

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        if not check_tools.is_str(text):
            raise TypeError(f"text must be of type str, not '{type(text)}'.")

        self._text = text
        self._render_text_surface()

    @property
    def text_size(self) -> int:
        return self._text_size

    @text_size.setter
    def text_size(self, text_size: int) -> None:
        if not check_tools.is_int(text_size):
            raise TypeError(f"text_size must be of type int, not '{type(text_size)}'.")

        self._text_size = text_size

        if self._font_name is not None:
            self._font = pygame.font.SysFont(self._font_name, self._text_size)

        self._render_text_surface()

    @property
    def text_antialiasing(self) -> bool:
        return self._text_antialiasing

    @text_antialiasing.setter
    def text_antialiasing(self, text_antialiasing: bool) -> None:
        if not check_tools.is_bool(text_antialiasing):
            raise TypeError(f"text_antialiasing must be of type bool, not '{type(text_antialiasing)}'.")

        self._text_antialiasing = text_antialiasing
        self._render_text_surface()

    @property
    def color_text(self) -> Any:
        return self._color_text

    @color_text.setter
    def color_text(self, value: Any) -> None:
        if not color_tools.is_color(value):
            raise TypeError(f"color_hovered must be rgb, hex, or pygame.Color, not '{value}'.")

        self._color_text = value
        self._render_text_surface()
