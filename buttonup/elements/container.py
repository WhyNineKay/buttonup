import math
from enum import Enum, auto
from typing import SupportsInt, List, Optional

import pygame

from .element import ContainerElement, SizedElement, ResizableElement, ThemedElement, Element, BorderedElement
from .. import constants
from ..theme import load_default_theme, ThemeLike
from ..utils import ParsingTools


class GridFillOrder(Enum):
    ROW_MAJOR = auto()
    COLUMN_MAJOR = auto()


class PerpendicularOverflowBehaviour(Enum):
    EXPAND = auto()
    FIXED = auto()


class Panel(ResizableElement, ThemedElement, Element, BorderedElement):
    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 width: SupportsInt,
                 height: SupportsInt,
                 theme: ThemeLike = None,
                 element: SizedElement = None,
                 padding: SupportsInt = None,
                 border_radius: SupportsInt = None,
                 border_width: SupportsInt = None,
                 ) -> None:
        if element is None:
            self._element = None
        else:
            self._element = self._parse_element(element)

        ResizableElement.__init__(self, x, y, width, height)

        if theme is None:
            theme = load_default_theme()

        ThemedElement.__init__(self, theme=theme)

        if padding is None:
            padding = constants.DEFAULT_CONTAINER_PADDING

        self._padding = ParsingTools.parse_non_negative_int(padding, "padding")

        if border_radius is None:
            border_radius = constants.DEFAULT_CONTAINER_BORDER_RADIUS

        if border_width is None:
            border_width = constants.DEFAULT_CONTAINER_BORDER_WIDTH

        BorderedElement.__init__(self, border_radius=border_radius, border_width=border_width)

        self._container_theme = self._theme.container_theme.copy()

    def _update_colors(self) -> None:
        self._container_theme = self._theme.container_theme.copy()

    def draw(self, surface: pygame.Surface) -> None:
        # Draw background
        pygame.draw.rect(surface, self._container_theme.base_color, self._rect, border_radius=self._border_radius)

        # Draw border
        if self._border_width > 0:
            pygame.draw.rect(surface, self._container_theme.border_color, self._rect, width=self._border_width, border_radius=self._border_radius)

        if self._element is not None and isinstance(self._element, Element):
            self._element.draw(surface)

    def update(self, dt: float) -> None:
        if self._element is not None and isinstance(self._element, Element):
            self._element.update(dt)

    def debug_draw(self, surface: pygame.Surface) -> None:
        super().debug_draw(surface)

        if self._element is not None and isinstance(self._element, Element):
            self._element.debug_draw(surface)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._element is not None and isinstance(self._element, Element):
            self._element.handle_event(event)

    def _parse_element(self, element: SizedElement) -> SizedElement:
        if not isinstance(element, SizedElement):
            raise TypeError(f"Panel element must be of type 'SizedElement', not '{type(element)}'.")

        return element

    def _update_element_position(self) -> None:
        if self._element is not None:
            # Top left
            element_x = self._x + self._padding
            element_y = self._y + self._padding
            self._element.pos = (element_x, element_y)

    def _update_element_size(self) -> None:
        if self._element is not None:
            occupied_width = self._element.width + self._padding * 2
            occupied_height = self._element.height + self._padding * 2

            if occupied_width > self._width or occupied_height > self._height:
                # Resize panel to fit element with padding.
                new_width = max(self._width, occupied_width)
                new_height = max(self._height, occupied_height)

                self._update_dimensions(new_width, new_height)

    def _update_dimensions(self, width: SupportsInt, height: SupportsInt) -> None:
        super()._update_dimensions(width, height)
        self._update_element_size()

    def _update_position(self, x: SupportsInt, y: SupportsInt) -> None:
        super()._update_position(x, y)
        self._update_element_position()

    @property
    def element(self) -> Optional[SizedElement]:
        return self._element

    @element.setter
    def element(self, element: SizedElement) -> None:
        self._element = self._parse_element(element)
        self._update_element_position()
        self._update_element_size()



