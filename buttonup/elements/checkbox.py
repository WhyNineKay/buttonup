from typing import SupportsInt, Union, Optional

import pygame

from .element import InteractionState, InteractiveElement, ResizableElement, ThemedElement
from .label import Label
from ..buttonup_types import Callback, BoolCallback, FontLike, RGB
from ..theme import ThemeLike, load_default_theme, CheckboxTheme
from ..utils import CallbackPackage, TEMP_COLOR, ParsingTools
from .. import constants
from enum import Enum, auto


class CheckStyle(Enum):
    CHECK = auto()
    CROSS = auto()
    FILL = auto()


class Checkbox(InteractiveElement, ThemedElement):
    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 size: SupportsInt = None,
                 theme: ThemeLike = None,
                 text: str = None,
                 font: FontLike = None,
                 font_size: SupportsInt = None,
                 on_toggle: Union[CallbackPackage, BoolCallback] = None,
                 on_hover: Union[CallbackPackage, Callback] = None,
                 border_radius: SupportsInt = None,
                 border_width: SupportsInt = None,
                 text_padding: SupportsInt = None,
                 check_padding: SupportsInt = None,
                 check_style: CheckStyle = None,
                 default_checked: bool = None
                 ) -> None:
        self._checkbox_theme: Optional[CheckboxTheme] = None

        if theme is None:
            theme = load_default_theme()

        ThemedElement.__init__(self, theme=theme)

        if size is None:
            size = constants.DEFAULT_CHECKBOX_SIZE

        if border_radius is None:
            border_radius = constants.DEFAULT_CHECKBOX_BORDER_RADIUS

        self._border_radius = self._parse_border_radius(border_radius)

        if border_width is None:
            border_width = constants.DEFAULT_CHECKBOX_BORDER_WIDTH

        self._border_width = self._parse_border_width(border_width)

        if text is None:
            text = ""

        if font_size is None:
            font_size = constants.DEFAULT_FONT_SIZE

        if font is None:
            font = constants.DEFAULT_FONT_NAME

        if text_padding is None:
            text_padding = constants.DEFAULT_CHECKBOX_TEXT_PADDING

        self._text_padding = self._parse_text_padding(text_padding)

        self._checkbox_label = Label(
            x=0,  # Set to zero, InteractiveElement will call _update_position and update label pos.
            y=0,
            text=text,
            font=font,
            font_size=font_size,
            theme=self.theme
        )

        if on_toggle is None:
            on_toggle = lambda _: None

        self._on_toggle: CallbackPackage = ParsingTools.parse_callback_or_callback_package(on_toggle, "on_toggle")

        if len(self._on_toggle.args) > 0:
            raise ValueError(
                "on_toggle callback cannot have any positional arguments as new checked state will be passed as the only argument when called.")

        self._size = self._parse_size(size)

        if check_padding is None:
            check_padding = constants.DEFAULT_CHECKBOX_CHECK_PADDING

        self._check_padding = self._parse_check_padding(check_padding)

        check_rect_size = self._size - 2 * self._check_padding
        self._check_rect = pygame.Rect(
            0,
            0,
            check_rect_size,
            check_rect_size
        )
        self._checkbox_rect = pygame.Rect(0, 0, self._size, self._size)

        InteractiveElement.__init__(
            self, x=x, y=y, width=0, height=0, on_click=self._on_click_handler, on_hover=on_hover
        )

        self._update_size(self._size)

        if check_style is None:
            check_style = CheckStyle.CHECK

        self._check_style = self._parse_check_style(check_style)

        if default_checked is None:
            default_checked = False

        self._checked = ParsingTools.parse_bool_strict(default_checked, "default_checked")

    def _update_colors(self) -> None:
        self._checkbox_theme = self.theme.checkbox_theme

    def _parse_size(self, size: SupportsInt) -> int:
        return ParsingTools.parse_non_negative_int(size, "size")

    def _parse_border_radius(self, border_radius: SupportsInt) -> int:
        return ParsingTools.parse_non_negative_int(border_radius, "border_radius")

    def _parse_border_width(self, border_width: SupportsInt) -> int:
        return ParsingTools.parse_non_negative_int(border_width, "border_width")

    def _parse_text_padding(self, text_padding: SupportsInt) -> int:
        return ParsingTools.parse_non_negative_int(text_padding, "text_padding")

    def _parse_check_padding(self, check_padding: SupportsInt) -> int:
        return ParsingTools.parse_non_negative_int(check_padding, "check_padding")

    def _parse_check_style(self, check_style: CheckStyle) -> CheckStyle:
        if not isinstance(check_style, CheckStyle):
            raise TypeError(f"check_style must be of type CheckStyle, not '{type(check_style)}'.")

        return check_style

    def _on_click_handler(self) -> None:
        """
        Call the user provided callback with the new checked state.
        """
        self._checked = not self._checked

        self._on_toggle.args = (self._checked,)
        self._on_toggle.call()

    def _update_position(self, x: SupportsInt, y: SupportsInt) -> None:
        super()._update_position(x, y)

        self._checkbox_label.x = self._x + self._size + self._text_padding
        # Try and center the label vertically with the checkbox, but don't let it go above the top of the checkbox if
        # it's too tall.
        self._checkbox_label.y = max(
            self._y + self._size / 2 - self._checkbox_label.height / 2,
            self._y
        )

        self._check_rect.x = self._x + self._check_padding
        self._check_rect.y = self._y + self._check_padding
        self._checkbox_rect.x = self._x
        self._checkbox_rect.y = self._y

    def _update_size(self, size: SupportsInt) -> None:
        """Called to update the size of the checkbox square."""
        self._size = self._parse_size(size)

        self._checkbox_rect.width = self._size
        self._checkbox_rect.height = self._size

        self._update_dimensions(
            width=self._size + self._text_padding + self._checkbox_label.width,
            height=max(self._size, self._checkbox_label.height)
        )

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, value: SupportsInt) -> None:
        self._update_size(value)

    @property
    def checked(self) -> bool:
        return self._checked

    @checked.setter
    def checked(self, value: bool) -> None:
        self._checked = ParsingTools.parse_bool_strict(value, "checked")

    def _get_base_color(self) -> RGB:
        if self._checked:
            return self._checkbox_theme.base_color_checked
        elif self._state == InteractionState.PRESSED:
            return self._checkbox_theme.base_color_pressed
        elif self._state == InteractionState.HOVERED:
            return self._checkbox_theme.base_color_hovered
        else:
            return self._checkbox_theme.base_color

    def _get_border_color(self) -> RGB:
        if self._checked:
            return self._checkbox_theme.border_color_checked
        elif self._state == InteractionState.PRESSED:
            return self._checkbox_theme.border_color_pressed
        elif self._state == InteractionState.HOVERED:
            return self._checkbox_theme.border_color_hovered
        else:
            return self._checkbox_theme.border_color

    def _get_check_color(self) -> RGB:
        if self._checked:
            return self._checkbox_theme.check_color_checked
        elif self._state == InteractionState.PRESSED:
            return self._checkbox_theme.check_color_pressed
        elif self._state == InteractionState.HOVERED:
            return self._checkbox_theme.check_color_hovered
        else:
            return self._checkbox_theme.check_color

    def _get_text_color(self) -> RGB:
        if self._checked:
            return self._checkbox_theme.text_color_checked
        elif self._state == InteractionState.PRESSED:
            return self._checkbox_theme.text_color_pressed
        elif self._state == InteractionState.HOVERED:
            return self._checkbox_theme.text_color_hovered
        else:
            return self._checkbox_theme.text_color

    def draw(self, surface: pygame.Surface) -> None:
        base_color = self._get_base_color()
        border_color = self._get_border_color()
        check_color = self._get_check_color()

        pygame.draw.rect(surface, base_color, self._checkbox_rect, border_radius=self._border_radius)
        pygame.draw.rect(surface, border_color, self._checkbox_rect, width=self._border_width, border_radius=self._border_radius)

        if self._checked:
            self._draw_check(surface, check_color)

        self._checkbox_label.draw(surface)

    def _draw_check(self, surface: pygame.Surface, color: RGB) -> None:
        if self._check_style == CheckStyle.FILL:
            border_radius = max(0, self._border_radius - self._check_padding)
            pygame.draw.rect(surface, color, self._check_rect, border_radius=border_radius)

        elif self._check_style == CheckStyle.CHECK:
            # Draw a checkmark using two lines.
            start_pos = (self._check_rect.left + self._check_rect.width * 0.2, self._check_rect.centery)
            mid_pos = (self._check_rect.centerx, self._check_rect.bottom - self._check_rect.height * 0.2)
            end_pos = (self._check_rect.right - self._check_rect.width * 0.2,
                       self._check_rect.top + self._check_rect.height * 0.2)
            pygame.draw.line(surface, color, start_pos, mid_pos, width=self._border_width)
            pygame.draw.line(surface, color, mid_pos, end_pos, width=self._border_width)

        elif self._check_style == CheckStyle.CROSS:
            # Draw an X using two lines.
            start_pos1 = (self._check_rect.left + self._check_rect.width * 0.2,
                          self._check_rect.top + self._check_rect.height * 0.2)
            end_pos1 = (self._check_rect.right - self._check_rect.width * 0.2,
                        self._check_rect.bottom - self._check_rect.height * 0.2)
            start_pos2 = (self._check_rect.left + self._check_rect.width * 0.2,
                          self._check_rect.bottom - self._check_rect.height * 0.2)
            end_pos2 = (self._check_rect.right - self._check_rect.width * 0.2,
                        self._check_rect.top + self._check_rect.height * 0.2)
            pygame.draw.line(surface, color, start_pos1, end_pos1, width=self._border_width)
            pygame.draw.line(surface, color, start_pos2, end_pos2, width=self._border_width)

    def update(self, dt: float) -> None:
        super().update(dt)

        # Update label text color
        self._checkbox_label.color = self._get_text_color()

    def debug_draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (255, 0, 255), self._checkbox_rect, width=1)
        pygame.draw.rect(surface, (0, 255, 255), self._check_rect, width=1)
        pygame.draw.rect(surface, (255, 255, 0), self._rect, width=1)
        self._checkbox_label.debug_draw(surface)