import math
from enum import Enum, auto
from typing import SupportsInt, List, Optional, Union, Iterable, Tuple

import pygame

from .element import SizedElement, SingleContainerElement, MultiContainerElement
from .. import constants
from ..theme import load_default_theme, ThemeLike
from ..utils import ParsingTools, Alignment, get_alignment_position


class GridFillOrder(Enum):
    ROW_FIRST = auto()
    COLUMN_FIRST = auto()

class Panel(SingleContainerElement):
    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 width: SupportsInt,
                 height: SupportsInt,
                 theme: Optional[ThemeLike] = None,
                 element: Optional[Union[SizedElement, None]] = None,
                 content_alignment: Optional[Alignment] = None,
                 draw_background: Optional[bool] = None,
                 border_radius: Optional[SupportsInt] = None,
                 border_width: Optional[SupportsInt] = None,
                 propagate_theme_change: Optional[bool] = None,
                 padding: Optional[SupportsInt] = None,
                 ) -> None:
        if theme is None:
            theme = load_default_theme()

        if draw_background is None:
            draw_background = False

        if border_radius is None:
            border_radius = constants.DEFAULT_CONTAINER_BORDER_RADIUS

        if border_width is None:
            border_width = constants.DEFAULT_CONTAINER_BORDER_WIDTH

        if propagate_theme_change is None:
            propagate_theme_change = True

        SingleContainerElement.__init__(
            self,
            x=x,
            y=y,
            width=width,
            height=height,
            theme=theme,
            element=element,
            draw_background=draw_background,
            border_radius=border_radius,
            border_width=border_width,
            propagate_theme_change=propagate_theme_change
        )

        if padding is None:
            padding = constants.DEFAULT_CONTAINER_PADDING

        self._padding = ParsingTools.parse_non_negative_int(padding, "padding")

        if content_alignment is None:
            content_alignment = Alignment.TOP_LEFT

        self._content_alignment = self._parse_content_alignment(content_alignment)

    def _parse_content_alignment(self, content_alignment: Optional[Alignment]) -> Alignment:
        if not isinstance(content_alignment, Alignment):
            raise ValueError(
                f"content_alignment must be of type {Alignment.__name__}, not {type(content_alignment).__name__}")

        return content_alignment

    def _update_element_position(self) -> None:
        if self._element is None:
            return

        element_x, element_y = get_alignment_position(
            alignment=self._content_alignment,
            container_rect=self._rect,
            element_rect=self._element.rect,
            left_padding=self._padding,
            right_padding=self._padding,
            top_padding=self._padding,
            bottom_padding=self._padding
        )

        self._element.pos = (element_x, element_y)

    def _update_element_size(self) -> None:
        if self._element is None:
            return

        occupied_width = self._element.width + self._padding * 2
        occupied_height = self._element.height + self._padding * 2

        if occupied_width > self._width or occupied_height > self._height:
            # Resize panel to fit element with padding.
            new_width = max(self._width, occupied_width)
            new_height = max(self._height, occupied_height)

            self._update_dimensions(new_width, new_height)

    def _update_dimensions(self, width: SupportsInt, height: SupportsInt) -> None:
        super()._update_dimensions(width, height)

    def _update_position(self, x: SupportsInt, y: SupportsInt) -> None:
        super()._update_position(x, y)

    def apply(self) -> None:
        super().apply()

        self._update_element_position()
        self._update_element_size()

    @property
    def content_alignment(self) -> Alignment:
        return self._content_alignment

    @content_alignment.setter
    def content_alignment(self, value: Alignment) -> None:
        self._content_alignment = self._parse_content_alignment(value)

        self.apply()

    @property
    def padding(self) -> int:
        return self._padding

    @padding.setter
    def padding(self, value: int) -> None:
        self._padding = ParsingTools.parse_non_negative_int(value, "padding")

        self.apply()