class VBox(ContainerElement):
    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 width: SupportsInt,
                 height: SupportsInt,
                 elements: List[SizedElement] = None,
                 enforce_layout_cleanliness: bool = None,
                 padding: SupportsInt = None,
                 spacing: SupportsInt = None,
                 overflow_behavior: PerpendicularOverflowBehaviour = None,
                 ) -> None:
        super().__init__(x, y, width, height, elements, enforce_layout_cleanliness)

        if padding is None:
            padding = constants.DEFAULT_CONTAINER_PADDING

        if spacing is None:
            spacing = constants.DEFAULT_CONTAINER_SPACING

        self._padding = ParsingTools.parse_non_negative_int(padding, "padding")
        self._spacing = ParsingTools.parse_non_negative_int(spacing, "spacing")

        if overflow_behavior is None:
            overflow_behavior = PerpendicularOverflowBehaviour.FIXED

        self._overflow_behavior = self._parse_overflow_behavior(overflow_behavior)

    def _parse_overflow_behavior(self, overflow_behavior: PerpendicularOverflowBehaviour) -> PerpendicularOverflowBehaviour:
        if not isinstance(overflow_behavior, PerpendicularOverflowBehaviour):
            raise TypeError(f"overflow_behavior must be of type 'OverflowBehavior', not '{type(overflow_behavior)}'.")

        return overflow_behavior

    def apply(self) -> None:
        super().apply()

        if len(self._elements) == 0:
            return

        total_width = 0
        current_column_width = 0
        current_x = self._x + self._padding
        current_y = self._y + self._padding

        for element in self.elements:
            # Check if new element exceeds container height.
            if current_y + element.height > self._y + self._height - self._padding:
                # Move to next column.
                current_x += current_column_width + self._spacing
                current_y = self._y + self._padding
                total_width += current_column_width + self._spacing

                current_column_width = 0

            element.pos = (current_x, current_y)

            current_y += element.height + self._spacing

            current_column_width = max(current_column_width, element.width)

        total_width += current_column_width + self._padding * 2

        if total_width == self._width:
            return

        if self._overflow_behavior == PerpendicularOverflowBehaviour.EXPAND:
            self._update_dimensions(total_width, self._height, apply=False)


class HBox(ContainerElement):
    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 width: SupportsInt,
                 height: SupportsInt,
                 elements: List[SizedElement] = None,
                 enforce_layout_cleanliness: bool = None,
                 padding: SupportsInt = None,
                 spacing: SupportsInt = None,
                 overflow_behavior: PerpendicularOverflowBehaviour = None,
                 ) -> None:
        super().__init__(x, y, width, height, elements, enforce_layout_cleanliness)

        if padding is None:
            padding = constants.DEFAULT_CONTAINER_PADDING

        if spacing is None:
            spacing = constants.DEFAULT_CONTAINER_SPACING

        self._padding = ParsingTools.parse_non_negative_int(padding, "padding")
        self._spacing = ParsingTools.parse_non_negative_int(spacing, "spacing")

        if overflow_behavior is None:
            overflow_behavior = PerpendicularOverflowBehaviour.FIXED

        self._overflow_behavior = self._parse_overflow_behavior(overflow_behavior)

    def _parse_overflow_behavior(self, overflow_behavior: PerpendicularOverflowBehaviour) -> PerpendicularOverflowBehaviour:
        if not isinstance(overflow_behavior, PerpendicularOverflowBehaviour):
            raise TypeError(f"overflow_behavior must be of type 'OverflowBehavior', not '{type(overflow_behavior)}'.")

        return overflow_behavior

    def apply(self) -> None:
        super().apply()

        if len(self._elements) == 0:
            return

        total_height = 0
        current_row_height = 0
        current_x = self._x + self._padding
        current_y = self._y + self._padding

        for element in self.elements:
            # Check if new element exceeds container width.
            if current_x + element.width > self._x + self._width - self._padding:
                # Move to next row.
                current_y += current_row_height + self._spacing
                current_x = self._x + self._padding
                total_height += current_row_height + self._spacing

                current_row_height = 0

            element.pos = (current_x, current_y)

            current_x += element.width + self._spacing

            current_row_height = max(current_row_height, element.height)

        total_height += current_row_height + self._padding * 2

        if total_height == self._height:
            return

        if self._overflow_behavior == PerpendicularOverflowBehaviour.EXPAND:
            self._update_dimensions(self._width, total_height, apply=False)


