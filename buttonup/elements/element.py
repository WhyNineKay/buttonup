"""
element.py
"""
import math
from pathlib import Path
from typing import SupportsInt, Tuple, Union, Optional, List, Any

import pygame

from ..buttonup_types import Callback, FontLike
from ..theme import Theme, ThemeLike, load_theme
from ..utils import CallbackPackage, InteractionState, ParsingTools
from .. import constants

class Element:
    """Base element class for all drawable elements."""

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def debug_draw(self, surface: pygame.Surface) -> None:
        pass


class PositionalElement:
    """
    Base class that allows for elements to have a position on the screen.
    """

    def __init__(self, x: SupportsInt, y: SupportsInt) -> None:
        """
        Constructor.
        :param x: x position of the element. Must support int() conversion.
        :param y: y position of the element. Must support int() conversion.
        """
        self._x = 0
        self._y = 0
        self._init_position(x, y)

    def _init_position(self, x: SupportsInt, y: SupportsInt) -> None:
        if hasattr(x, "__int__"):
            self._x = int(x)
        else:
            raise TypeError(f"Value 'x' must be of type int, or support __int__ conversion.")

        if hasattr(y, "__int__"):
            self._y = int(y)
        else:
            raise TypeError(f"Value 'y' must be of type int, or support __int__ conversion.")

    def _update_position(self, x: SupportsInt, y: SupportsInt) -> None:
        self._init_position(x, y)

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @x.setter
    def x(self, value: SupportsInt) -> None:
        self._update_position(value, self._y)

    @y.setter
    def y(self, value: SupportsInt) -> None:
        self._update_position(self._x, value)

    @property
    def pos(self) -> Tuple[int, int]:
        return self._x, self._y

    @pos.setter
    def pos(self, value: Tuple[SupportsInt, SupportsInt]) -> None:
        if not isinstance(value, tuple) or len(value) != 2:
            raise TypeError(f"Value 'pos' must be a tuple of length 2.")

        self._update_position(value[0], value[1])

    @property
    def vec(self) -> pygame.Vector2:
        return pygame.Vector2(self._x, self._y)

    @vec.setter
    def vec(self, value: pygame.Vector2) -> None:
        if not isinstance(value, pygame.Vector2):
            raise TypeError(f"Value 'vec' must be a tuple of length 2.")

        self._update_position(value[0], value[1])


class SizedElement(PositionalElement):
    """
    Base class that allows for elements to have a position and size on the screen.

    This element does not allow for changing the size of the element.
    """

    def __init__(self, x: SupportsInt, y: SupportsInt, width: SupportsInt, height: SupportsInt) -> None:
        self._rect = pygame.Rect(0, 0, 0, 0)

        PositionalElement.__init__(self, x, y)

        self._width = 0
        self._height = 0
        self._init_dimensions(width, height)

    def _init_dimensions(self, width: SupportsInt, height: SupportsInt) -> None:
        if not hasattr(width, "__int__"):
            raise TypeError(f"Value 'width' must be of type int, or support __int__ conversion.")
        if not hasattr(height, "__int__"):
            raise TypeError(f"Value 'height' must be of type int, or support __int__ conversion.")

        self._width = int(width)
        self._height = int(height)

        if self._width < 0:
            raise ValueError(f"Value 'width' must be non-negative.")
        if self._height < 0:
            raise ValueError(f"Value 'height' must be non-negative.")

        self._rect.size = (self._width, self._height)

    def _update_dimensions(self, width: SupportsInt, height: SupportsInt) -> None:
        self._init_dimensions(width, height)

    def _init_position(self, x: SupportsInt, y: SupportsInt) -> None:
        super()._init_position(x, y)
        self._rect.x = self._x
        self._rect.y = self._y

    def _update_position(self, x: SupportsInt, y: SupportsInt) -> None:
        super()._update_position(x, y)
        self._rect.x = self._x
        self._rect.y = self._y

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def dimensions(self) -> Tuple[int, int]:
        return self._width, self._height

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @property
    def centerx(self) -> int:
        return self._rect.centerx

    @property
    def centery(self) -> int:
        return self._rect.centery

    @property
    def center(self) -> Tuple[int, int]:
        return self._rect.center

    @center.setter
    def center(self, value: Tuple[SupportsInt, SupportsInt]) -> None:
        if not isinstance(value, tuple) or len(value) != 2:
            raise TypeError(f"Value 'center' must be a tuple of length 2.")

        if not hasattr(value[0], "__int__") or not hasattr(value[1], "__int__"):
            raise TypeError(f"Values in 'center' must be of type int, or support __int__ conversion.")

        x = int(value[0]) - self._width // 2
        y = int(value[1]) - self._height // 2

        self._update_position(x, y)

    @centerx.setter
    def centerx(self, value: SupportsInt) -> None:
        if not hasattr(value, "__int__"):
            raise TypeError(f"Value 'centerx' must be of type int, or support __int__ conversion.")

        x = int(value) - self._width // 2

        self._update_position(x, self._y)

    @centery.setter
    def centery(self, value: SupportsInt) -> None:
        if not hasattr(value, "__int__"):
            raise TypeError(f"Value 'centery' must be of type int, or support __int__ conversion.")

        y = int(value) - self._height // 2
        self._update_position(self._x, y)


