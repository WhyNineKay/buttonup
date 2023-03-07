from ..Utility.program_tools import check_tools, color_tools
from ..Elements.element import Element
from ..Elements import button
from ..Themes import themes
from .. import constants as c

import logging
import pygame

log = logging.getLogger(__name__)


raise NotImplementedError("Slider class has not yet been updated.")

class DefaultSlider(Element):
    def __init__(self,
                 pos_x: int,
                 pos_y: int,
                 rail_width: int = 300,
                 rail_height: int = 10,
                 slider_size: int = 30,
                 theme: themes.Theme = None,
                 rail_rounded_corners_amount: int = 10,
                 slider_rounded_corners_amount: int = 50,
                 on_hover_change_cursor: bool = True,
                 on_disabled_change_cursor: bool = False) -> None:
        """
        A slider that can be interacted with.
        :param pos_x: The x position of the button.
        :param pos_y: The y position of the button.
        :param rail_width: The length of the rail.
        :param rail_height: The height of the rail.
        :param slider_size: The size of the slider grip.
        :param theme: Theme object. Defaults to globs.project_theme.
        :param rail_rounded_corners_amount: Rail rounded corners. Set to -1 or None for no rounded corners.
        :param slider_rounded_corners_amount: Slider grip rounded corners. Set to -1 or None for no rounded corners.
        :param on_hover_change_cursor: If the cursor should change when the mouse is hovering over the slider grip.
        :param on_disabled_change_cursor: If the cursor should change when the slider grip is disabled.
        :raises ValueError: If any of the parameters are not the correct type or specification.
        """

        super().__init__()

        if check_tools.is_num(pos_x):
            self._pos_x = int(pos_x)
        else:
            raise ValueError("position values must be of type <int> or <float>.")

        if check_tools.is_num(pos_y):
            self._pos_y = int(pos_y)
        else:
            raise ValueError("position values must be of type <int> or <float>.")

        if check_tools.is_num(rail_width):
            self._rail_width = int(rail_width)
        else:
            raise ValueError("size values must be of type <int> or <float>.")

        if check_tools.is_num(rail_height):
            self._rail_height = int(rail_height)
        else:
            raise ValueError("size values must be of type <int> or <float>.")

        if check_tools.is_num(slider_size):
            self._slider_size = slider_size
        else:
            raise ValueError("size values must be of type <int> or <float>.")

        if theme is None:
            self._theme = themes.get_default_theme()
        elif isinstance(theme, themes.Theme):
            self._theme = theme
        elif isinstance(theme, str):
            self._theme = themes.get_theme(str(theme))
        else:
            raise ValueError("theme argument must be of type <str> or <Theme>.")

        if not check_tools.is_num(rail_rounded_corners_amount):
            raise ValueError("rounded_corners_amounts must be of type <int> or <float>.")

        if not check_tools.is_num(slider_rounded_corners_amount):
            raise ValueError("rounded_corners_amounts must be of type <int> or <float>.")

        if rail_rounded_corners_amount is None:
            self._rail_rounded_corners_amount = -1
        else:
            self._rail_rounded_corners_amount = int(rail_rounded_corners_amount)

        if slider_rounded_corners_amount is None:
            self._slider_rounded_corners_amount = -1
        else:
            self._slider_rounded_corners_amount = int(rail_rounded_corners_amount)

        if check_tools.is_bool(on_hover_change_cursor):
            self._on_hover_change_cursor: bool = on_hover_change_cursor
        else:
            raise ValueError("on_hover_change_cursor must be of type <bool>.")

        if check_tools.is_bool(on_disabled_change_cursor):
            self._on_disabled_change_cursor: bool = on_disabled_change_cursor
        else:
            raise ValueError("on_disabled_change_cursor must be of type <bool>.")

        self._rail_rect = pygame.Rect = pygame.rect.Rect(self._pos_x, self._pos_y, self._rail_width, self._rail_height)

        self._slider_button = button.DefaultButton(
            self._pos_x, int(self._pos_y - self._slider_size / 2 + self._rail_height / 2), self._slider_size,
            self._slider_size, theme=themes.get_default_theme(), text="", cursor_change_hover=self._on_hover_change_cursor,
            border_radius=self._slider_rounded_corners_amount, on_click_function=self._dummy_function
        )

        self._held = False
        self._changed_cursor = False
        self._percent = 0.0
        self._dont_move = False
        self._moved_direction = None

        self._create_colors()

    def _dummy_function(self) -> None:
        pass

    def _create_colors(self) -> None:
        self._color_rail = color_tools.change_hex_brightness(self._theme.surface,
                                                             self._theme.brightness_offsets["slider-rail"])

    def update(self, dt: float = None) -> None:
        """
        Updates the element.
        :param dt: Delta time. Optional for some elements.
        """

        mouse_pos = pygame.mouse.get_pos()
        mouse_keys = pygame.mouse.get_pressed()

        self._slider_button.update(dt)

        if self._slider_button.state == c.States.PRESSED:
            self._held = True
        elif not mouse_keys[0]:
            self._held = False
            self._dont_move = False

        if self._held:
            if mouse_pos[0] < self._slider_button.pos_x + self._slider_size / 2 and self._moved_direction == "left":
                self._dont_move = False
            elif mouse_pos[0] > self._slider_button.pos_x + self._slider_size / 2 and self._moved_direction == "right":
                self._dont_move = False

        if self._held:

            self._slider_button.state = c.States.PRESSED

            if not self._dont_move:
                if mouse_pos[0] < self._pos_x:
                    self._slider_button.pos_x = self._pos_x
                else:
                    if mouse_pos[0] - self._slider_size / 2 < self._pos_x:
                        pass
                    else:

                        self._slider_button.x = mouse_pos[0] - self._slider_size / 2

                if mouse_pos[0] > self._pos_x + self._rail_width - self._slider_size / 2:
                    self._slider_button.pos_x = self._pos_x + self._rail_width - self._slider_size
                else:
                    if mouse_pos[0] - self._slider_size / 2:
                        pass
                    else:
                        self._slider_button.pos_x = mouse_pos[0] - self._slider_size / 2

        if self._held:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            self._changed_cursor = True

        elif self._changed_cursor:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self._changed_cursor = False

        # calculate float percentage value of slider
        self._percent = (self._slider_button.pos_x - self._pos_x) / (self._rail_width - self._slider_size)

    def render(self, screen: pygame.Surface) -> None:
        """Renders the element to the screen."""

        pygame.draw.rect(screen, self._color_rail, self._rail_rect, border_radius=self._rail_rounded_corners_amount)

        self._slider_button.draw(screen)

    def event(self, event: pygame.event.Event) -> None:

        # TODO: Make move amount a param
        move_amount = 1

        if event.type == pygame.KEYDOWN:
            if self._slider_button.state == c.States.PRESSED:
                if event.key == pygame.K_RIGHT:
                    if not self._slider_button.pos_x + self._slider_size + move_amount > self._pos_x + self._rail_width:
                        self._slider_button.pos_x += move_amount
                        self._dont_move = True
                    else:
                        self._slider_button.pos_x = self._pos_x + self._rail_width - self._slider_size
                        self._dont_move = True

                    self._moved_direction = 'right'

                elif event.key == pygame.K_LEFT:
                    if not self._slider_button.pos_x - move_amount < self._pos_x:
                        self._slider_button.pos_x -= move_amount
                        self._dont_move = True
                    else:
                        self._slider_button.pos_x = self._pos_x
                        self._dont_move = True

                    self._moved_direction = 'left'

    @property
    def value(self) -> float:
        """
        Get the value of the slider
        """
        return self._percent

    @value.setter
    def value(self, value: float) -> None:
        """
        Set the value.
        :param value: Must be a float 0 to 1.
        """

        if check_tools.is_num(value):
            if value < 0:
                value = 0
            elif value > 1:
                value = 1
        else:
            raise ValueError("value argument must be of type <float>.")

        self._slider_button.pos_x = self._pos_x + (self._rail_width - self._slider_size) * value

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
            self._pos_x = int(value)
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
            self._pos_y = int(value)
        else:
            raise ValueError("y value must be of type <int> or <float>.")

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
            log.debug("Unreachable code. Defaulting to default theme.")
            theme = themes.get_default_theme()

        self._theme = theme

        self._create_colors()
        self._slider_button.theme = theme