class Grid(ContainerElement):
    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 width: SupportsInt,
                 height: SupportsInt,
                 elements: List[SizedElement] = None,
                 columns: SupportsInt = None,
                 row_height: SupportsInt = None,
                 enforce_layout_cleanliness: bool = None,
                 padding: SupportsInt = None,
                 spacing: SupportsInt = None,
                 fill_order: GridFillOrder = None,
                 ) -> None:
        super().__init__(x, y, width, height, elements, enforce_layout_cleanliness)

        if padding is None:
            padding = constants.DEFAULT_CONTAINER_PADDING

        if spacing is None:
            spacing = constants.DEFAULT_CONTAINER_SPACING

        self._padding = ParsingTools.parse_non_negative_int(padding, "padding")
        self._spacing = ParsingTools.parse_non_negative_int(spacing, "spacing")

        if columns is None:
            columns = 1

        self._columns = self._parse_columns(columns)

        if fill_order is None:
            fill_order = GridFillOrder.ROW_MAJOR

        self._fill_order = self._parse_fill_order(fill_order)

        self._column_width = self._calculate_column_width()

        if row_height is None:
            row_height = self._column_width

        self._row_height = ParsingTools.parse_non_negative_int(row_height, "row_height")

    def _calculate_column_width(self) -> int:
        total_spacing = self._spacing * (self._columns - 1)
        total_padding = self._padding * 2

        available_width = self._width - total_spacing - total_padding
        column_width = available_width // self._columns

        return column_width

    def _parse_fill_order(self, fill_order: GridFillOrder) -> GridFillOrder:
        if not isinstance(fill_order, GridFillOrder):
            raise TypeError(f"fill_order must be of type 'GridFillOrder', not '{type(fill_order)}'.")

        return fill_order

    def _parse_columns(self, columns: SupportsInt) -> int:
        if not hasattr(columns, "__int__"):
            raise TypeError(f"columns must be of type 'int' or support __int__ conversion, not '{type(columns)}'.")

        columns_int = int(columns)

        if columns_int <= 0:
            raise ValueError("columns must be greater than 0.")

        return columns_int

    def apply(self) -> None:
        super().apply()

        if len(self._elements) == 0:
            return

        for index, element in enumerate(self.elements):
            if self._fill_order == GridFillOrder.ROW_MAJOR:
                # Row major: fill rows first, then columns.
                row = index // self._columns
                column = index % self._columns
            else:
                rows = math.ceil(len(self._elements) / self._columns)

                # Column major: fill columns first, then rows.
                column = index // rows
                row = index % rows

            # TOP LEFT
            x = self._x + self._padding + column * (self._column_width + self._spacing)
            y = self._y + self._padding + row * (self._row_height + self._spacing)

            element.pos = (x, y)

    def debug_draw(self, surface: pygame.Surface) -> None:
        super().debug_draw(surface)

        # Draw column lines.
        for i in range(1, self._columns):
            x = self._x + self._padding + i * (self._column_width + self._spacing) - self._spacing // 2
            pygame.draw.line(surface, (0, 127, 255), (x, self._y + self._padding),
                             (x, self._y + self._height - self._padding), 1)

        # Draw row lines.
        rows = math.ceil(len(self._elements) / self._columns)
        for i in range(1, rows):
            y = self._y + self._padding + i * (self._row_height + self._spacing) - self._spacing // 2
            pygame.draw.line(surface, (0, 127, 255), (self._x + self._padding, y),
                             (self._x + self._width - self._padding, y), 1)
