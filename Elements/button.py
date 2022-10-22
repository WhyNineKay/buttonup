from .. Utility.program_tools import color_tools, text_align, check_tools
from .. Utility.globs import globs
from .. Themes import themes
from .. Elements.element import Element
from typing import Callable, Any
from .. import constants as c
import pygame


class DefaultButton(Element):
    def __init__(self,
                 pos_x: int,
                 pos_y: int,
                 width: int = None,
                 height: int = None,
                 theme: themes.Theme = None,
                 text: str = None,
                 text_size: int = None,
                 font: str = None,
                 text_align_x: str = "center",
                 text_align_y: str = "center",
                 text_align_margin: int = 15,
                 antialiasing: bool = True,
                 rounded_corners_amount: int = None,
                 on_click_function: None or Callable = None,
                 on_hover_change_cursor: bool = True,
                 on_disabled_change_cursor: bool = False) -> None:
        """
        A button that can be clicked and has a text on it.
        :param pos_x: The x position of the button.
        :param pos_y: The y position of the button.
        :param width: The width of the button.
        :param height: The height of the button.
        :param theme: Theme object. Defaults to globs.project_theme.
        :param text: The text on the button.
        :param text_size: The size of the text.
        :param text_align_x: The x position of the text. ("left", "center", "right")
        :param text_align_y: The y position of the text. ("top", "center", "bottom")
        :param text_align_margin: The margin between the text and the button.
        :param rounded_corners_amount: Rounded corners amount. Set to -1 for no roundness, or any integer greater
                                       than 1 for rounded corners. If set to None it will calculate rounded corners
                                       amount automatically from width and height.
        :param on_click_function: The function to call when the button is clicked.
        :param on_hover_change_cursor: If the cursor should change when the mouse is hovering over the button.
        :param on_disabled_change_cursor: If the cursor should change when the button is disabled.
        :raises ValueError: If any of the parameters are not the correct type or specification.
        """

        super().__init__()

        # Perform type checks for all the arguments

        self._color_hovered_outline = None
        self._color_disabled_text = None
        self._color_disabled = None
        self._color_pressed = None
        self._color_hovered = None

        if check_tools.is_num(pos_x):
            self._pos_x = int(pos_x)
        else:
            raise ValueError("position values must be of type <int> or <float>.")

        if check_tools.is_num(pos_y):
            self._pos_y = int(pos_y)
        else:
            raise ValueError("position values must be of type <int> or <float>.")

        if width is None:
            self._width = 75
        elif check_tools.is_num(width):
            self._width = int(width)
        else:
            raise ValueError("size values must be of type <int> or <float>.")

        if height is None:
            self._height = 75
        elif check_tools.is_num(height):
            self._height = int(height)
        else:
            raise ValueError("size values must be of type <int> or <float>.")

        if text is None:
            self._text = c.DEFAULT_TEXT
        elif check_tools.is_str(text):
            self._text = str(text)
        else:
            raise ValueError("text argument must be of type <str>.")

        if theme is None:
            self._theme = globs.project_theme
        elif isinstance(theme, themes.Theme):
            self._theme = theme
        elif isinstance(theme, str):
            self._theme = themes.get_theme(str(theme))
        else:
            raise ValueError("theme argument must be of type <str> or <Theme>.")

        if text_size is None:
            self._text_size = 20
        elif check_tools.is_negative(text_size):
            raise ValueError("text_size argument must be a positive int.")
        elif check_tools.is_num(text_size):
            self._text_size = int(text_size)
        else:
            raise ValueError("text_size argument must be of type <int> or <float>.")

        if not check_tools.is_str(text_align_x):
            raise ValueError("text_align arguments must be of type <str>.")

        if not check_tools.is_str(text_align_y):
            raise ValueError("text_align arguments must be of type <str>.")

        if check_tools.is_num(text_align_margin):
            if text_align_margin < 0:
                raise ValueError("text_align_margin must be greater than 0. (x > 0)")
            self._text_align_margin = int(text_align_margin)
        else:
            raise ValueError("text_align_margin must be of type <int>.")

        if font is None:
            self._font = pygame.font.SysFont("consolas", self._text_size)
        elif check_tools.is_str(font):
            self._font = pygame.font.SysFont(font, self._text_size)
        elif isinstance(font, pygame.font.Font):
            self._font = font
        else:
            raise ValueError("font argument must be of type <str>.")

        if on_click_function is None:
            self._on_click_function = self._default_on_click_function
        elif isinstance(on_click_function, Callable):
            self._on_click_function = on_click_function
        else:
            raise ValueError("on_click_function must be of type <function> or None.")

        self._rect: pygame.Rect = pygame.rect.Rect(self._pos_x, self._pos_y, self._width, self._height)

        if check_tools.is_bool(on_hover_change_cursor):
            self._on_hover_change_cursor: bool = on_hover_change_cursor
        else:
            raise ValueError("on_hover_change_cursor must be of type <bool>.")

        if check_tools.is_bool(on_disabled_change_cursor):
            self._on_disabled_change_cursor: bool = on_disabled_change_cursor
        else:
            raise ValueError("on_disabled_change_cursor must be of type <bool>.")

        if check_tools.is_bool(antialiasing):
            self._antialiasing = antialiasing
        else:
            raise ValueError("antialiasing argument must be of type <bool>.")

        self._text_surface = self._font.render(self._text, self._antialiasing, (255, 255, 255))

        # will raise ValueError if text_align_x or text_align_y is not correct
        self._text_rect = text_align.align(self._rect, self._text_surface.get_rect(),
                                           text_align_y, text_align_x,
                                           margin=self._text_align_margin)

        self._text_align_y = text_align_y
        self._text_align_x = text_align_x

        self._prev_pressed = False
        self._changed_cursor = False
        self._state = c.STATE_INACTIVE

        # Create colors.
        self._create_colors()

        if not check_tools.is_num(rounded_corners_amount) and rounded_corners_amount is not None:
            raise ValueError("rounded_corners_amount must be of type <int> or <float>.")

        if rounded_corners_amount is None:
            self._rounded_corners_amount = int(((self._width / c.SMART_ROUNDED_CORNERS_MULTIPLIER)
                                                + (self._height / c.SMART_ROUNDED_CORNERS_MULTIPLIER)) / 2)
        elif rounded_corners_amount == -1:
            self._rounded_corners_amount = -1
        else:
            self._rounded_corners_amount = int(rounded_corners_amount)

    def _create_colors(self) -> None:
        """
        Creates the colors.
        This function is mainly to stop calculating stuff in the update() method.
        """
        self._color_disabled = color_tools.change_hex_brightness(self._theme.surface,
                                                                 self._theme.brightness_offsets["disabled"])
        self._color_disabled_text = color_tools.change_hex_brightness(self._theme.on_surface,
                                                                      self._theme.brightness_offsets["disabled-text"])
        self._color_pressed = color_tools.change_hex_brightness(self._theme.surface,
                                                                self._theme.brightness_offsets["pressed"])
        self._color_hovered = color_tools.change_hex_brightness(self._theme.surface,
                                                                self._theme.brightness_offsets["hovered"])

        self._color_hovered_outline = color_tools.change_hex_brightness(self._theme.surface,
                                                                        self._theme.brightness_offsets[
                                                                            "hovered-outline"])
        self._color_text = self._theme.on_surface
        self._color_base = self._theme.surface

    def render(self, screen: pygame.Surface) -> None:
        """Draw to the pygame surface."""

        # If the button is disabled, draw the disabled color.
        if self._state == c.STATE_DISABLED:
            if self._color_disabled is not None:
                pygame.draw.rect(screen, self._color_disabled, self._rect, border_radius=self._rounded_corners_amount)

            if self._text and self._color_disabled is not None:  # if text is not ""
                # Render the text.
                self._text_surface = self._font.render(self._text, self._antialiasing, self._color_disabled_text)

                # Blit to the screen
                screen.blit(self._text_surface, self._text_rect)

        # If the button is not disabled, draw the normal color.
        elif self._state == c.STATE_PRESSED:
            if self._color_pressed is not None:
                pygame.draw.rect(screen, self._color_pressed, self._rect, border_radius=self._rounded_corners_amount)

            if self._text and self._color_text is not None:  # if text is not ""
                # Render the text.
                self._text_surface = self._font.render(self._text, self._antialiasing, self._color_text)

                # Blit to the screen
                screen.blit(self._text_surface, self._text_rect)

        elif self._state == c.STATE_HOVERED:
            if self._color_hovered is not None:
                pygame.draw.rect(screen, self._color_hovered, self._rect, border_radius=self._rounded_corners_amount)

            if self._color_hovered_outline is not None:
                pygame.draw.rect(screen, self._color_hovered_outline, self._rect, 3,
                                 border_radius=self._rounded_corners_amount)

            if self._text and self._color_text is not None:  # if text is not ""
                # Render the text.
                self._text_surface = self._font.render(self._text, self._antialiasing, self._color_text)

                # Blit to the screen
                screen.blit(self._text_surface, self._text_rect)

        else:

            if self._color_base is not None:
                pygame.draw.rect(screen, self._color_base, self._rect,
                                 border_radius=self._rounded_corners_amount)

            if self._text and self._color_text is not None:  # if text is not ""
                # Render the text.
                self._text_surface = self._font.render(self._text, self.antialiasing, self._color_text)

                # Blit to the screen
                screen.blit(self._text_surface, self._text_rect)

    def update(self, dt: float) -> None:
        """
        Update the element.
        :param dt: Delta Time.
        """

        self._prev_pressed = self._state == c.STATE_PRESSED

        mouse_pos = pygame.mouse.get_pos()
        mouse_keys = pygame.mouse.get_pressed()

        if self._state != c.STATE_DISABLED:

            if self._rect.collidepoint(mouse_pos):
                if mouse_keys[0]:
                    if not self._state == c.STATE_HOVERED:
                        if not self._prev_pressed:
                            self._state = c.STATE_INACTIVE
                        else:
                            self._state = c.STATE_PRESSED
                    else:
                        self._state = c.STATE_PRESSED
                else:
                    self._state = c.STATE_HOVERED

            else:
                self._state = c.STATE_INACTIVE
        else:
            self.state = c.STATE_DISABLED

        self._change_cursor()

        if self._state == c.STATE_PRESSED and not self._prev_pressed and self._on_click_function is not None:
            self._on_click_function()

    def _change_cursor(self) -> None:
        """
        Changes the cursor.
        Called every update()
        """

        mouse_pos = pygame.mouse.get_pos()

        if self._state == c.STATE_DISABLED and self._rect.collidepoint(mouse_pos) and self._on_disabled_change_cursor:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_NO)
            self._changed_cursor = True

        elif (self._state == c.STATE_HOVERED or self._state == c.STATE_PRESSED) and self._on_hover_change_cursor:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            self._changed_cursor = True

        elif self._changed_cursor:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self._changed_cursor = False

    def event(self, event: pygame.event.Event) -> None:
        """
        Handle a pygame event.
        Call this in the main event loop.
        """
        pass

    @property
    def text(self) -> str:
        """
        Gets the current text.
        """
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        """
        Set the current text.
        Must be a string value.
        :param text: Text Value.
        :raises ValueError: If the text is not a string.
        """

        if not isinstance(text, str):
            raise ValueError("text argument must be of type <str>.")

        self._text = text

    @property
    def on_click_function(self) -> None or Callable:
        """
        Returns the current on click function.
        Returns None if there is no current on_click_function or if it is the default one.
        :returns Callable: The on_click_function
        :returns None: If there is no on_click_function or if it is the default one.
        """

        if self._on_click_function == self._default_on_click_function:
            return

        elif self._on_click_function is None:
            return

        else:
            return self._on_click_function

    @on_click_function.setter
    def on_click_function(self, value: Callable) -> None:
        """
        Set the on_click_function.
        :raises ValueError: If the value is not a Callable function.
        """

        if value is None:
            self._on_click_function = None

        elif not isinstance(value, Callable):
            raise ValueError("on_click_function must be of type <function>.")

        else:
            self._on_click_function = value

    @property
    def state(self) -> str:
        """
        Gets the current state of the button.
        Return states: ["inactive", "hovered", "pressed", "disabled"]
        :returns state: Returns the worded string representation of the state.
        """
        return self._state

    @state.setter
    def state(self, state: str) -> None:
        """
        Set the state of the button. Use from the constants.states

        :param state: The requested state. Must be one of: ["disabled", "hovered", "pressed", "inactive"]
        :raises ValueError: If the state is none of the possible states.
        """

        states = ["disabled", "hovered", "pressed", "inactive"]

        state = state.lower()

        if state in states:
            self._state = state
        else:
            raise ValueError("state is not valid.")

    @staticmethod
    def _default_on_click_function() -> None:
        print(f"Button clicked")

    def set_color(self, key: str, color: Any) -> None:
        """
        Set a certain color of the button.

        :param key: The requested color. Must be one of: ['disabled', 'disabled_text', 'pressed',
                    'hovered', 'hovered_outline']. It is not case sensitive.
        :param color: The color to set.
        """

        # check if key is correct
        colors = ['disabled', 'disabled_text', 'pressed',
                  'hovered', 'hovered_outline']

        if key.lower() not in colors:
            raise ValueError(f"Invalid key '{key}'.", "invalid_key")

        if not color_tools.is_color(color):
            raise ValueError(f"Invalid color '{color}'.", "invalid_color")

        color = color.lower()

        if color == "disabled":
            self._color_disabled = color
        elif color == "disabled_text":
            self._color_disabled_text = color
        elif color == "pressed":
            self._color_pressed = color
        elif color == "hovered":
            self._color_hovered = color
        elif color == "hovered_outline":
            self._color_hovered_outline = color

    @property
    def pos(self) -> tuple[int, int]:
        """
        Gets a tuple of the position of the button.
        :return pos: The position.
        """
        return self._pos_x, self._pos_y

    @pos.setter
    def pos(self, value: tuple[int, int]) -> None:
        """
        Sets the position of the button.
        :raises ValueError: If the position is invalid.
        """

        if not check_tools.is_pos(value):
            raise ValueError(f"position must be tuple[int, int] not '{value}'.")

        self._pos_x = value[0]
        self._pos_y = value[1]
        self._rect.topleft = value

        self._text_rect = text_align.align(self._rect, self._text_surface.get_rect(),
                                           self._text_align_y, self._text_align_x,
                                           margin=self._text_align_margin)

    @property
    def x(self) -> int:
        """
        Gets the x value of the button.
        """
        return self._pos_x

    @x.setter
    def x(self, value: int) -> None:
        """
        Set the x value of the button
        :raises ValueError: If the value is not an int or float.
        """
        if check_tools.is_num(value):
            self.pos = int(value), self.pos[1]
        else:
            raise ValueError("x value must be of type <int> or <float>.")

    @property
    def y(self) -> int:
        """
        Gets the x value of the button.
        """
        return self._pos_y

    @y.setter
    def y(self, value: int) -> None:
        """
        Set the x value of the button
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

    def __str__(self) -> str:
        return f"<DefaultButton, pos: {self.pos}, state: {self.state}>"

