"""
element.py
"""
from pathlib import Path
from typing import SupportsInt, Tuple, Union, Optional, List
import pygame

from ..theme import Theme, ThemeLike, load_theme
from ..buttonup_types import Callback, FontLike
from ..utils import CallbackPackage, InteractionState, ParsingTools


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
        self._update_position(x, y)

    def _update_position(self, x: SupportsInt, y: SupportsInt) -> None:
        if hasattr(x, "__int__"):
            self._x = int(x)
        else:
            raise TypeError(f"Value 'x' must be of type int, or support __int__ conversion.")

        if hasattr(y, "__int__"):
            self._y = int(y)
        else:
            raise TypeError(f"Value 'y' must be of type int, or support __int__ conversion.")

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
        self._update_dimensions(width, height)

    def _update_dimensions(self, width: SupportsInt, height: SupportsInt) -> None:
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

    def _update_position(self, x: SupportsInt, y: SupportsInt) -> None:
        PositionalElement._update_position(self, x, y)
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
    Base class that allows for elements to have a position and size on the screen, and allows for changing the size of the element.
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

    def _parse_named_callback(self,
                              callback: Union[CallbackPackage, Callback, None],
                              parameter_name: str,
                              ) -> CallbackPackage:
        callback_package = self._parse_generic_callback(callback)

        if callback_package is None:
            raise TypeError(
                f"Parameter '{parameter_name}' must be of type callable, CallbackPackage, or None, not '{type(callback)}'."
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
            else:
                self._state = InteractionState.INACTIVE

        # Mouse button just pressed
        if current_pressed and not self._previous_pressed:
            if is_mouse_over:
                self._state = InteractionState.PRESSED

        # Mouse button just released
        if not current_pressed and self._previous_pressed:
            if is_mouse_over:
                self._on_click_callback_package.call()
                self._state = InteractionState.HOVERED
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
        self._update_colors()

    def _parse_theme(self, theme: ThemeLike) -> Theme:
        return load_theme(theme)

    def _update_colors(self) -> None:
        """Update colors for the element."""
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
                 elements: List[SizedElement] = None,
                 enforce_layout_cleanliness: bool = None
                 ) -> None:
        if elements is None:
            elements = []

        self._elements = self._parse_elements(elements)

        ResizableElement.__init__(self, x=x, y=y, width=width, height=height)

        if enforce_layout_cleanliness is None:
            self._enforce_layout_cleanliness = True
        else:
            self._enforce_layout_cleanliness = ParsingTools.parse_bool_strict(enforce_layout_cleanliness, "enforce_layout_cleanliness")

        self._layout_dirty = True

    def _raise_or_apply_if_dirty(self) -> None:
        if self._layout_dirty:
            if self._enforce_layout_cleanliness:
                raise RuntimeError("Container layout is dirty: Elements are not synced to container. Please call the "
                                   "'apply' method to update the layout before drawing, updating, or handling events.")
            else:
                self.apply()


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
        self._raise_or_apply_if_dirty()

        for element in self._elements:
            if isinstance(element, Element):
                element.draw(surface)

    def update(self, dt: float) -> None:
        self._raise_or_apply_if_dirty()

        for element in self._elements:
            if isinstance(element, Element):
                element.update(dt)

    def handle_event(self, event: pygame.event.Event) -> None:
        self._raise_or_apply_if_dirty()

        for element in self._elements:
            if isinstance(element, Element):
                element.handle_event(event)

    def debug_draw(self, surface: pygame.Surface) -> None:
        for element in self._elements:
            if isinstance(element, Element):
                element.debug_draw(surface)

        pygame.draw.rect(surface, (255, 0, 0), self._rect, 1)

    def _update_position(self, x: SupportsInt, y: SupportsInt) -> None:
        ResizableElement._update_position(self, x, y)
        self.apply()

    def _update_dimensions(self, width: SupportsInt, height: SupportsInt) -> None:
        ResizableElement._update_dimensions(self, width, height)
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

