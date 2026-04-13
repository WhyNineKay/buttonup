from typing import SupportsInt, Callable, Union

import pygame

from .element import ResizableElement, ThemedElement, InteractiveElement, BorderedElement
from .label import Label
from .. import constants
from ..buttonup_types import FontLike, Callback, RGB
from ..theme import ThemeLike, load_default_theme
from ..utils import CallbackPackage, TEMP_COLOR, InteractionState, dummy_function, ParsingTools


class TextInput(InteractiveElement, ResizableElement, ThemedElement, BorderedElement):
    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 width: SupportsInt = None,
                 height: SupportsInt = None,
                 theme: ThemeLike = None,
                 font: FontLike = None,
                 font_size: SupportsInt = None,
                 text: str = None,
                 border_radius: SupportsInt = None,
                 border_width: SupportsInt = None,
                 placeholder: str = None,
                 max_length: SupportsInt = None,
                 allowed_char_filter: Callable[[str], bool] = None,
                 char_transform_function: Callable[[str], str] = None,
                 on_change: Union[Callback, CallbackPackage] = None,
                 on_submit: Union[Callback, CallbackPackage] = None,
                 text_padding: SupportsInt = None
                 ) -> None:
        if border_radius is None:
            border_radius = constants.DEFAULT_TEXTINPUT_BORDER_RADIUS

        if border_width is None:
            border_width = constants.DEFAULT_TEXTINPUT_BORDER_WIDTH

        BorderedElement.__init__(self, border_radius=border_radius, border_width=border_width)

        if width is None:
            width = constants.DEFAULT_TEXTINPUT_WIDTH

        if height is None:
            height = constants.DEFAULT_TEXTINPUT_HEIGHT

        if placeholder is None:
            placeholder = constants.DEFAULT_TEXTINPUT_PLACEHOLDER

        self._placeholder = self._parse_placeholder(placeholder)

        self._text_label = Label(
            x=0, y=0, text=text, theme=theme, font=font, font_size=font_size
        )
        self._placeholder_label = Label(
            x=0, y=0, text=self._placeholder, theme=theme, font=font, font_size=font_size
        )

        if text_padding is None:
            text_padding = constants.DEFAULT_TEXTINPUT_TEXT_PADDING

        self._text_padding = self._parse_text_padding(text_padding)

        if allowed_char_filter is None:
            allowed_char_filter = lambda char: True

        self._allowed_char_filter = self._parse_allowed_char_filter(allowed_char_filter)

        if char_transform_function is None:
            char_transform_function = lambda char: char

        self._char_transform_function = self._parse_char_transform_function(char_transform_function)

        self._max_length: Union[int, None] = self._parse_max_length(max_length)

        self._on_change = self._parse_on_change(on_change)  # will handle None as dummy callback
        self._on_submit = self._parse_on_submit(on_submit)  # ^

        self._width = 0
        self._height = 0

        InteractiveElement.__init__(self, x=x, y=y, width=width, height=height, on_click=self._on_click,
                                    on_hover=self._on_hover)
        self._update_position(self._x, self._y)  # Required to position the text label correctly

        self._base_color: RGB = TEMP_COLOR
        self._base_color_focused: RGB = TEMP_COLOR
        self._base_color_hovered: RGB = TEMP_COLOR
        self._base_color_disabled: RGB = TEMP_COLOR
        self._border_color: RGB = TEMP_COLOR
        self._border_color_focused: RGB = TEMP_COLOR
        self._border_color_hovered: RGB = TEMP_COLOR
        self._border_color_disabled: RGB = TEMP_COLOR
        self._text_color: RGB = TEMP_COLOR
        self._text_color_focused: RGB = TEMP_COLOR
        self._text_color_hovered: RGB = TEMP_COLOR
        self._text_color_disabled: RGB = TEMP_COLOR
        self._placeholder_color: RGB = TEMP_COLOR
        self._caret_color: RGB = TEMP_COLOR

        if theme is None:
            theme = load_default_theme()

        ThemedElement.__init__(self, theme=theme)

        self._focused = False

        self._cursor_pos = 0
        self._cursor_flash_timer = 0.0
        self._cursor_visible = True
        self._cursor_width = max(1, self._text_label.font_size // 5)  # Make cursor width proportional to font size
        self._cursor_height = self._text_label.font.get_height()

    def _update_colors(self) -> None:
        self._base_color = self._theme.text_input_theme.base_color
        self._base_color_focused = self._theme.text_input_theme.base_color_focused
        self._base_color_hovered = self._theme.text_input_theme.base_color_hovered
        self._base_color_disabled = self._theme.text_input_theme.base_color_disabled
        self._border_color = self._theme.text_input_theme.border_color
        self._border_color_focused = self._theme.text_input_theme.border_color_focused
        self._border_color_hovered = self._theme.text_input_theme.border_color_hovered
        self._border_color_disabled = self._theme.text_input_theme.border_color_disabled
        self._text_color = self._theme.text_input_theme.text_color
        self._text_color_focused = self._theme.text_input_theme.text_color_focused
        self._text_color_hovered = self._theme.text_input_theme.text_color_hovered
        self._text_color_disabled = self._theme.text_input_theme.text_color_disabled
        self._placeholder_color = self._theme.text_input_theme.placeholder_color
        self._caret_color = self._theme.text_input_theme.caret_color

        self._text_label._update_colors()
        self._placeholder_label.text_color = self._placeholder_color

    def _parse_char_transform_function(self, char_transform_function: Callable[[str], str]) -> Callable[[str], str]:
        if not callable(char_transform_function):
            raise TypeError(
                f"TextInput char_transform_function must be a callable that takes a single string argument and returns a"
                f"string, not '{type(char_transform_function)}'."
            )
        return char_transform_function

    def _parse_on_change(
            self,
            on_change: Union[Callback, CallbackPackage, None]
    ) -> Union[Callback, CallbackPackage, None]:
        return self._parse_named_callback(on_change, "on_change")

    def _parse_on_submit(
            self,
            on_submit: Union[Callback, CallbackPackage, None]
    ) -> Union[Callback, CallbackPackage, None]:
        return self._parse_named_callback(on_submit, "on_submit")

    def _parse_max_length(self, max_length: Union[SupportsInt, None]) -> Union[int, None]:
        if max_length is None:
            return None

        return ParsingTools.parse_non_negative_int(max_length, "max_length")

    def _parse_allowed_char_filter(self, allowed_char_filter: Callable[[str], bool]) -> Callable[[str], bool]:
        if not callable(allowed_char_filter):
            raise TypeError(
                f"TextInput allowed_char_filter must be a callable that takes a single string argument and returns a"
                f"boolean, not '{type(allowed_char_filter)}'."
            )
        return allowed_char_filter

    def _parse_text_padding(self, text_padding: SupportsInt) -> int:
        return ParsingTools.parse_non_negative_int(text_padding, "text_padding")

    def _parse_placeholder(self, placeholder: str) -> str:
        if not isinstance(placeholder, str):
            raise TypeError(f"TextInput placeholder must be of type 'str', not '{type(placeholder)}'.")
        return placeholder

    def _move_cursor_from_click(self, mouse_x: int) -> None:
        relative_x = mouse_x - self._text_label.x
        pos = 0
        for i in range(len(self._text_label.text) + 1):
            if i < len(self._text_label.text):
                char_width = self._text_label.font.size(self._text_label.text[i])[0]
            else:
                char_width = 0

            if relative_x < char_width / 2:
                break

            relative_x -= char_width
            pos += 1

        self._cursor_pos = pos

        self._reset_cursor_timer()

    def _on_click(self) -> None:
        # Move the clicked position to the cursor
        mouse_x, _ = pygame.mouse.get_pos()
        self._move_cursor_from_click(mouse_x)

        self._focused = True

        self._reset_cursor_timer()

    def _on_hover(self) -> None:
        pass

    def _update_position(self, x: SupportsInt, y: SupportsInt) -> None:
        super()._update_position(x, y)
        self._text_label.x = self._x + self._text_padding
        self._text_label.centery = self._y + self._height / 2
        self._placeholder_label.x = self._text_label.x
        self._placeholder_label.centery = self._text_label.centery

    def draw(self, surface: pygame.Surface) -> None:
        # Draw the text input background and border
        if self._focused:
            base_color = self._base_color_focused
            border_color = self._border_color_focused
            self._text_label.text_color = self._text_color_focused
        elif self._state in {InteractionState.HOVERED, InteractionState.PRESSED}:
            base_color = self._base_color_hovered
            border_color = self._border_color_hovered
            self._text_label.text_color = self._text_color_hovered
        elif self._state == InteractionState.DISABLED:
            base_color = self._base_color_disabled
            border_color = self._border_color_disabled
            self._text_label.text_color = self._text_color_disabled
        else:
            base_color = self._base_color
            border_color = self._border_color
            self._text_label.text_color = self._text_color

        pygame.draw.rect(surface, base_color, self._rect, border_radius=self._border_radius)

        if self._border_width > 0:
            pygame.draw.rect(surface, border_color, self._rect, width=self._border_width,
                             border_radius=self._border_radius)

        # Draw the text or placeholder
        if len(self._text_label.text) == 0:
            self._placeholder_label.draw(surface)
        else:
            self._text_label.draw(surface)

        # Draw the cursor if focused
        if self._focused and self._cursor_visible:
            # Draw a rect
            cursor_x = self._text_label.x + self._text_label.font.size(self._text_label.text[:self._cursor_pos])[0]
            cursor_y = self._text_label.y
            pygame.draw.rect(
                surface,
                self._caret_color,
                (cursor_x, cursor_y, self._cursor_width, self._cursor_height),
                border_radius=self._cursor_width // 2
            )

    def update(self, dt: float) -> None:
        super().update(dt)

        if self._focused:
            self._cursor_flash_timer += dt

            if self._cursor_flash_timer >= constants.CURSOR_FLASH_INTERVAL:
                self._cursor_flash_timer = 0.0
                self._cursor_visible = not self._cursor_visible

            # Detect press outside of the text input to unfocus
            mouse_pos = pygame.mouse.get_pos()
            pressed = pygame.mouse.get_pressed()[0]

            if not self._rect.collidepoint(mouse_pos) and pressed:
                self._unfocus()

    def _key_backspace(self) -> None:
        # Backspace at cursor pos
        if self._cursor_pos > 0:
            self._text_label.text = self._text_label.text[:self._cursor_pos - 1] + self._text_label.text[
                self._cursor_pos:]
            self._cursor_pos -= 1
            self._on_change.call()

    def _key_delete(self) -> None:
        # Delete at cursor pos
        if self._cursor_pos < len(self._text_label.text):
            self._text_label.text = self._text_label.text[:self._cursor_pos] + self._text_label.text[
                self._cursor_pos + 1:]
            self._on_change.call()

    def handle_event(self, event: pygame.event.Event) -> None:
        if not self._focused:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._key_enter()
            elif event.key == pygame.K_BACKSPACE:
                self._key_backspace()
            elif event.key == pygame.K_DELETE:
                self._key_delete()
            elif event.key == pygame.K_LEFT:
                self._key_left()
            elif event.key == pygame.K_RIGHT:
                self._key_right()
            elif event.key == pygame.K_HOME:
                self._key_home()
            elif event.key == pygame.K_END:
                self._key_end()
            else:
                char = event.unicode

                if char.isprintable() and char != "":
                    self._key_char(char)

            self._reset_cursor_timer()

    def _reset_cursor_timer(self) -> None:
        self._cursor_flash_timer = 0.0
        self._cursor_visible = True

    def _key_char(self, char: str) -> None:
        char = self._char_transform_function(char)
        # char_transform_function may return "" or string with multiple characters.

        if not isinstance(char, str) or char == "":
            return

        if not all(self._allowed_char_filter(c) for c in char):
            return

        insert_text = char
        if self._max_length is not None:
            remaining = self._max_length - len(self._text_label.text)
            if remaining <= 0:
                return
            insert_text = insert_text[:remaining]

        if insert_text:
            self._text_label.text = (
                self._text_label.text[:self._cursor_pos] + insert_text + self._text_label.text[self._cursor_pos:]
            )
            self._cursor_pos += len(insert_text)
            self._on_change.call()

    def _key_home(self) -> None:
        self._cursor_pos = 0

    def _key_end(self) -> None:
        self._cursor_pos = len(self._text_label.text)

    def _key_enter(self) -> None:
        self._on_submit.call()
        self._unfocus()

    def _move_cursor_delta(self, delta: int) -> None:
        self._cursor_pos = max(0, min(len(self._text_label.text), self._cursor_pos + delta))

    def _key_left(self) -> None:
        self._move_cursor_delta(-1)

    def _key_right(self) -> None:
        self._move_cursor_delta(1)

    def _unfocus(self) -> None:
        self._focused = False
