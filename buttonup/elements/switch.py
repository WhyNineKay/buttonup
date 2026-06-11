from enum import Enum, auto
from typing import SupportsInt, Union, Optional

import pygame

from .element import InteractionState, InteractiveElement, ThemedElement, BorderedElement, DraggableElement
from .label import Label
from .. import constants
from ..buttonup_types import Callback, BoolCallback, FontLike, RGB
from ..theme import ThemeLike, load_default_theme, CheckboxTheme
from ..utils import CallbackPackage, ParsingTools


class Switch(DraggableElement, ThemedElement, BorderedElement):
    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 height: SupportsInt = None,
                 theme: ThemeLike = None,
                 text: str = None,
                 font: FontLike = None,
                 font_size: SupportsInt = None,
                 on_toggle: Union[CallbackPackage, BoolCallback] = None,
                 on_click: Union[CallbackPackage, Callback] = None,
                 on_hover: Union[CallbackPackage, Callback] = None,
                 border_radius: SupportsInt = None,
                 border_width: SupportsInt = None,
                 text_padding: SupportsInt = None,
                 knob_padding: SupportsInt = None,
                 default_switched: bool = None
                 ) -> None:
        if height is None:
            track_height = constants.DEFAULT_SWITCH_HEIGHT
        else:
            track_height = height

        self._track_height = self._parse_track_height(track_height)
        self._track_width = self._track_height * 2

        self._user_on_click_callback_package = self._parse_named_callback(on_click, "on_click")

        DraggableElement.__init__(
            self, x, y, width=self._track_width, height=self._track_height, on_click=self._on_click_handler,
            on_hover=on_hover,
            on_drag_start=self._on_drag_start,
            on_drag=self._on_drag, on_drag_end=self._on_drag_end,
        )

        # ----- Knob Padding
        if knob_padding is None:
            knob_padding = constants.DEFAULT_SWITCH_PADDING

        self._knob_padding = self._parse_knob_padding(knob_padding)

        # ----- Rects and positions
        self._track_rect = pygame.Rect(self._x, self._y, self._track_width, self._track_height)
        self._knob_rect = pygame.Rect(
            0, 0,
            self._track_height - 2 * self._knob_padding,
            self._track_height - 2 * self._knob_padding
        )

        self._knob_pos_on = (
            self._x + self._track_width - self._knob_rect.width - self._knob_padding,
            self._y + self._knob_padding
        )
        self._knob_pos_off = (self._x + self._knob_padding, self._y + self._knob_padding)

        # ----- Theme

        if theme is None:
            theme = load_default_theme()

        ThemedElement.__init__(self, theme=theme)

        self._switch_theme = self.theme.switch_theme.copy()

        # ----- Border

        if border_radius is None:
            border_radius = constants.DEFAULT_SWITCH_BORDER_RADIUS

        if border_width is None:
            border_width = constants.DEFAULT_SWITCH_BORDER_WIDTH

        BorderedElement.__init__(self, border_radius=border_radius, border_width=border_width)

        # ----- On Switch callback

        if on_toggle is None:
            on_toggle = lambda _: None

        self._on_toggle: CallbackPackage = ParsingTools.parse_callback_or_callback_package(on_toggle, "on_toggle")

        if len(self._on_toggle.args) > 0:
            raise ValueError(
                "on_toggle callback cannot have any positional arguments as new switched state will be passed as the "
                "only argument when called."
            )
        # ----- Padding

        if text_padding is None:
            text_padding = constants.DEFAULT_SWITCH_TEXT_PADDING

        self._text_padding = self._parse_text_padding(text_padding)

        # ----- Label (text, font, font_size)
        if text is None:
            text = ""

        if font_size is None:
            font_size = constants.DEFAULT_FONT_SIZE

        if font is None:
            font = constants.DEFAULT_FONT_NAME

        self._switch_label = Label(
            x=self._x + self._track_width + self._text_padding,
            y=self._y + self._track_height // 2,
            text=text,
            font=font,
            font_size=font_size,
            theme=self.theme
        )

        # Update dimensions to set up the track and knob rects
        self._update_dimensions(
            width=self._track_width + self._text_padding + self._switch_label.width,
            height=max(self._track_height, self._switch_label.height)
        )

        if default_switched is None:
            default_switched = False

        self._switched = ParsingTools.parse_bool_strict(default_switched, "default_switched")

        self._set_knob_position()

    def _set_knob_position(self) -> None:
        if self._switched:
            self._knob_rect.topleft = self._knob_pos_on
        else:
            self._knob_rect.topleft = self._knob_pos_off

    def _parse_track_height(self, track_height: SupportsInt) -> int:
        return ParsingTools.parse_non_negative_int(track_height, "track_height")

    def _update_track_height(self, track_height: SupportsInt) -> None:
        self._track_height = self._parse_track_height(track_height)
        self._track_width = self._track_height * 2

        self._width = self._track_width + self._text_padding + self._switch_label.width
        self._height = max(self._track_height, self._switch_label.height)

        self._update_dimensions(self._width, self._height)


    def _update_position(self, x: SupportsInt, y: SupportsInt) -> None:
        super()._update_position(x, y)

        self._track_rect.topleft = (self._x, self._y)

        self._knob_pos_on = (
            self._x + self._track_width - self._knob_rect.width - self._knob_padding,
            self._y + self._knob_padding
        )
        self._knob_pos_off = (self._x + self._knob_padding, self._y + self._knob_padding)

        if self._switched:
            self._knob_rect.topleft = self._knob_pos_on
        else:
            self._knob_rect.topleft = self._knob_pos_off

        # Update label position
        self._switch_label.x = self._x + self._track_width + self._text_padding
        self._switch_label.y = self._y + (self._height - self._switch_label.height) // 2

    def _update_dimensions(self, width: int, height: int) -> None:
        super()._update_dimensions(width, height)

        self._track_rect = pygame.Rect(self._x, self._y, self._track_width, self._track_height)
        self._knob_rect = pygame.Rect(
            0, 0,
            self._track_height - 2 * self._knob_padding,
            self._track_height - 2 * self._knob_padding
        )

        self._knob_pos_on = (
            self._x + self._track_width - self._knob_rect.width - self._knob_padding,
            self._y + self._knob_padding
        )
        self._knob_pos_off = (self._x + self._knob_padding, self._y + self._knob_padding)

    def _parse_knob_padding(self, knob_padding: SupportsInt) -> int:
        return ParsingTools.parse_non_negative_int(knob_padding, "knob_padding")

    def _on_click_handler(self) -> None:
        # Determine the new switched state based on the click position
        click_x, _ = pygame.mouse.get_pos()

        previous_switched = self._switched

        if self._track_rect.x <= click_x <= self._track_rect.x + self._track_rect.width:
            # Click inside of rail.
            if click_x < self._x + self._track_width / 2:
                self._switched = False
            else:
                self._switched = True
        else:
            # Click outside of rail, simply just toggle the state.
            self._switched = not self._switched

        # On click first
        self._user_on_click_callback_package.call()

        # Then if the state changed, call the on_toggle callback with the new state.
        if self._switched != previous_switched:
            self._on_toggle.callback(self._switched, **self._on_toggle.kwargs)

        self._set_knob_position()


    def _on_drag_start(self) -> None:
        pass

    def _on_drag_end(self) -> None:
        self._switched = self._get_new_switched_state()

        self._on_toggle.callback(self._switched, **self._on_toggle.kwargs)

        self._set_knob_position()

    def _on_drag(self) -> None:
        mouse_x, _ = pygame.mouse.get_pos()

        # Set it to the mouse_x but clamp it to the track
        knob_x = mouse_x - self._knob_rect.width // 2

        if knob_x < self._x + self._knob_padding:
            knob_x = self._x + self._knob_padding
        elif knob_x > self._x + self._track_width - self._knob_rect.width - self._knob_padding:
            knob_x = self._x + self._track_width - self._knob_rect.width - self._knob_padding

        self._knob_rect.x = knob_x

    def _get_new_switched_state(self) -> bool:
        # Determine the new switched state based on the knob's position
        center_x = self._knob_rect.centerx
        track_center_x = self._x + self._track_width / 2

        return center_x >= track_center_x

    def _update_colors(self) -> None:
        self._switch_theme = self.theme.switch_theme.copy()

    def _parse_text_padding(self, text_padding: SupportsInt) -> int:
        return ParsingTools.parse_non_negative_int(text_padding, "text_padding")

    def _get_base_color(self) -> RGB:
        if self._state == InteractionState.DISABLED:
            return self._switch_theme.base_color_disabled
        elif self._state == InteractionState.PRESSED:
            return self._switch_theme.base_color_pressed
        elif self._state == InteractionState.HOVERED:
            return self._switch_theme.base_color_hovered
        elif self._state == InteractionState.DRAGGING:
            return self._switch_theme.base_color_pressed
        else:
            return self._switch_theme.base_color

    def _get_border_color(self) -> RGB:
        if self._state == InteractionState.DISABLED:
            return self._switch_theme.border_color_disabled
        elif self._state == InteractionState.PRESSED:
            return self._switch_theme.border_color_pressed
        elif self._state == InteractionState.HOVERED:
            return self._switch_theme.border_color_hovered
        elif self._state == InteractionState.DRAGGING:
            return self._switch_theme.border_color_pressed
        else:
            return self._switch_theme.border_color

    def _get_check_color(self) -> RGB:
        if self._state == InteractionState.DISABLED:
            return self._switch_theme.knob_color_disabled
        elif self._state == InteractionState.PRESSED:
            return self._switch_theme.knob_color_pressed
        elif self._state == InteractionState.HOVERED:
            return self._switch_theme.knob_color_hovered
        elif self._state == InteractionState.DRAGGING:
            return self._switch_theme.knob_color_pressed
        else:
            return self._switch_theme.knob_color

    def _get_text_color(self) -> RGB:
        if self._state == InteractionState.DISABLED:
            return self._switch_theme.text_color_disabled
        elif self._state == InteractionState.PRESSED:
            return self._switch_theme.text_color_pressed
        elif self._state == InteractionState.HOVERED:
            return self._switch_theme.text_color_hovered
        else:
            return self._switch_theme.text_color

    def draw(self, surface: pygame.Surface) -> None:
        base_color = self._get_base_color()
        border_color = self._get_border_color()
        check_color = self._get_check_color()
        text_color = self._get_text_color()

        # Draw track
        pygame.draw.rect(surface, base_color, self._track_rect, border_radius=self._border_radius)

        if self._border_width > 0:
            pygame.draw.rect(surface, border_color, self._track_rect, width=self._border_width,
                             border_radius=self._border_radius)

        # Draw knob
        pygame.draw.rect(surface, check_color, self._knob_rect, border_radius=self._border_radius - self._border_width)

        # Draw label
        if self._switch_label.text_color != text_color:
            self._switch_label.text_color = text_color

        self._switch_label.draw(surface)

    def update(self, dt: float) -> None:
        super().update(dt)

        if ((self._switch_label.width + self._text_padding + self._track_width != self._width)
                or max(self._switch_label.height, self._track_height) != self._height):

            self._update_dimensions(
                width=self._track_width + self._text_padding + self._switch_label.width,
                height=max(self._track_height, self._switch_label.height)
            )

    @property
    def switched(self) -> bool:
        return self._switched

    @switched.setter
    def switched(self, value: bool) -> None:
        value = ParsingTools.parse_bool_strict(value, "switched")

        self._switched = value
        self._set_knob_position()

    @property
    def label(self) -> Label:
        return self._switch_label

    @property
    def track_height(self) -> int:
        return self._track_height

    @track_height.setter
    def track_height(self, value: SupportsInt) -> None:
        self._update_track_height(value)

    @property
    def knob_padding(self) -> int:
        return self._knob_padding

    @knob_padding.setter
    def knob_padding(self, value: SupportsInt) -> None:
        self._knob_padding = self._parse_knob_padding(value)
        self._update_dimensions(self._width, self._height)

    @property
    def text_padding(self) -> int:
        return self._text_padding

    @text_padding.setter
    def text_padding(self, value: SupportsInt) -> None:
        self._text_padding = self._parse_text_padding(value)
        self._update_dimensions(self._width, self._height)