class VBox(MultiContainerElement):
    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 width: SupportsInt,
                 height: SupportsInt,
                 elements: Optional[Iterable[SizedElement]] = None,
                 padding: Optional[SupportsInt] = None,
                 spacing: Optional[SupportsInt] = None,
                 draw_background: Optional[bool] = None,
                 border_radius: Optional[SupportsInt] = None,
                 border_width: Optional[SupportsInt] = None,
                 theme: Optional[ThemeLike] = None,
                 propagate_theme_change: Optional[bool] = None,
                 ) -> None:
        if theme is None:
            theme = load_default_theme()

        if draw_background is None:
            draw_background = False

        if border_radius is None:
            border_radius = constants.DEFAULT_CONTAINER_BORDER_RADIUS

        if border_width is None:
            border_width = constants.DEFAULT_CONTAINER_BORDER_WIDTH

        if propagate_theme_change is None:
            propagate_theme_change = True

        if elements is None:
            elements = []

        MultiContainerElement.__init__(
            self,
            x=x,
            y=y,
            width=width,
            height=height,
            theme=theme,
            elements=elements,
            draw_background=draw_background,
            border_radius=border_radius,
            border_width=border_width,
            propagate_theme_change=propagate_theme_change,
        )

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

    @property
    def padding(self) -> int:
        return self._padding

    @padding.setter
    def padding(self, value: int) -> None:
        self._padding = ParsingTools.parse_non_negative_int(value, "padding")

        self.apply()

    @property
    def spacing(self) -> int:
        return self._spacing

    @spacing.setter
    def spacing(self, value: int) -> None:
        self._spacing = ParsingTools.parse_non_negative_int(value, "spacing")

        self.apply()

class HBox(MultiContainerElement):
    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 width: SupportsInt,
                 height: SupportsInt,
                 elements: Optional[Iterable[SizedElement]] = None,
                 padding: Optional[SupportsInt] = None,
                 spacing: Optional[SupportsInt] = None,
                 draw_background: Optional[bool] = None,
                 border_radius: Optional[SupportsInt] = None,
                 border_width: Optional[SupportsInt] = None,
                 theme: Optional[ThemeLike] = None,
                 propagate_theme_change: Optional[bool] = None,
                 ) -> None:
        if theme is None:
            theme = load_default_theme()

        if draw_background is None:
            draw_background = False

        if border_radius is None:
            border_radius = constants.DEFAULT_CONTAINER_BORDER_RADIUS

        if border_width is None:
            border_width = constants.DEFAULT_CONTAINER_BORDER_WIDTH

        if propagate_theme_change is None:
            propagate_theme_change = True

        if elements is None:
            elements = []

        MultiContainerElement.__init__(
            self,
            x=x,
            y=y,
            width=width,
            height=height,
            theme=theme,
            elements=elements,
            draw_background=draw_background,
            border_radius=border_radius,
            border_width=border_width,
            propagate_theme_change=propagate_theme_change,
        )

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

    @property
    def padding(self) -> int:
        return self._padding

    @padding.setter
    def padding(self, value: int) -> None:
        self._padding = ParsingTools.parse_non_negative_int(value, "padding")

        self.apply()

    @property
    def spacing(self) -> int:
        return self._spacing

    @spacing.setter
    def spacing(self, value: int) -> None:
        self._spacing = ParsingTools.parse_non_negative_int(value, "spacing")

        self.apply()