class ResizableElement(SizedElement):
    """
    Base class that allows for elements to have a position and size on the screen, and allows for changing the size of
    the element.
    """

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: SupportsInt) -> None:
        self._update_dimensions(value, self._height)

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: SupportsInt) -> None:
        self._update_dimensions(self._width, value)

    @property
    def dimensions(self) -> Tuple[int, int]:
        return self._width, self._height

    @dimensions.setter
    def dimensions(self, value: Tuple[SupportsInt, SupportsInt]) -> None:
        if not isinstance(value, tuple) or len(value) != 2:
            raise TypeError(f"Value 'dimensions' must be a tuple of length 2.")

        self._update_dimensions(value[0], value[1])


class InteractiveElement(SizedElement, Element):
    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 width: SupportsInt,
                 height: SupportsInt,
                 on_click: Union[CallbackPackage, Callback] = None,
                 on_hover: Union[CallbackPackage, Callback] = None,
                 ) -> None:
        SizedElement.__init__(self, x=x, y=y, width=width, height=height)

        self._on_click_callback_package: CallbackPackage = self._parse_on_click(on_click)
        self._on_hover_callback_package: CallbackPackage = self._parse_on_hover(on_hover)

        self._state: InteractionState = InteractionState.INACTIVE
        self._previous_pressed: bool = False
        self._started_click_on_element: bool = False

    def _parse_named_callback(self,
                              callback: Union[CallbackPackage, Callback, None],
                              parameter_name: str,
                              ) -> CallbackPackage:
        callback_package = self._parse_generic_callback(callback)

        if callback_package is None:
            raise TypeError(
                f"Parameter '{parameter_name}' must be of type callable, CallbackPackage, or None, not "
                f"'{type(callback)}'."
            )

        return callback_package

    def _parse_on_click(self, callback: Union[CallbackPackage, Callback, None]) -> CallbackPackage:
        return self._parse_named_callback(callback, "on_click")

    def _parse_on_hover(self, callback: Union[CallbackPackage, Callback, None]) -> CallbackPackage:
        return self._parse_named_callback(callback, "on_hover")

    @staticmethod
    def _parse_generic_callback(callback: Union[CallbackPackage, Callback, None]) -> Optional[CallbackPackage]:
        if callback is None:
            return CallbackPackage(lambda: None, (), {})

        elif isinstance(callback, CallbackPackage):
            return callback

        elif callable(callback):
            return CallbackPackage(callback, (), {})

        return None

    def update(self, dt: float) -> None:
        if self._state == InteractionState.DISABLED:
            return

        mouse_pos = pygame.mouse.get_pos()
        is_mouse_over = self._rect.collidepoint(mouse_pos)

        current_pressed = pygame.mouse.get_pressed()[0]

        # Hover logic (only when not actively clicking)
        if not current_pressed:
            if is_mouse_over:
                if self._state != InteractionState.HOVERED:
                    self._state = InteractionState.HOVERED
                    self._on_hover_callback_package.call()
                    if self._state == InteractionState.DISABLED:
                        return
            else:
                self._state = InteractionState.INACTIVE

        # Mouse button just pressed
        if current_pressed and not self._previous_pressed:
            if is_mouse_over:
                self._state = InteractionState.PRESSED
                self._started_click_on_element = True
            else:
                self._started_click_on_element = False

        # Mouse button just released
        if not current_pressed and self._previous_pressed:
            if is_mouse_over and self._started_click_on_element:
                self._on_click_callback_package.call()
                if self._state != InteractionState.DISABLED:
                    self._state = InteractionState.HOVERED
            else:
                if self._state != InteractionState.DISABLED:
                    self._state = InteractionState.INACTIVE

            self._started_click_on_element = False

        self._previous_pressed = current_pressed

    def _parse_interaction_state(self, value: Any) -> InteractionState:
        if isinstance(value, InteractionState):
            return value
        else:
            raise TypeError(f"Interaction state must be of type InteractionState, not '{type(value)}'.")

    @property
    def state(self) -> InteractionState:
        return self._state

    @state.setter
    def state(self, value: Any) -> None:
        self._state = self._parse_interaction_state(value)

    def disable(self) -> None:
        self._state = InteractionState.DISABLED

    def enable(self) -> None:
        if self._state == InteractionState.DISABLED:
            self._state = InteractionState.INACTIVE


