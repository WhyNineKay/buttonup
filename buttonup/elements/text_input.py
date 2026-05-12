from typing import SupportsInt, Callable, Union

import pygame

from .element import ResizableElement, ThemedElement, InteractiveElement, BorderedElement
from .label import Label
from .. import constants
from ..buttonup_types import FontLike, Callback, RGB
from ..theme import ThemeLike, load_default_theme
from ..utils import CallbackPackage, UNINITIALIZED_COLOR, InteractionState, dummy_function, ParsingTools
import string

WORD_CHARACTERS = string.ascii_letters + string.digits + "_"
SEPERATOR_CHARACTERS = string.punctuation.replace("_", "") + " "


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

        self._label_clipping_surface = pygame.Surface(
            (self._width, self._height), pygame.SRCALPHA
        )

        self._base_color: RGB = UNINITIALIZED_COLOR
        self._base_color_focused: RGB = UNINITIALIZED_COLOR
        self._base_color_hovered: RGB = UNINITIALIZED_COLOR
        self._base_color_disabled: RGB = UNINITIALIZED_COLOR
        self._border_color: RGB = UNINITIALIZED_COLOR
        self._border_color_focused: RGB = UNINITIALIZED_COLOR
        self._border_color_hovered: RGB = UNINITIALIZED_COLOR
        self._border_color_disabled: RGB = UNINITIALIZED_COLOR
        self._text_color: RGB = UNINITIALIZED_COLOR
        self._text_color_focused: RGB = UNINITIALIZED_COLOR
        self._text_color_hovered: RGB = UNINITIALIZED_COLOR
        self._text_color_disabled: RGB = UNINITIALIZED_COLOR
        self._placeholder_color: RGB = UNINITIALIZED_COLOR
        self._caret_color: RGB = UNINITIALIZED_COLOR

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
        super()._update_colors()
    
    def _init_colors(self) -> None:
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

        self._text_label.text_color = self._text_color
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

    def _available_text_width(self) -> int:
        return max(0, self._width - 2 * self._text_padding)

    def _cursor_text_x(self) -> int:
        return self._text_label.font.size(self._text_label.text[:self._cursor_pos])[0]

    def _ensure_cursor_visible(self) -> None:
        text_width = self._text_label.width
        available_width = self._available_text_width()

        if text_width <= available_width:
            self._text_label.x = self._text_padding
            return

        min_label_x = self._text_padding - (text_width - available_width)
        max_label_x = self._text_padding

        caret_x = self._text_label.x + self._cursor_text_x()
        left_bound = self._text_padding
        right_bound = self._width - self._text_padding

        if caret_x < left_bound:
            self._text_label.x += left_bound - caret_x
        elif caret_x > right_bound:
            self._text_label.x -= caret_x - right_bound

        self._text_label.x = max(min_label_x, min(max_label_x, self._text_label.x))

    def _set_cursor_pos(self, cursor_pos: int) -> None:
        self._cursor_pos = max(0, min(len(self._text_label.text), cursor_pos))
        self._ensure_cursor_visible()

    def _move_cursor_from_click(self, mouse_x: int) -> None:
        local_x = int(mouse_x) - self._x
        text_x = local_x - self._text_label.x

        if text_x <= 0:
            self._set_cursor_pos(0)
            return

        text = self._text_label.text

        if text == "":
            self._set_cursor_pos(0)
            return

        previous_width = 0
        font = self._text_label.font

        for index in range(1, len(text) + 1):
            current_width = font.size(text[:index])[0]

            if current_width >= text_x:
                if abs(text_x - previous_width) <= abs(current_width - text_x):
                    self._set_cursor_pos(index - 1)
                else:
                    self._set_cursor_pos(index)
                return

            previous_width = current_width

        self._set_cursor_pos(len(text))

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

        # Position labels relatively
        self._text_label.x = self._text_padding
        self._text_label.centery = self._height / 2

        self._placeholder_label.x = self._text_label.x
        self._placeholder_label.centery = self._text_label.centery
        self._ensure_cursor_visible()

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

        # Fill the label clipping surface with the text or placeholder
        self._label_clipping_surface.fill((0, 0, 0, 0))  # Clear with transparent

        # Draw the text or placeholder
        if len(self._text_label.text) == 0:
            self._placeholder_label.draw(self._label_clipping_surface)
        else:
            self._text_label.draw(self._label_clipping_surface)

        # Blit the clipping surface onto the main surface with appropriate offset
        surface.blit(self._label_clipping_surface, (self._x, self._y))

        # Draw the cursor if focused
        if self._focused and self._cursor_visible:
            # Draw a rect
            cursor_x = self._x + self._text_label.x + \
                       self._text_label.font.size(self._text_label.text[:self._cursor_pos])[0]
            cursor_y = self._y + self._text_label.y
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

    def _update_label_text(self, new_text: str) -> None:
        self._text_label.text = new_text
        self._on_change.call()
        self._set_cursor_pos(self._cursor_pos)

    def _key_backspace(self) -> None:
        # Delete before cursor pos
        if self._cursor_pos <= 0:
            return

        if pygame.key.get_mods() & pygame.KMOD_CTRL:
            delta = self._word_offset_delta(-1)

            if delta == 0:
                return

            delete_start = self._cursor_pos + delta
            self._cursor_pos = delete_start
            self._update_label_text(
                self._text_label.text[:delete_start] + self._text_label.text[delete_start - delta:]
            )
            return

        self._cursor_pos -= 1
        self._update_label_text(
            self._text_label.text[:self._cursor_pos] + self._text_label.text[self._cursor_pos + 1:]
        )


    def _key_delete(self) -> None:
        # Delete at cursor pos
        if pygame.key.get_mods() & pygame.KMOD_CTRL:
            # Use self._word_offset_delta to find the next word boundary
            delta = self._word_offset_delta(1)

            if delta == 0:
                return

            self._update_label_text(
                self._text_label.text[:self._cursor_pos] + self._text_label.text[self._cursor_pos + delta:]
            )
        else:
            if self._cursor_pos < len(self._text_label.text):
                self._update_label_text(
                    self._text_label.text[:self._cursor_pos] + self._text_label.text[self._cursor_pos + 1:]
                )


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
            self._update_label_text(
                self._text_label.text[:self._cursor_pos] + insert_text + self._text_label.text[self._cursor_pos:]
            )
            self._set_cursor_pos(self._cursor_pos + len(insert_text))

    def _key_home(self) -> None:
        self._set_cursor_pos(0)

    def _key_end(self) -> None:
        self._set_cursor_pos(len(self._text_label.text))

    def _key_enter(self) -> None:
        self._on_submit.call()
        self._unfocus()

    def _move_cursor_delta(self, delta: int) -> None:
        self._set_cursor_pos(self._cursor_pos + delta)

    def _key_left(self) -> None:
        if pygame.key.get_mods() & pygame.KMOD_CTRL:
            self._move_cursor_jump_delta(-1)
        else:
            self._move_cursor_delta(-1)

    def _key_right(self) -> None:
        if pygame.key.get_mods() & pygame.KMOD_CTRL:
            self._move_cursor_jump_delta(1)
        else:
            self._move_cursor_delta(1)

    def _unfocus(self) -> None:
        self._focused = False

        # Move label back to default position when unfocusing
        self._text_label.x = self._text_padding

    def _move_cursor_jump_delta(self, direction: int) -> None:
        delta = self._word_offset_delta(direction)
        self._move_cursor_delta(delta)

    def _word_offset_delta(self, direction: int) -> int:
        if direction not in {-1, 1}:
            raise ValueError(f"direction must be -1 or 1, not {direction}.")

        text = self._text_label.text
        text_length = len(text)
        cursor_pos = self._cursor_pos

        if text_length == 0:
            return 0

        if direction > 0:
            if cursor_pos >= text_length:
                return 0

            index = cursor_pos

            # Code-editor style: jump across exactly one run (word or separator).
            current_is_word = text[index] in WORD_CHARACTERS
            while index < text_length and (text[index] in WORD_CHARACTERS) == current_is_word:
                index += 1

            return index - cursor_pos

        if cursor_pos <= 0:
            return 0

        index = cursor_pos

        # Code-editor style: jump left across exactly one run (word or separator).
        current_is_word = text[index - 1] in WORD_CHARACTERS
        while index > 0 and (text[index - 1] in WORD_CHARACTERS) == current_is_word:
            index -= 1

        return index - cursor_pos
