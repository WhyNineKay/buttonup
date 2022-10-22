import pygame

import constants
from Utility.globs import globs
from Utility.program_tools import color_tools, text_align, check_tools
from typing import Callable
from Themes import themes


class SquareButton:
    def __init__(self,
                 pos_x: int,
                 pos_y: int,
                 width: int = 75,
                 height: int = 75,
                 theme: themes.Theme = None,
                 text: str = "hi",
                 text_size: int = 20,
                 font: str = "consolas",
                 text_align_x: str = "center",
                 text_align_y: str = "center",
                 text_align_margin: int = 15,
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
        :raises ValueError: If any of the parameters are not the correct type.
        """

        # Perform type checks for all the arguments

        if isinstance(pos_x, int):
            self._pos_x = pos_x
        else:
            raise ValueError("position values must be of type <int>.")

        if isinstance(pos_y, int):
            self._pos_y = pos_y
        else:
            raise ValueError("position values must be of type <int>.")

        if isinstance(width, int):
            self._width = width
        else:
            raise ValueError("size values must be of type <int>.")

        if isinstance(height, int):
            self._height = height
        else:
            raise ValueError("size values must be of type <int>.")

        if isinstance(text, str):
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

        if isinstance(text_size, int):
            self._text_size = text_size
        else:
            raise ValueError("text_size argument must be of type <int>.")

        if not isinstance(text_align_x, str):
            raise ValueError("text_align arguments must be of type <str>.")

        if not isinstance(text_align_y, str):
            raise ValueError("text_align arguments must be of type <str>.")

        if isinstance(text_align_margin, int):
            if text_align_margin < 0:
                raise ValueError("text_align_margin must be greater than 0. (x > 0)")
            self._text_align_margin = text_align_margin
        else:
            raise ValueError("text_align_margin must be of type <int>.")

        if isinstance(font, str):
            self._font = pygame.font.SysFont(font, self._text_size)
        else:
            raise ValueError("font argument must be of type <str>.")

        if on_click_function is None:
            self._on_click_function = self._default_on_click_function
        elif isinstance(on_click_function, Callable):
            self._on_click_function = on_click_function
        else:
            raise ValueError("on_click_function must be of type <function> or None.")

        self._rect: pygame.Rect = pygame.Rect(self._pos_x, self._pos_y, self._width, self._height)
        self._on_hover_change_cursor: bool = on_hover_change_cursor
        self._on_disabled_change_cursor: bool = on_disabled_change_cursor
        self._text_surface = self._font.render(self._text, True, (255, 255, 255))

        # will raise ValueError if text_align_x or text_align_y is not correct
        self._text_rect = text_align.align(self._rect, self._text_surface.get_rect(),
                                           text_align_y, text_align_x,
                                           margin=self._text_align_margin)

        self._state_hovered = False
        self._state_pressed = False
        self._state_disabled = False
        self._prev_mouse_clicked = False
        self._changed_cursor = False

        # Create colors.
        self._create_colors()

        if rounded_corners_amount is None:
            self._rounded_corners_amount = int(((self._width / constants.SMART_ROUNDED_CORNERS_MULTIPLIER)
                                                + (self._height / constants.SMART_ROUNDED_CORNERS_MULTIPLIER)) / 2)
        elif self._rounded_corners_amount == -1:
            self._rounded_corners_amount = -1
        else:
            self._rounded_corners_amount = rounded_corners_amount

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
                                                                        self._theme.brightness_offsets["hovered-outline"])

    def render(self, screen: pygame.Surface) -> None:
        """Draw to the pygame surface."""

        # If the button is disabled, draw the disabled color.
        if self._state_disabled:
            pygame.draw.rect(screen, self._color_disabled, self._rect, border_radius=self._rounded_corners_amount)

            if self._text:  # if text is not ""
                # Render the text.
                self._text_surface = self._font.render(self._text, True, self._color_disabled_text)

                # Blit to the screen
                screen.blit(self._text_surface, self._text_rect)

        # If the button is not disabled, draw the normal color.
        elif self._state_pressed:
            pygame.draw.rect(screen, self._color_pressed, self._rect, border_radius=self._rounded_corners_amount)

            if self._text:  # if text is not ""
                # Render the text.
                self._text_surface = self._font.render(self._text, True, self._theme.on_surface)

                # Blit to the screen
                screen.blit(self._text_surface, self._text_rect)

        elif self._state_hovered:

            pygame.draw.rect(screen, self._color_hovered, self._rect, border_radius=self._rounded_corners_amount)

            pygame.draw.rect(screen, self._color_hovered_outline, self._rect, 3,
                             border_radius=self._rounded_corners_amount)

            if self._text:  # if text is not ""
                # Render the text.
                self._text_surface = self._font.render(self._text, True, self._theme.on_surface)

                # Blit to the screen
                screen.blit(self._text_surface, self._text_rect)

        else:
            pygame.draw.rect(screen, self._theme.surface, self._rect,
                             border_radius=self._rounded_corners_amount)

            if self._text:  # if text is not ""
                # Render the text.
                self._text_surface = self._font.render(self._text, True, self._theme.on_surface)

                # Blit to the screen
                screen.blit(self._text_surface, self._text_rect)

    def update(self, dt: float) -> None:
        """
        Update the element.
        :param dt: Delta Time.
        """

        mouse_pos = pygame.mouse.get_pos()
        mouse_keys = pygame.mouse.get_pressed()

        if not self._state_disabled:
            if self._rect.collidepoint(mouse_pos):
                if not self._prev_mouse_clicked:
                    if mouse_keys[0]:
                        self._state_pressed = True
                        self._state_hovered = False
                    else:
                        self._state_pressed = False
                        self._state_hovered = True
                else:
                    self._state_hovered = False
                    self._state_pressed = False
            else:
                self._state_hovered = False
                self._state_pressed = False

        self._prev_mouse_clicked = mouse_keys[0]

        self._change_cursor()

        if self._state_pressed and not self._prev_mouse_clicked and self._on_click_function is not None:
            self._on_click_function()

    def _change_cursor(self) -> None:
        """
        Changes the cursor.
        Called every update()
        """

        mouse_pos = pygame.mouse.get_pos()

        if self._state_disabled and self._rect.collidepoint(mouse_pos) and self._on_disabled_change_cursor:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_NO)
            self._changed_cursor = True

        elif (self._state_hovered or self._state_pressed) and self._on_hover_change_cursor:
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
    def on_click_function(self) -> Callable | None:
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

        if not isinstance(value, Callable):
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

        if self._state_disabled:
            return "DISABLED"
        elif self._state_pressed:
            return "PRESSED"
        elif self._state_hovered:
            return "HOVERED"
        else:
            return "INACTIVE"

    @state.setter
    def state(self, state: str | int) -> None:
        """
        Set the state of the button.
        You can use a string of the state or an int (0-3).
        You can also use the first letter of the worded states.
        States str: ["inactive", "hovered", "pressed", "disabled"]
        States str: ["i", "h", "p", "d"]
        States int: [0, 1, 2, 3] | ["0", "1", "2", "3"]

        :raises ValueError: If the state is none of the possible states.
        """

        states = {
            "inactive": ["inactive", "i", 0, "0"],
            "hovered": ["hovered", "h", 1, "1"],
            "pressed": ["pressed", "p", 2, "2"],
            "disabled": ["disabled", "d", 3, "3"]
        }

        found = False

        for s in states.items():
            for sub_s in s[1]:
                if state == sub_s:
                    found = True
                    state = s[0]
                    break

        if not found:
            raise ValueError("state is not valid.")


        if state == "inactive":
            return
        elif state == "hovered":
            self._state_hovered = True
        elif state == "pressed":
            self._state_pressed = True
        elif state == "disabled":
            self._state_disabled = True


    @staticmethod
    def _default_on_click_function() -> None:
        print(f"Button clicked")