class DraggableElement(InteractiveElement):
    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 width: SupportsInt,
                 height: SupportsInt,
                 on_click: Union[CallbackPackage, Callback] = None,
                 on_hover: Union[CallbackPackage, Callback] = None,
                 on_drag_start: Union[CallbackPackage, Callback] = None,
                 on_drag: Union[CallbackPackage, Callback] = None,
                 on_drag_end: Union[CallbackPackage, Callback] = None,
                 drag_threshold: SupportsInt = None
                 ) -> None:
        InteractiveElement.__init__(self, x=x, y=y, width=width, height=height, on_click=on_click, on_hover=on_hover)

        self._on_drag_start_callback_package: CallbackPackage = self._parse_named_callback(on_drag_start, "on_drag_start")
        self._on_drag_callback_package: CallbackPackage = self._parse_named_callback(on_drag, "on_drag")
        self._on_drag_end_callback_package: CallbackPackage = self._parse_named_callback(on_drag_end, "on_drag_end")


        if drag_threshold is None:
            drag_threshold = constants.DEFAULT_DRAG_THRESHOLD

        self._drag_threshold = self._parse_drag_threshold(drag_threshold)

        # Set once when the drag threshold is crossed; persists until next drag begins.
        self._drag_start_pos: Optional[tuple[int, int]] = None

        # Set on mouse release after a drag; persists until next drag begins.
        self._drag_end_pos: Optional[tuple[int, int]] = None

        # Delta from the previous frame's mouse position. Zero when not dragging.
        self._drag_delta: tuple[int, int] = (0, 0)

        # Total displacement from drag_start_pos to the current mouse position.
        self._drag_total_delta: tuple[int, int] = (0, 0)

        # Internal tracking.
        self._press_origin: Optional[tuple[int, int]] = None  # Where the mouse first went down.
        self._previous_mouse_pos: Optional[tuple[int, int]] = None
        self._is_dragging: bool = False

    def _parse_drag_threshold(self, value: Any) -> int:
        return ParsingTools.parse_non_negative_int(value, "drag_threshold")

    @property
    def drag_start_pos(self) -> Optional[tuple[int, int]]:
        """Mouse position where the drag was confirmed (threshold crossed).
        Persists until the next drag begins. None before any drag has occurred."""
        return self._drag_start_pos

    @property
    def drag_end_pos(self) -> Optional[tuple[int, int]]:
        """Mouse position when the last drag ended.
        Persists until the next drag begins. None before any drag has completed."""
        return self._drag_end_pos

    @property
    def drag_delta(self) -> tuple[int, int]:
        """Per-frame mouse delta while dragging. (0, 0) when not dragging."""
        return self._drag_delta

    @property
    def drag_total_delta(self) -> tuple[int, int]:
        """Total displacement from drag_start_pos to the current mouse position.
        (0, 0) when not dragging."""
        return self._drag_total_delta

    @property
    def is_dragging(self) -> bool:
        return self._is_dragging

    def update(self, dt: float) -> None:
        if self._state == InteractionState.DISABLED:
            self._drag_delta = (0, 0)
            self._drag_total_delta = (0, 0)
            return

        mouse_pos = pygame.mouse.get_pos()
        is_mouse_over = self._rect.collidepoint(mouse_pos)
        current_pressed = pygame.mouse.get_pressed()[0]

        # Mouse button JUST PRESSED
        if current_pressed and not self._previous_pressed:
            if is_mouse_over:
                self._state = InteractionState.PRESSED
                self._started_click_on_element = True
                self._press_origin = mouse_pos
                self._previous_mouse_pos = mouse_pos

            else:
                self._started_click_on_element = False
                self._press_origin = None

        # Mouse button HELD DOWN
        elif current_pressed and self._previous_pressed:
            if self._started_click_on_element and self._press_origin is not None:
                if self._is_dragging:
                    # Already dragging - update deltas and fire on_drag.
                    prev = self._previous_mouse_pos or mouse_pos

                    self._drag_delta = (mouse_pos[0] - prev[0], mouse_pos[1] - prev[1])

                    self._drag_total_delta = (
                        mouse_pos[0] - self._drag_start_pos[0],
                        mouse_pos[1] - self._drag_start_pos[1],
                    )

                    self._previous_mouse_pos = mouse_pos
                    self._on_drag_callback_package.call()

                    if self._state == InteractionState.DISABLED:
                        return

                else:
                    # Not yet dragging - check whether threshold is crossed.
                    dx = mouse_pos[0] - self._press_origin[0]
                    dy = mouse_pos[1] - self._press_origin[1]

                    distance = math.sqrt(dx * dx + dy * dy)

                    if distance >= self._drag_threshold:
                        self._is_dragging = True

                        self._drag_start_pos = mouse_pos
                        self._drag_end_pos = None
                        self._drag_delta = (dx, dy)
                        self._drag_total_delta = (dx, dy)
                        self._previous_mouse_pos = mouse_pos

                        self._state = InteractionState.DRAGGING
                        self._on_drag_start_callback_package.call()

                        if self._state == InteractionState.DISABLED:
                            return

        # Mouse button JUST RELEASED
        elif not current_pressed and self._previous_pressed:
            if self._is_dragging:
                # End the drag and suppress click.
                self._drag_end_pos = mouse_pos

                self._drag_delta = (0, 0)
                self._drag_total_delta = (0, 0)
                self._is_dragging = False
                self._press_origin = None
                self._previous_mouse_pos = None

                self._state = InteractionState.HOVERED if is_mouse_over else InteractionState.INACTIVE

                self._on_drag_end_callback_package.call()

                if self._state == InteractionState.DISABLED:
                    return

            else:
                # Normal click release (no drag occurred).
                self._drag_delta = (0, 0)

                if is_mouse_over and self._started_click_on_element:
                    self._on_click_callback_package.call()
                    if self._state != InteractionState.DISABLED:
                        self._state = InteractionState.HOVERED
                else:
                    if self._state != InteractionState.DISABLED:
                        self._state = InteractionState.INACTIVE

                self._started_click_on_element = False
                self._press_origin = None
                self._previous_mouse_pos = None

        # mouse button inactive
        else:
            self._drag_delta = (0, 0)

            if not self._is_dragging:
                # Hover logic (mirrors InteractiveElement exactly).
                if is_mouse_over:
                    if self._state != InteractionState.HOVERED:
                        self._state = InteractionState.HOVERED
                        self._on_hover_callback_package.call()
                        if self._state == InteractionState.DISABLED:
                            return
                else:
                    self._state = InteractionState.INACTIVE

        self._previous_pressed = current_pressed


