import math
from enum import Enum, auto
from typing import SupportsInt, List

import pygame

from .element import ContainerElement, SizedElement
from .. import constants
from ..utils import ParsingTools


class GridFillOrder(Enum):
    ROW_MAJOR = auto()
    COLUMN_MAJOR = auto()


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
                 ) -> None:
        super().__init__(x, y, width, height, elements, enforce_layout_cleanliness)

        if padding is None:
            padding = constants.DEFAULT_CONTAINER_PADDING

        if spacing is None:
            spacing = constants.DEFAULT_CONTAINER_SPACING

        self._padding = ParsingTools.parse_non_negative_int(padding, "padding")
        self._spacing = ParsingTools.parse_non_negative_int(spacing, "spacing")

    def apply(self) -> None:
        super().apply()

        if len(self._elements) == 0:
            return

        current_column_width = 0
        current_x = self._x + self._padding
        current_y = self._y + self._padding

        for element in self.elements:
            # Check if new element exceeds container height.
            if current_y + element.height > self._y + self._height - self._padding:
                # Move to next column.
                current_x += current_column_width + self._spacing
                current_y = self._y + self._padding
                current_column_width = 0

            element.pos = (current_x, current_y)

            current_y += element.height + self._spacing

            current_column_width = max(current_column_width, element.width)


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
                 ) -> None:
        super().__init__(x, y, width, height, elements, enforce_layout_cleanliness)

        if padding is None:
            padding = constants.DEFAULT_CONTAINER_PADDING

        if spacing is None:
            spacing = constants.DEFAULT_CONTAINER_SPACING

        self._padding = ParsingTools.parse_non_negative_int(padding, "padding")
        self._spacing = ParsingTools.parse_non_negative_int(spacing, "spacing")

    def apply(self) -> None:
        super().apply()

        if len(self._elements) == 0:
            return

        current_row_height = 0
        current_x = self._x + self._padding
        current_y = self._y + self._padding

        for element in self.elements:
            # Check if new element exceeds container width.
            if current_x + element.width > self._x + self._width - self._padding:
                # Move to next row.
                current_y += current_row_height + self._spacing
                current_x = self._x + self._padding
                current_row_height = 0

            element.pos = (current_x, current_y)

            current_x += element.width + self._spacing

            current_row_height = max(current_row_height, element.height)


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