class UniformGrid(MultiContainerElement):
    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 width: SupportsInt,
                 height: SupportsInt,
                 elements: Optional[List[SizedElement]] = None,
                 rows: Optional[SupportsInt] = None,
                 columns: Optional[SupportsInt] = None,
                 padding: Optional[SupportsInt] = None,
                 spacing: Optional[SupportsInt] = None,
                 content_alignment: Optional[Alignment] = None,
                 draw_background: Optional[bool] = None,
                 border_radius: Optional[SupportsInt] = None,
                 border_width: Optional[SupportsInt] = None,
                 theme: Optional[ThemeLike] = None,
                 propagate_theme_change: Optional[bool] = None,
                 fill_order: Optional[GridFillOrder] = None,
                 ) -> None:
        if theme is None:
            theme = load_default_theme()

        if draw_background is None:
            draw_background = False

        if border_radius is None:
            border_radius = constants.DEFAULT_CONTAINER_BORDER_RADIUS

        if border_width is None:
            border_width = constants.DEFAULT_CONTAINER_BORDER_WIDTH

        if propagate_theme_change is None:
            propagate_theme_change = True

        if elements is None:
            elements = []

        if rows is None:
            rows = 2

        if columns is None:
            columns = 2

        self._rows = ParsingTools.parse_non_negative_int(rows, "rows")
        self._columns = ParsingTools.parse_non_negative_int(columns, "columns")

        MultiContainerElement.__init__(
            self,
            x=x,
            y=y,
            width=width,
            height=height,
            theme=theme,
            elements=elements,
            draw_background=draw_background,
            border_radius=border_radius,
            border_width=border_width,
            propagate_theme_change=propagate_theme_change,
        )

        if padding is None:
            padding = constants.DEFAULT_CONTAINER_PADDING

        if spacing is None:
            spacing = constants.DEFAULT_CONTAINER_SPACING

        self._padding = ParsingTools.parse_non_negative_int(padding, "padding")
        self._spacing = ParsingTools.parse_non_negative_int(spacing, "spacing")

        if fill_order is None:
            fill_order = GridFillOrder.ROW_FIRST

        self._fill_order = self._parse_fill_order(fill_order)

        if content_alignment is None:
            content_alignment = Alignment.TOP_LEFT

        self._content_alignment = self._parse_content_alignment(content_alignment)

    @staticmethod
    def _parse_fill_order(fill_order: GridFillOrder) -> GridFillOrder:
        if not isinstance(fill_order, GridFillOrder):
            raise ValueError(f"fill_order must be an instance of GridFillOrder, not {type(fill_order)}")

        return fill_order

    def _get_grid_positions(self) -> List[Tuple[int, int]]:
        if self._fill_order == GridFillOrder.ROW_FIRST:
            return [(row, col) for row in range(self._rows) for col in range(self._columns)]
        else:
            return [(row, col) for col in range(self._columns) for row in range(self._rows)]

    def _calculate_cell_size(self) -> Tuple[int, int]:
        cell_width = (self._width - self._padding * 2 - self._spacing * (self._columns - 1)) // self._columns
        cell_height = (self._height - self._padding * 2 - self._spacing * (self._rows - 1)) // self._rows

        return cell_width, cell_height

    def apply(self) -> None:
        super().apply()

        if len(self._elements) == 0:
            return

        cell_width, cell_height = self._calculate_cell_size()
        grid_positions = self._get_grid_positions()

        if len(self._elements) > self._rows * self._columns:
            raise ValueError(
                f"Grid capacity exceeded: {len(self._elements)} elements cannot fit in a {self._rows}x{self._columns}={self._rows * self._columns} grid"
            )



        for (row, col), element in zip(grid_positions, self.elements):
            cell_x = self._x + self._padding + col * (cell_width + self._spacing)
            cell_y = self._y + self._padding + row * (cell_height + self._spacing)

            # Calculate element position based on content alignment.
            cell_rect = pygame.Rect(cell_x, cell_y, cell_width, cell_height)

            element_pos = get_alignment_position(
                alignment=self._content_alignment,
                container_rect=cell_rect,
                element_rect=element.rect,
                left_padding=0,
                right_padding=0,
                top_padding=0,
                bottom_padding=0
            )

            element.pos = element_pos


    def debug_draw(self, surface: pygame.Surface) -> None:
        super().debug_draw(surface)

        cell_width, cell_height = self._calculate_cell_size()

        for row in range(self._rows):
            for col in range(self._columns):
                cell_x = self._x + self._padding + col * (cell_width + self._spacing)
                cell_y = self._y + self._padding + row * (cell_height + self._spacing)

                pygame.draw.rect(
                    surface,
                    (255, 0, 0),
                    (cell_x, cell_y, cell_width, cell_height),
                    1
                )

    @staticmethod
    def _parse_content_alignment(content_alignment: Optional[Alignment]) -> Alignment:
        if not isinstance(content_alignment, Alignment):
            raise ValueError(
                f"content_alignment must be of type {Alignment.__name__}, not {type(content_alignment).__name__}"
            )

        return content_alignment

    @property
    def padding(self) -> int:
        return self._padding

    @padding.setter
    def padding(self, value: int) -> None:
        self._padding = ParsingTools.parse_non_negative_int(value, "padding")

        self.apply()

    @property
    def spacing(self) -> int:
        return self._spacing

    @spacing.setter
    def spacing(self, value: int) -> None:
        self._spacing = ParsingTools.parse_non_negative_int(value, "spacing")

        self.apply()


    @property
    def fill_order(self) -> GridFillOrder:
        return self._fill_order

    @fill_order.setter
    def fill_order(self, value: GridFillOrder) -> None:
        self._fill_order = self._parse_fill_order(value)

        self.apply()

    @property
    def content_alignment(self) -> Alignment:
        return self._content_alignment

    @content_alignment.setter
    def content_alignment(self, value: Alignment) -> None:
        self._content_alignment = self._parse_content_alignment(value)

        self.apply()

    @property
    def rows(self) -> int:
        return self._rows

    @rows.setter
    def rows(self, value: int) -> None:
        self._rows = ParsingTools.parse_non_negative_int(value, "rows")

        self.apply()

    @property
    def columns(self) -> int:
        return self._columns

    @columns.setter
    def columns(self, value: int) -> None:
        self._columns = ParsingTools.parse_non_negative_int(value, "columns")

        self.apply()