class FontElement:
    def __init__(self, font: FontLike, font_size: SupportsInt) -> None:
        self._raw_font_form = font
        self._font_size = self._parse_font_size(font_size)
        self._font = self._parse_font(font)

    def _update_font_and_size(self, font: FontLike, font_size: SupportsInt) -> None:
        self._font_size = self._parse_font_size(font_size)
        self._font = self._parse_font(font)

    def _parse_font(self, font: FontLike) -> pygame.font.Font:
        if not pygame.font.get_init():
            raise RuntimeError("Pygame font module must be initialized before creating a FontElement.")

        if isinstance(font, pygame.font.Font):
            return font

        elif isinstance(font, str):
            if pygame.font.match_font(font) is None:
                raise ValueError(f"Font name '{font}' does not match any available system fonts.")

            return pygame.font.SysFont(font, self._font_size)
        elif isinstance(font, Path):
            if not font.exists():
                raise ValueError(f"Font path '{font}' does not exist.")
            if not font.is_file():
                raise ValueError(f"Font path '{font}' is not a file.")
            return pygame.font.Font(str(font), self._font_size)
        else:
            raise TypeError(f"Font must be of type pygame.font.Font, str font name, or Path to a font file.")

    @staticmethod
    def _parse_font_size(font_size: SupportsInt) -> int:
        if not hasattr(font_size, "__int__"):
            raise TypeError(f"Font size must be of type int, or support __int__ conversion.")

        size = int(font_size)

        if size <= 0:
            raise ValueError(f"Font size must be greater than 0, not '{size}'.")

        return size

    @property
    def font(self) -> pygame.font.Font:
        return self._font

    @font.setter
    def font(self, font: FontLike) -> None:
        self._raw_font_form = font
        self._update_font_and_size(font, self._font_size)

    @property
    def font_size(self) -> int:
        return self._font_size

    @font_size.setter
    def font_size(self, font_size: int) -> None:
        if isinstance(self._raw_font_form, pygame.font.Font):
            raise ValueError("Cannot change font size when using a pygame.font.Font object as the font.")

        self._update_font_and_size(self._raw_font_form, font_size)


