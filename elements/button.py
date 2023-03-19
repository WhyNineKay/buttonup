import logging
from typing import Callable, Union, Tuple, Any

import pygame
from ..themes.themes import Theme
from .. import constants as c
from ..elements.element import NewElement
from ..themes import themes
from ..utility.program_tools import check_tools, text_align, color_tools

log = logging.getLogger(__name__)


class DefaultButton(NewElement):
    """
    A button that has many features, such as:
     - text alignment
     - theme support
     - on hover, and on click
     and more!

    """
    def __init__(self, pos_x: int, pos_y: int, width: int = None, height: int = None,
                 theme: Union[themes.Theme, str] = None, text: str = None, text_size: int = None,
                 font: Union[pygame.font.Font, str] = None, text_antialiasing: bool = None,
                 text_alignment_x: c.Alignments = None, text_alignment_y: c.Alignments = None,
                 text_alignment_margin: int = None, border_radius: int = None,
                 border_width: int = None, on_click_function: Callable = None,
                 on_click_function_args: list | tuple = None, on_click_function_kwargs: dict = None,
                 on_hover_function: Callable = None, on_hover_function_args: list | tuple = None,
                 on_hover_function_kwargs: dict = None, cursor_change_hover: bool = None) -> None:
        """
        :param pos_x: The x position of the button.
        :param pos_y: The y position of the button.
        :param width: The width of the button.
        :param height: The height of the button.

        :param theme: The theme of the button, defaults to the current project theme. (globs.project_theme)
        :param text: The text that is displayed on the button. Defaults to an empty string ('').

        :param text_size: The size of the text in pixels, defaults to 20.
        :param font: The font of the text.
        :param text_antialiasing: Choose whether the text is anti-aliased. Defaults to True.

        :param text_alignment_x: The alignment of the text on the button in the x direction. Defaults to
            Alignments.CENTER.

        :param text_alignment_y: The alignment of the text on the button in the y direction. Defaults to
            Alignments.CENTER.

        :param text_alignment_margin: The margin of the text in pixels, from the top-left of the button.
            Defaults to 10.

        :param border_radius: How much the corners are rounded on the button, in pixels.

        :param border_width: The width of the border of the button, in pixels.

        :param on_click_function: The function to be called when the button is clicked. Defaults to None.
        :param on_click_function_args: The args to put into the on_click_function when called. Defaults to [].
        :param on_click_function_kwargs: The kwargs to put into the on_click_function when called. Defaults to {}.
        :param on_hover_function: The function to be called when the button is hovered. Defaults to None.
        :param on_hover_function_args: The args to put into the on_hover_function when called. Defaults to [].
        :param on_hover_function_kwargs: The kwargs to put into the on_hover_function when called. Defaults to {}.

        :param cursor_change_hover: Sets whether when you hover your mouse over the button, it sets your cursor
            to the pointer hand.

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
            height = 40
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

        # -------- ALIGNMENT

        if text_alignment_x is None:
            text_alignment_x = c.Alignments.CENTER
        else:
            if not isinstance(text_alignment_x, c.Alignments):
                raise TypeError(f"text_alignment_x must be of type Alignments, not '{type(text_alignment_x)}'.")

        self._text_alignment_x = text_alignment_x

        if text_alignment_y is None:
            text_alignment_y = c.Alignments.CENTER
        else:
            if not isinstance(text_alignment_y, c.Alignments):
                raise TypeError(f"text_alignment_y must be of type Alignments, not '{type(text_alignment_y)}'.")

        self._text_alignment_y = text_alignment_y

        if text_alignment_margin is None:
            text_alignment_margin = 5

        else:
            if not check_tools.is_int(text_alignment_margin):
                try:
                    text_alignment_margin = int(text_alignment_margin)
                except ValueError:
                    raise TypeError(f"text_alignment_margin must be of type int, not "
                                    f"'{type(text_alignment_margin)}'.")
                else:
                    pass

                if text_alignment_margin < 0:
                    raise ValueError(f"text_alignment_margin must be greater than or equal to 0, not "
                                     f"'{text_alignment_margin}'.")

        self._text_alignment_margin = text_alignment_margin

        # -------- BORDER

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

        if border_width is None:
            border_width = 2

        else:
            if not check_tools.is_int(border_width):
                try:
                    border_width = int(border_width)
                except ValueError:
                    raise TypeError(f"border_width must be of type int, not '{type(border_width)}'.")
                else:
                    pass

                if border_width < 0:
                    raise ValueError(f"border_width must be greater than or equal to 0, not "
                                     f"'{border_width}'.")

        self._border_width = border_width

        # -------- ON CLICK FUNCTIONS

        if on_click_function is None:
            self._on_click_function = c.dummy_function
        else:
            if not callable(on_click_function):
                raise TypeError(f"on_click_function must be callable, not '{type(on_click_function)}'.")

            self._on_click_function = on_click_function

        # args / kwargs

        if on_click_function_args is None:
            self._on_click_function_args = ()
        else:
            if not check_tools.is_tuple(on_click_function_args):
                raise TypeError(f"on_click_function_args must be of type tuple, not '{type(on_click_function_args)}'.")
            else:
                self._on_click_function_args = on_click_function_args

        if on_click_function_kwargs is None:
            self._on_click_function_kwargs = {}
        else:
            if not check_tools.is_dict(on_click_function_kwargs):
                raise TypeError(
                    f"on_click_function_kwargs must be of type dict, not '{type(on_click_function_kwargs)}'.")
            else:
                self._on_click_function_kwargs = on_click_function_kwargs

        # -------- ON HOVER FUNCTIONS

        if on_hover_function is None:
            self._on_hover_function = c.dummy_function

        else:
            if not callable(on_hover_function):
                raise TypeError(f"on_hover_function must be callable, not '{type(on_hover_function)}'.")

            self._on_hover_function = on_hover_function

        # args / kwargs

        if on_hover_function_args is None:
            self._on_hover_function_args = ()

        else:
            if not isinstance(on_hover_function_args, tuple):
                raise TypeError(f"on_hover_function_args must be of type tuple, not '{type(on_hover_function_args)}'.")
            else:
                self._on_hover_function_args = on_hover_function_args

        if on_hover_function_kwargs is None:
            self._on_hover_function_kwargs = {}

        else:
            if not check_tools.is_dict(on_hover_function_kwargs):
                raise TypeError(
                    f"on_hover_function_kwargs must be of type dict, not '{type(on_hover_function_kwargs)}'.")
            else:
                self._on_hover_function_kwargs = on_hover_function_kwargs

        # -------- CURSOR

        if cursor_change_hover is None:
            cursor_change_hover = True

        else:
            if not check_tools.is_bool(cursor_change_hover):
                raise TypeError(f"cursor_change_hover must be of type bool, not '{type(cursor_change_hover)}'.")

        self._cursor_change_hover = cursor_change_hover

        # -------- MISC

        self._rect = pygame.rect.Rect(self._pos_x, self._pos_y, self._width, self._height)

        self._previously_pressed = False
        self._previously_hovered = False

        self._state = c.States.INACTIVE

        self._text_surface = None
        self._text_rect = None

        self._changed_cursor = False

        # -------- COLORS

        # disabled
        self._color_disabled: str | None = None
        self._color_disabled_outline: str | None = None
        self._color_disabled_text: str | None = None
        # pressed
        self._color_pressed: str | None = None
        self._color_pressed_outline: str | None = None
        self._color_pressed_text: str | None = None
        # hovered
        self._color_hovered: str | None = None
        self._color_hovered_outline: str | None = None
        self._color_hovered_text: str | None = None
        # base
        self._color_base: str | None = None
        self._color_outline: str | None = None
        self._color_text: str | None = None

        self._load_colors()

        self._render_text_surface()

    def _render_text_surface(self) -> None:
        """
        Renders/reloads the text surface.
        """

        color_table = {
            c.States.DISABLED: self._color_disabled_text,
            c.States.PRESSED: self._color_pressed_text,
            c.States.HOVERED: self._color_hovered_text,
            c.States.INACTIVE: self._color_text
        }


        self._text_surface = self._font.render(self._text, self._text_antialiasing, color_table[self._state])
        self._text_rect = self._text_surface.get_rect()

        # Align the text, using the text_align.align_new function.
        self._text_rect = text_align.align_new(
            area_rect=self._rect,
            text_rect=self._text_rect,
            text_align_x=self._text_alignment_x,
            text_align_y=self._text_alignment_y,
            margin=self._text_alignment_margin
        )

    def _load_colors(self) -> None:
        """
        Loads the colors.
        """

        # Disabled
        self._color_disabled = self._theme.button_data.disabled
        self._color_disabled_outline = self._theme.button_data.outline_disabled
        self._color_disabled_text = self._theme.button_data.text_disabled
        # Pressed
        self._color_pressed = self._theme.button_data.pressed
        self._color_pressed_outline = self._theme.button_data.outline_pressed
        self._color_pressed_text = self._theme.button_data.text_pressed
        # Hovered
        self._color_hovered = self._theme.button_data.hovered
        self._color_hovered_outline = self._theme.button_data.outline_hovered
        self._color_hovered_text = self._theme.button_data.text_hovered
        # Base
        self._color_outline = self._theme.button_data.outline_base
        self._color_text = self._theme.button_data.text_base
        self._color_base = self._theme.button_data.base

    def update(self, dt: float) -> None:
        """
        Update the element.
        :param dt: Delta Time.
        """

        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        previous_state = self._state

        # Determine the current state of the button
        if self._state == c.States.DISABLED:
            self._state = c.States.DISABLED

        elif self._rect.collidepoint(mouse_pos):
            if mouse_buttons[0]:
                if self._state == c.States.HOVERED or self._previously_pressed:
                    self._state = c.States.PRESSED
                else:
                    self._state = c.States.INACTIVE
            else:
                self._state = c.States.HOVERED
        else:
            self._state = c.States.INACTIVE

        # Call the hover function if the button has just been hovered over
        if self._state == c.States.HOVERED and \
                not self._previously_hovered and \
                self._on_hover_function and \
                previous_state != c.States.PRESSED:
            self._on_hover_function(*self._on_hover_function_args, **self._on_hover_function_kwargs)

        # Call the click function if the button has just been clicked
        if self._state == c.States.PRESSED and \
                not self._previously_pressed and \
                self._on_click_function:
            self._on_click_function(*self._on_click_function_args, **self._on_click_function_kwargs)

        # Update the previous states
        self._previously_pressed = self._state == c.States.PRESSED
        self._previously_hovered = self._state == c.States.HOVERED

        if self._state != previous_state:
            self._render_text_surface()

        # Change the cursor to a hand icon if the button is active
        self._change_cursor()

    def _change_cursor(self) -> None:
        """
        Changes the cursor to a hand icon if the button is active.
        """

        if self._state in (c.States.HOVERED, c.States.PRESSED) and self._cursor_change_hover:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            self._changed_cursor = True

        elif self._changed_cursor:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self._changed_cursor = False

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the element to the given surface.
        :param surface: The surface to draw on.
        """

        if self._state == c.States.DISABLED:
            pygame.draw.rect(surface, self._color_disabled, self._rect, border_radius=self._border_radius)
            pygame.draw.rect(surface, self._color_disabled_outline, self._rect, border_radius=self._border_radius,
                             width=self._border_width)
            surface.blit(self._text_surface, self._text_rect)

        elif self._state == c.States.PRESSED:
            pygame.draw.rect(surface, self._color_pressed, self._rect, border_radius=self._border_radius)
            pygame.draw.rect(surface, self._color_pressed_outline, self._rect, border_radius=self._border_radius,
                             width=self._border_width)
            surface.blit(self._text_surface, self._text_rect)

        elif self._state == c.States.HOVERED:
            pygame.draw.rect(surface, self._color_hovered, self._rect, border_radius=self._border_radius)
            pygame.draw.rect(surface, self._color_hovered_outline, self._rect, border_radius=self._border_radius,
                             width=self._border_width)
            surface.blit(self._text_surface, self._text_rect)

        else:
            pygame.draw.rect(surface, self._color_base, self._rect, border_radius=self._border_radius)
            pygame.draw.rect(surface, self._color_outline, self._rect, border_radius=self._border_radius,
                             width=self._border_width)
            surface.blit(self._text_surface, self._text_rect)

    def _update_position(self, x: int, y: int) -> None:
        """
        Updates the position of the button.
        """

        self._pos_x = x
        self._pos_y = y
        self._rect.x = self._pos_x
        self._rect.y = self._pos_y

        self._render_text_surface()  # aligns and renders the text surface

    @property
    def pos_x(self) -> int:
        return self._pos_x

    @pos_x.setter
    def pos_x(self, x: int) -> None:

        # type checks
        if not check_tools.is_int(x):
            raise TypeError(f"pos_x must be of type int, not '{type(x)}'.")

        self._update_position(x, self._pos_y)

    @property
    def pos_y(self) -> int:
        return self._pos_y

    @pos_y.setter
    def pos_y(self, y: int) -> None:

        # type checks
        if not check_tools.is_int(y):
            raise TypeError(f"pos_y must be of type int, not '{type(y)}'.")

        self._update_position(self._pos_x, y)

    @property
    def pos(self) -> Tuple[int, int]:
        return self._pos_x, self._pos_y

    @pos.setter
    def pos(self, pos: Tuple[int, int]) -> None:
        if not check_tools.is_pos(pos):
            raise TypeError(f"pos must be of type tuple, not '{type(pos)}'.")

        self._update_position(pos[0], pos[1])

    @property
    def center(self) -> Tuple[int, int]:
        return self._rect.center

    @center.setter
    def center(self, center: Tuple[int, int]) -> None:

        # type checks

        if not check_tools.is_tuple(center):
            raise TypeError(f"center must be of type tuple, not '{type(center)}'.")

        # it is tuple

        if len(center) != 2:
            raise ValueError(f"center must contain two integers, not '{center}'.")

        # it is len 2

        if not check_tools.is_int(center[0]) or not check_tools.is_int(center[1]):
            raise TypeError(f"center must contain two integers, not '{center}'.")

        # it is int tuple

        self._rect.center = center
        self._update_position(self._rect.x, self._rect.y)

    @property
    def centerx(self) -> int:
        return self._rect.centerx

    @centerx.setter
    def centerx(self, x: int) -> None:

        # type checks
        if not check_tools.is_int(x):
            raise TypeError(f"centerx must be of type int, not '{type(x)}'.")

        self._rect.centerx = x
        self._update_position(self._rect.x, self._rect.y)

    @property
    def centery(self) -> int:
        return self._rect.centery

    @centery.setter
    def centery(self, y: int) -> None:

        # type checks
        if not check_tools.is_int(y):
            raise TypeError(f"centery must be of type int, not '{type(y)}'.")

        self._rect.centery = y
        self._update_position(self._rect.x, self._rect.y)

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, width: int) -> None:

        # type checks
        if not check_tools.is_int(width):
            raise TypeError(f"width must be of type int, not '{type(width)}'.")

        self._width = width
        self._rect.width = self._width
        self._render_text_surface()

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, height: int) -> None:
        # type checks
        if not check_tools.is_int(height):
            raise TypeError(f"height must be of type int, not '{type(height)}'.")

        self._height = height
        self._rect.height = self._height
        self._render_text_surface()

    @property
    def size(self) -> Tuple[int, int]:
        return self._width, self._height

    @size.setter
    def size(self, size: Tuple[int, int]) -> None:
        # type checks

        if not check_tools.is_tuple(size):
            raise TypeError(f"size must be of type tuple, not '{type(size)}'.")

        # it is tuple

        if len(size) != 2:
            raise ValueError(f"size must contain two integers, not '{size}'.")

        # it is len 2

        if not check_tools.is_int(size[0]) or not check_tools.is_int(size[1]):
            raise TypeError(f"size must contain two integers, not '{size}'.")

        # it is int tuple

        self._width = size[0]
        self._height = size[1]
        self._rect.width = self._width
        self._rect.height = self._height
        self._render_text_surface()

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        # type checks
        if not check_tools.is_str(text):
            raise TypeError(f"text must be of type str, not '{type(text)}'.")

        self._text = text
        self._render_text_surface()

    @property
    def text_size(self) -> int:
        return self._text_size

    @text_size.setter
    def text_size(self, text_size: int) -> None:
        # type checks
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
        # type checks
        if not check_tools.is_bool(text_antialiasing):
            raise TypeError(f"text_antialiasing must be of type bool, not '{type(text_antialiasing)}'.")

        self._text_antialiasing = text_antialiasing
        self._render_text_surface()

    @property
    def theme(self) -> Theme:
        return self._theme

    @theme.setter
    def theme(self, value: themes.Theme | str) -> None:
        """
        Sets the theme and reloads the colours.
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
            log.error("Unreachable code? Defaulting to default theme.")
            theme = themes.get_default_theme()

        self._theme = theme

        self._load_colors()
        self._render_text_surface()

    @property
    def border_radius(self) -> int:
        return self._border_radius

    @border_radius.setter
    def border_radius(self, border_radius: int) -> None:
        # type checks

        if check_tools.is_int(border_radius):
            if border_radius < 0:
                raise ValueError(f"border_radius must be greater than or equal to 0, not "
                                 f"'{border_radius}'.")
            else:
                self._border_radius = border_radius

        else:
            try:
                int(border_radius)

            except ValueError:
                raise ValueError(f"border_radius must be of type int, not '{type(border_radius)}'.")

            else:
                if int(border_radius) < 0:
                    raise ValueError(f"border_radius must be greater than or equal to 0, not "
                                     f"'{int(border_radius)}'.")
                else:
                    self._border_radius = int(border_radius)

    @property
    def border_width(self) -> int:
        return self._border_width

    @border_width.setter
    def border_width(self, border_width: int) -> None:
        # type checks

        if check_tools.is_int(border_width):
            if border_width < 0:
                raise ValueError(f"border_width must be greater than or equal to 0, not "
                                 f"'{border_width}'.")
            else:
                self._border_width = border_width

        else:
            try:
                int(border_width)

            except ValueError:
                raise ValueError(f"border_width must be of type int, not '{type(border_width)}'.")

            else:
                if int(border_width) < 0:
                    raise ValueError(f"border_width must be greater than or equal to 0, not "
                                     f"'{int(border_width)}'.")
                else:
                    self._border_width = int(border_width)

    @property
    def on_click_function(self) -> Callable:
        return self._on_click_function

    @property
    def on_hover_function(self) -> Callable:
        return self._on_hover_function

    @property
    def cursor_change_hover(self) -> bool:
        return self._cursor_change_hover

    @cursor_change_hover.setter
    def cursor_change_hover(self, value: bool) -> None:
        if not check_tools.is_bool(value):
            raise TypeError(f"cursor_change_hover must be of type bool, not '{type(value)}'.")

        self._cursor_change_hover = bool(value)

    @property
    def state(self) -> c.States:
        return self._state

    @state.setter
    def state(self, value: c.States) -> None:
        try:
            value = c.States(value)
        except ValueError:
            raise TypeError(f"state must be of type States, not '{type(value)}'.")

        self._state = value

        self._render_text_surface()

    @property
    def color_base(self) -> Any:
        return self._color_base

    @color_base.setter
    def color_base(self, value: Any) -> None:
        if not color_tools.is_color(value):
            raise TypeError(f"color_base must be rgb, hex, or pygame.Color, not '{value}'.")

        self._color_base = value

    @property
    def color_outline(self) -> Any:
        return self._color_outline

    @color_outline.setter
    def color_outline(self, value: Any) -> None:
        if not color_tools.is_color(value):
            raise TypeError(f"color_outline must be rgb, hex, or pygame.Color, not '{value}'.")

        self._color_outline = value

    @property
    def color_text(self) -> Any:
        return self._color_text

    @color_text.setter
    def color_text(self, value: Any) -> None:
        if not color_tools.is_color(value):
            raise TypeError(f"color_text must be rgb, hex, or pygame.Color, not '{value}'.")

        self._color_text = value

        self._render_text_surface()

    @property
    def color_disabled(self) -> Any:
        return self._color_disabled

    @color_disabled.setter
    def color_disabled(self, value: Any) -> None:
        if not color_tools.is_color(value):
            raise TypeError(f"color_disabled must be rgb, hex, or pygame.Color, not '{value}'.")

        self._color_disabled = value

    @property
    def color_disabled_outline(self) -> Any:
        return self._color_disabled_outline

    @color_disabled_outline.setter
    def color_disabled_outline(self, value: Any) -> None:
        if not color_tools.is_color(value):
            raise TypeError(f"color_disabled_outline must be rgb, hex, or pygame.Color, not '{value}'.")

        self._color_disabled_outline = value

    @property
    def color_disabled_text(self) -> Any:
        return self._color_disabled_text

    @color_disabled_text.setter
    def color_disabled_text(self, value: Any) -> None:
        if not color_tools.is_color(value):
            raise TypeError(f"color_disabled_text must be rgb, hex, or pygame.Color, not '{value}'.")

        self._color_disabled_text = value

        self._render_text_surface()

    @property
    def color_pressed(self) -> Any:
        return self._color_pressed

    @color_pressed.setter
    def color_pressed(self, value: Any) -> None:
        if not color_tools.is_color(value):
            raise TypeError(f"color_pressed must be rgb, hex, or pygame.Color, not '{value}'.")

        self._color_pressed = value

    @property
    def color_pressed_outline(self) -> Any:
        return self._color_pressed_outline

    @color_pressed_outline.setter
    def color_pressed_outline(self, value: Any) -> None:
        if not color_tools.is_color(value):
            raise TypeError(f"color_pressed_outline must be rgb, hex, or pygame.Color, not '{value}'.")

        self._color_pressed_outline = value

    @property
    def color_hovered(self) -> Any:
        return self._color_hovered

    @color_hovered.setter
    def color_hovered(self, value: Any) -> None:
        if not color_tools.is_color(value):
            raise TypeError(f"color_hovered must be rgb, hex, or pygame.Color, not '{value}'.")

        self._color_hovered = value

    @property
    def color_hovered_outline(self) -> Any:
        return self._color_hovered_outline

    @color_hovered_outline.setter
    def color_hovered_outline(self, value: Any) -> None:
        if not color_tools.is_color(value):
            raise TypeError(f"color_hovered_outline must be rgb, hex, or pygame.Color, not '{value}'.")

        self._color_hovered_outline = value

