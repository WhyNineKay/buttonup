from enum import Enum, auto
from typing import SupportsInt, Union, Optional, Tuple

import pygame

from .element import InteractionState, InteractiveElement, ThemedElement, BorderedElement, DraggableElement
from .label import Label
from .. import constants
from ..buttonup_types import Callback, BoolCallback, FontLike, RGB, Number, FloatCallback
from ..theme import ThemeLike, load_default_theme, CheckboxTheme
from ..utils import CallbackPackage, ParsingTools, Axis


class Slider(DraggableElement, ThemedElement, BorderedElement):
    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 track_length: SupportsInt = None,
                 track_width: SupportsInt = None,
                 knob_size: SupportsInt = None,
                 theme: ThemeLike = None,
                 axis: Axis = None,
                 step: Number = None,
                 on_click: Union[CallbackPackage, Callback] = None,
                 on_hover: Union[CallbackPackage, Callback] = None,
                 on_change: Union[CallbackPackage, FloatCallback] = None,
                 border_radius: SupportsInt = None,
                 border_width: SupportsInt = None,
                 ) -> None:
        # ----- Track dimensions
        if track_length is None:
            track_length = constants.DEFAULT_SLIDER_TRACK_LENGTH

        self._track_length = self._parse_track_length(track_length)

        if track_width is None:
            track_width = constants.DEFAULT_SLIDER_TRACK_WIDTH

        self._track_width = self._parse_track_width(track_width)

        self._ensure_correct_width_length_ratio()

        # ----- knob Size
        if knob_size is None:
            knob_size = self._track_width * 1.5

        self._knob_size = self._parse_knob_size(knob_size)

        # ----- Axis
        if axis is None:
            axis = Axis.HORIZONTAL

        self._axis = self._parse_axis(axis)

        width, height = self._get_width_height_from_axis()

        self._user_on_click_callback_package = self._parse_named_callback(on_click, "on_click")

        DraggableElement.__init__(
            self, x, y, width=width, height=height, on_click=self._on_click_handler,
            on_hover=on_hover,
            on_drag_start=self._on_drag_start,
            on_drag=self._on_drag, on_drag_end=self._on_drag_end, drag_threshold=0
        )

        self._track_rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._knob_rect = pygame.Rect(self._x, self._y, self._knob_size, self._knob_size)

        # ---- Step
        if step is None:
            step = 0.0

        self._step = self._parse_step(step)

        self._value = 0.0

        self._set_knob_position(0.0)

        # ----- Theme
        if theme is None:
            theme = load_default_theme()

        ThemedElement.__init__(self, theme=theme)

        self._slider_theme = self.theme.slider_theme.copy()

        # ----- Border

        if border_radius is None:
            border_radius = constants.DEFAULT_SLIDER_BORDER_RADIUS

        if border_width is None:
            border_width = constants.DEFAULT_SLIDER_BORDER_WIDTH

        BorderedElement.__init__(self, border_radius=border_radius, border_width=border_width)

        # ----- On Change callback

        self._on_change: CallbackPackage = self._parse_on_change(on_change)

        if len(self._on_change.args) > 0:
            raise ValueError(
                "on_change callback cannot have any positional arguments as new changed state will be passed as the "
                "only argument when called."
            )


    def _parse_on_change(self, on_change: Union[CallbackPackage, Callback]) -> CallbackPackage:
        if on_change is None:
            on_change = CallbackPackage(callback=lambda value: None, args=(), kwargs={})

        return ParsingTools.parse_callback_or_callback_package(on_change, "on_change")

    def _parse_step(self, step: Number) -> float:
        if isinstance(step, (int, float)):
            if step < 0:
                raise ValueError(f"step must be non-negative, not {step}.")
            return float(step)
        else:
            raise TypeError(f"step must be a number (int or float), not '{type(step)}'.")

    def _set_knob_position(self, value: float) -> None:
        value = max(0.0, min(1.0, value))
        self._value = value

        if self._axis == Axis.HORIZONTAL:
            knob_x = self._x + int(value * (self._track_length - self._knob_size))
            knob_y = self._y + (self._track_width - self._knob_size) // 2
        else:
            knob_x = self._x + (self._track_width - self._knob_size) // 2
            knob_y = self._y + int(value * (self._track_length - self._knob_size))

        self._knob_rect.topleft = (knob_x, knob_y)

    def _parse_knob_size(self, knob_size: SupportsInt) -> int:
        return ParsingTools.parse_non_negative_int(knob_size, "knob_size")

    def _get_width_height_from_axis(self) -> Tuple[int, int]:
        if self._axis == Axis.HORIZONTAL:
            return self._track_length, self._track_width
        else:
            return self._track_width, self._track_length

    def _parse_axis(self, axis: Axis) -> Axis:
        if isinstance(axis, Axis):
            return axis
        else:
            raise TypeError(f"direction must be of type Axis, not '{type(axis)}'.")

    def _ensure_correct_width_length_ratio(self) -> None:
        # Ensure a 2:1 ratio between track length and width for proper appearance
        if self._track_length < 2 * self._track_width:
            raise ValueError(f"track_length must be >= 2 * track_width for proper appearance. (track_width={self._track_width}, track_length={self._track_length}, must be at least {2 * self._track_width})")

    def _parse_track_length(self, track_length: SupportsInt) -> int:
        return ParsingTools.parse_non_negative_int(track_length, "track_length")

    def _parse_track_width(self, track_width: SupportsInt) -> int:
        return ParsingTools.parse_non_negative_int(track_width, "track_width")

    def _on_click_handler(self) -> None:
        # Map the click position to a slider value and update the knob position accordingly, then call the user-provided on_click callback.
        previous_value = self._value

        mouse_x, mouse_y = pygame.mouse.get_pos()
        dominant_mouse_metric = mouse_x if self._axis == Axis.HORIZONTAL else mouse_y
        track_start, usable_range = self._compute_track_start_and_usable_range()

        value = self._compute_value_from_metric(dominant_mouse_metric, track_start, usable_range)
        self._set_knob_position(value)

        if self._user_on_click_callback_package:
            self._user_on_click_callback_package.call()

        if self._value != previous_value:
            if self._on_change:
                self._on_change.args = (self._value,)
                self._on_change.call()


    def _on_drag_start(self) -> None:
        pass

    def _on_drag_end(self) -> None:
        pass

    def _on_drag(self) -> None:
        """Handle dragging by mapping the current mouse position to a slider value."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dominant_mouse_metric = mouse_x if self._axis == Axis.HORIZONTAL else mouse_y

        previous_value = self._value

        track_start, usable_range = self._compute_track_start_and_usable_range()
        value = self._compute_value_from_metric(dominant_mouse_metric, track_start, usable_range)

        self._set_knob_position(value)

        if self._value != previous_value:
            if self._on_change:
                self._on_change.args = (self._value,)
                self._on_change.call()


    def _compute_track_start_and_usable_range(self) -> Tuple[int, float]:
        """
        Compute the starting pixel coordinate of the usable track and its usable pixel range.

        Returns:
            A tuple of (track_start, usable_range) where `track_start` is the pixel coordinate
            of the beginning of the knob movement and `usable_range` is the number of pixels
            available for the knob to travel.
        """
        track_start = self._x if self._axis == Axis.HORIZONTAL else self._y
        usable_range = float(self._track_length - self._knob_size)
        return track_start, usable_range


    def _compute_value_from_metric(self, dominant_metric: int, track_start: int, usable_range: float) -> float:
        """
        Convert a dominant screen metric (mouse x or y) into a normalized slider value [0.0, 1.0].

        Args:
            dominant_metric: The mouse coordinate along the slider's dominant axis.
            track_start: The starting pixel coordinate of the track.
            usable_range: The number of pixels the knob can move.

        Returns:
            A float value in [0.0, 1.0] representing the slider position.
        """
        # If there's no room for movement, keep value at 0
        if usable_range <= 0.0:
            return 0.0

        knob_center_offset = float(self._knob_size) / 2.0
        value = (dominant_metric - track_start - knob_center_offset) / usable_range

        if self._step_enabled():
            value = self._snap_to_nearest_step(value)

        return value

    def _snap_to_nearest_step(self, value: float) -> float:
        if self._step <= 0:
            return value

        steps = round(value / self._step)
        return steps * self._step

    def _step_enabled(self) -> bool:
        return self._step > 0

    def _update_colors(self) -> None:
        self._slider_theme = self.theme.slider_theme.copy()

    def _get_base_color(self) -> RGB:
        if self._state == InteractionState.DISABLED:
            return self._slider_theme.base_color_disabled
        elif self._state == InteractionState.PRESSED:
            return self._slider_theme.base_color_pressed
        elif self._state == InteractionState.HOVERED:
            return self._slider_theme.base_color_hovered
        elif self._state == InteractionState.DRAGGING:
            return self._slider_theme.base_color_pressed
        else:
            return self._slider_theme.base_color

    def _get_border_color(self) -> RGB:
        if self._state == InteractionState.DISABLED:
            return self._slider_theme.border_color_disabled
        elif self._state == InteractionState.PRESSED:
            return self._slider_theme.border_color_pressed
        elif self._state == InteractionState.HOVERED:
            return self._slider_theme.border_color_hovered
        elif self._state == InteractionState.DRAGGING:
            return self._slider_theme.border_color_pressed
        else:
            return self._slider_theme.border_color

    def _get_check_color(self) -> RGB:
        if self._state == InteractionState.DISABLED:
            return self._slider_theme.knob_color_disabled
        elif self._state == InteractionState.PRESSED:
            return self._slider_theme.knob_color_pressed
        elif self._state == InteractionState.HOVERED:
            return self._slider_theme.knob_color_hovered
        elif self._state == InteractionState.DRAGGING:
            return self._slider_theme.knob_color_pressed
        else:
            return self._slider_theme.knob_color

    def draw(self, surface: pygame.Surface) -> None:
        base_color = self._get_base_color()
        border_color = self._get_border_color()
        check_color = self._get_check_color()

        # Draw track
        pygame.draw.rect(surface, base_color, self._track_rect, border_radius=self._border_radius)

        # Draw notches if stepped
        if self._step_enabled():
            # Do not draw notches at the extreme ends (0 and 1) since the knob will cover them
            num_steps = int(1.0 / self._step)
            for i in range(1, num_steps):
                step_value = i * self._step
                notch_position = self._compute_notch_position(step_value)
                self._draw_notch(surface, notch_position, self._slider_theme.border_color)

        # Draw border
        if self._border_width > 0:
            pygame.draw.rect(surface, border_color, self._track_rect, width=self._border_width, border_radius=self._border_radius)

        # draw knob
        pygame.draw.rect(surface, check_color, self._knob_rect, border_radius=self._border_radius + (self._track_width - self._knob_size) // 2)

    def _draw_notch(self, surface: pygame.Surface, position: Tuple[int, int], color: RGB) -> None:
        notch_size = 4  # Size of the notch

        if self._axis == Axis.HORIZONTAL:
            notch_rect = pygame.Rect(position[0] - notch_size // 2, position[1] - self._track_width // 2, notch_size, self._track_width)
        else:
            notch_rect = pygame.Rect(position[0] - self._track_width // 2, position[1] - notch_size // 2, self._track_width, notch_size)

        pygame.draw.rect(surface, color, notch_rect)

    def _compute_notch_position(self, step_value: float) -> Tuple[int, int]:
        if self._axis == Axis.HORIZONTAL:
            notch_x = self._x + int(step_value * (self._track_length - self._knob_size)) + self._knob_size // 2
            notch_y = self._y + self._track_width // 2
        else:
            notch_x = self._x + self._track_width // 2
            notch_y = self._y + int(step_value * (self._track_length - self._knob_size)) + self._knob_size // 2

        return notch_x, notch_y

    def update(self, dt: float) -> None:
        super().update(dt)

    def _update_position(self, x: SupportsInt, y: SupportsInt) -> None:
        super()._update_position(x, y)
        self._track_rect.topleft = (self._x, self._y)
        self._set_knob_position(self._value)