class ThemedElement:
    def __init__(self, theme: ThemeLike) -> None:
        self._theme = self._parse_theme(theme)
        self._init_colors()

    def _parse_theme(self, theme: ThemeLike) -> Theme:
        return load_theme(theme)

    def _update_colors(self) -> None:
        """Update colors for the element."""
        self._init_colors()

    def _init_colors(self) -> None:
        """Initialize colors for the element. Called during __init__ after parsing the theme."""
        pass

    @property
    def theme(self) -> Theme:
        return self._theme

    @theme.setter
    def theme(self, theme: ThemeLike) -> None:
        self._theme = self._parse_theme(theme)
        self._update_colors()


class ContainerElement(Element, ResizableElement):
    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 width: SupportsInt,
                 height: SupportsInt,
                 elements: List[SizedElement] = None
                 ) -> None:
        ResizableElement.__init__(self, x=x, y=y, width=width, height=height)

        if elements is None:
            elements = []

        self._elements = self._parse_elements(elements)

        self._layout_dirty = True

    def _raise_if_dirty(self) -> None:
        if self._layout_dirty:
            raise RuntimeError("Container layout is dirty: Elements are not synced to container. Please call the "
                               "'apply' method to update the layout before drawing, updating, or handling events.")

    def _parse_elements(self, elements: List[SizedElement]) -> List[SizedElement]:
        if not isinstance(elements, list):
            raise TypeError(f"Elements must be a list of SizedElement objects, not '{type(elements)}'.")

        for element in elements:
            if not isinstance(element, SizedElement):
                raise TypeError(f"All elements must be of type SizedElement, not '{type(element)}'.")

        return elements

    def add(self, element: SizedElement) -> None:
        if not isinstance(element, SizedElement):
            raise TypeError(f"Element must be of type SizedElement, not '{type(element)}'.")

        self._elements.append(element)
        self._layout_dirty = True

    def remove(self, element: SizedElement) -> None:
        if element in self._elements:
            self._elements.remove(element)
        else:
            raise ValueError("Element not found in container.")

        self._layout_dirty = True

    def clear(self) -> None:
        self._elements.clear()
        self._layout_dirty = True

    def apply(self) -> None:
        """Apply the containers arrangement functionality. MUST be implemented by subclasses."""
        self._layout_dirty = False

    def draw(self, surface: pygame.Surface) -> None:
        self._raise_if_dirty()

        for element in self._elements:
            if isinstance(element, Element):
                element.draw(surface)

    def update(self, dt: float) -> None:
        self._raise_if_dirty()

        for element in self._elements:
            if isinstance(element, Element):
                element.update(dt)

    def handle_event(self, event: pygame.event.Event) -> None:
        self._raise_if_dirty()

        for element in self._elements:
            if isinstance(element, Element):
                element.handle_event(event)

    def debug_draw(self, surface: pygame.Surface) -> None:
        for element in self._elements:
            if isinstance(element, Element):
                element.debug_draw(surface)

        pygame.draw.rect(surface, (255, 0, 0), self._rect, 1)

    def _update_position(self, x: SupportsInt, y: SupportsInt, apply: bool = True) -> None:
        ResizableElement._update_position(self, x, y)

        if apply:
            self.apply()

    def _update_dimensions(self, width: SupportsInt, height: SupportsInt, apply: bool = True) -> None:
        ResizableElement._update_dimensions(self, width, height)

        if apply:
            self.apply()

    @property
    def elements(self) -> List[SizedElement]:
        return self._elements.copy()

    @elements.setter
    def elements(self, elements: List[SizedElement]) -> None:
        self._elements = self._parse_elements(elements)
        self._layout_dirty = True

    def extend(self, elements: List[SizedElement]) -> None:
        elements = self._parse_elements(elements)

        self._elements.extend(elements)
        self._layout_dirty = True


class BorderedElement:
    def __init__(self, border_radius: SupportsInt, border_width: SupportsInt) -> None:
        self._border_radius = self._parse_border_radius(border_radius)
        self._border_width = self._parse_border_width(border_width)

    def _parse_border_radius(self, value: SupportsInt) -> int:
        return ParsingTools.parse_non_negative_int(value, "border_radius")

    def _parse_border_width(self, value: SupportsInt) -> int:
        return ParsingTools.parse_non_negative_int(value, "border_width")

    @property
    def border_radius(self) -> int:
        return self._border_radius

    @border_radius.setter
    def border_radius(self, value: SupportsInt) -> None:
        self._update_border_radius(value)

    @property
    def border_width(self) -> int:
        return self._border_width

    @border_width.setter
    def border_width(self, value: SupportsInt) -> None:
        self._update_border_width(value)

    def _update_border_radius(self, value: SupportsInt) -> None:
        self._border_radius = self._parse_border_radius(value)

    def _update_border_width(self, value: SupportsInt) -> None:
        self._border_width = self._parse_border_width(value)
