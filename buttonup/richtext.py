import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import SupportsInt, Dict, Tuple, List, Union, Optional, Literal

import pygame

from . import constants
from .buttonup_types import RGB, FontLike, ColorLike
from .elements.element import FontElement
from .utils import ColorTools


class _DefaultColorFlag:
    def __repr__(self) -> str:
        return "<DEFAULT_COLOR_FLAG>"

    def __str__(self) -> str:
        return "<DEFAULT_COLOR_FLAG>"


DEFAULT_COLOR_FLAG = _DefaultColorFlag()


@dataclass
class TextStyle:
    color: Union[RGB, _DefaultColorFlag] = None
    background_color: Union[RGB, _DefaultColorFlag] = None
    bold: bool = None
    italic: bool = None
    underline: bool = None
    strikethrough: bool = None

    def get_bold(self) -> bool:
        return self.bold if self.bold is not None else False

    def get_italic(self) -> bool:
        return self.italic if self.italic is not None else False

    def get_underline(self) -> bool:
        return self.underline if self.underline is not None else False

    def get_strikethrough(self) -> bool:
        return self.strikethrough if self.strikethrough is not None else False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextStyle):
            raise NotImplementedError(f"Cannot compare TextStyle with {type(other)}.")
        return (
                self.color == other.color
                and self.background_color == other.background_color
                and self.bold == other.bold
                and self.italic == other.italic
                and self.underline == other.underline
                and self.strikethrough == other.strikethrough
        )

    def __repr__(self) -> str:
        fields = []
        if self.color is not None:
            fields.append(f"color={self.color}")
        if self.background_color is not None:
            fields.append(f"background_color={self.background_color}")
        if self.bold is not None:
            fields.append(f"bold={self.bold}")
        if self.italic is not None:
            fields.append(f"italic={self.italic}")
        if self.underline is not None:
            fields.append(f"underline={self.underline}")
        if self.strikethrough is not None:
            fields.append(f"strikethrough={self.strikethrough}")
        return f"TextStyle({', '.join(fields)})"


@dataclass(slots=True)
class TextSpan:
    text: str
    style: TextStyle

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextSpan):
            return NotImplemented
        return self.text == other.text and self.style == other.style


@dataclass(slots=True)
class RenderFormText:
    span: TextSpan
    surface: pygame.Surface
    width: int


class RichText(FontElement):
    def __init__(self, spans: List[TextSpan], font: FontLike = None, font_size: SupportsInt = None,
                 default_text_color: ColorLike = None) -> None:
        if font is None:
            font = constants.DEFAULT_FONT_NAME

        if font_size is None:
            font_size = constants.DEFAULT_FONT_SIZE

        super().__init__(font=font, font_size=font_size)

        if default_text_color is None:
            default_text_color = (255, 255, 255)

        self._default_text_color = self._parse_text_color(default_text_color)

        self._spans = self._parse_spans(spans)

        self._rendered_forms: List[RenderFormText] = []
        self.render()

    def _parse_spans(self, spans: List[TextSpan]) -> List[TextSpan]:
        if not isinstance(spans, list):
            raise TypeError(f"Spans must be of type 'list', not '{type(spans)}'.")
        for span in spans:
            if not isinstance(span, TextSpan):
                raise TypeError(f"All items in spans must be of type 'TextSpan', not '{type(span)}'.")
        return spans.copy()

    def _parse_text_color(self, color: ColorLike) -> RGB:
        if ColorTools.is_color(color):
            return ColorTools.to_rgb(color)
        else:
            raise TypeError(f"Default text color must be a valid color format, not '{color}'.")

    def _set_font_parameters(self, style: TextStyle) -> None:
        self._font.set_bold(style.get_bold())
        self._font.set_italic(style.get_italic())
        self._font.set_underline(style.get_underline())

    @staticmethod
    def _apply_strikethrough(surface: pygame.Surface, color: RGB) -> None:
        strike_width = max(1, surface.get_height() // 15)
        strike_y = surface.get_height() // 2

        pygame.draw.line(surface, color, (0, strike_y), (surface.get_width(), strike_y), strike_width)

    @property
    def rendered_forms(self) -> List[RenderFormText]:
        return self._rendered_forms.copy()

    def render(self) -> None:
        rendered_forms: List[RenderFormText] = []

        for span in self._spans:
            self._set_font_parameters(span.style)


            if span.style.color == DEFAULT_COLOR_FLAG or span.style.color is None:
                foreground_color = self._default_text_color
            else:
                foreground_color = span.style.color

            if span.style.background_color == DEFAULT_COLOR_FLAG or span.style.background_color is None:
                background_color = None
            else:
                background_color = span.style.background_color

            text_surface = self._font.render(
                span.text,
                True,
                foreground_color,
                background_color
            )

            if span.style.get_strikethrough():
                self._apply_strikethrough(text_surface, foreground_color)

            rendered_forms.append(RenderFormText(
                span=span,
                surface=text_surface,
                width=text_surface.get_width()
            ))

        self._rendered_forms = rendered_forms

    def _update_font_and_size(self, font: FontLike, font_size: SupportsInt) -> None:
        super()._update_font_and_size(font, font_size)
        self.render()


class RichTextParser(ABC):
    @abstractmethod
    def parse(self) -> List[TextSpan]:
        pass


class InlineDeveloperParser(RichTextParser):
    """
    A simple parser for custom inline markup.

    This is based on the typical Minecraft formatting codes using § or in this case & as the marker, followed by a
    single character code for the style.

    For example:
    &cHello &6world&r!

    would produce "Hello " in red, "world" in gold, and "!" in the default style.

    The legacy codes are implemented by the following mapping:
    - &0: Black
    - &1: Dark Blue
    - &2: Dark Green
    - &3: Dark Cyan
    - &4: Dark Red
    - &5: Dark Magenta
    - &6: Gold
    - &7: Gray
    - &8: Dark Gray
    - &9: Blue
    - &a: Green
    - &b: Cyan
    - &c: Red
    - &d: Magenta
    - &e: Yellow
    - &f: White
    - &l: Bold
    - &o: Italic
    - &n: Underline
    - &m: Strikethrough
    - &r: Reset to default style

    Furthermore, the parser is extended to implement following additional features:

    - &&: Escaped ampersand, produces a literal '&' character without changing the style. Only works if the set
    character is '&'.
    - &B: Background color, followed by a single character code. For example, &B4 would set the background color to dark
    red.
    - &#: Followed by 6 hexadecimal digits, sets the text color to the specified RGB value. For example, &#FF0000
    - &B#: Followed by 6 hexadecimal digits, sets the background color to the specified RGB value. For example, &B#00FF00.
    """

    DEFAULT_OPERATION_CHARACTER = "&"

    COLOR_CODE_MAPPING: Dict[str, RGB] = {
        "0": (0, 0, 0),  # Black
        "1": (0, 0, 170),  # Dark Blue
        "2": (0, 170, 0),  # Dark Green
        "3": (0, 170, 170),  # Dark Cyan
        "4": (170, 0, 0),  # Dark Red
        "5": (170, 0, 170),  # Dark Magenta
        "6": (255, 170, 0),  # Gold
        "7": (170, 170, 170),  # Gray
        "8": (85, 85, 85),  # Dark Gray
        "9": (85, 85, 255),  # Blue
        "a": (85, 255, 85),  # Green
        "b": (85, 255, 255),  # Cyan
        "c": (255, 85, 85),  # Red
        "d": (255, 85, 255),  # Magenta
        "e": (255, 255, 85),  # Yellow
        "f": (255, 255, 255),  # White
    }

    _HEX_COLOR_PATTERN = re.compile(r"^[0-9A-Fa-f]{6}$")

    def __init__(self, text: str, operation_character: str = None) -> None:
        if operation_character is None:
            operation_character = self.DEFAULT_OPERATION_CHARACTER

        self._operation_character = self._parse_operation_character(operation_character)
        self._text = self._parse_text(text)
        self._index = 0
        self._styles_and_text: List[Union[TextStyle, str]] = []

    @staticmethod
    def _parse_text(text: str) -> str:
        if not isinstance(text, str):
            raise TypeError(f"Text to parse must be of type 'str', not '{type(text)}'.")
        return text

    @staticmethod
    def _parse_operation_character(char: str) -> str:
        if not isinstance(char, str) or len(char) != 1:
            raise ValueError(
                f"Operation character must be a single character string, not '{char}'."
            )
        return char

    def parse(self) -> List[TextSpan]:
        """
        Parse the stored text and return a list of fully-resolved TextSpans.

        Each span carries the complete style state that was active when that
        run of characters was encountered.  Adjacent spans with identical
        styles are merged automatically to keep the output compact.
        """
        self._reset_state()
        self._tokenise()
        return self._resolve_tokens()

    def _reset_state(self) -> None:
        self._index = 0
        self._styles_and_text = []

    def _tokenise(self) -> None:
        """
        Walk `_text` left-to-right and fill `_styles_and_text` with a flat
        sequence of `TextStyle` objects (directives) and plain `str` chunks.
        """
        while self._index < len(self._text):
            current_char = self._current_char()

            if current_char == self._operation_character:
                self._consume_operation()
            else:
                self._consume_literal_char(current_char)

    def _consume_literal_char(self, ch: str) -> None:
        """Append a single non-operation character to the token stream."""
        self._styles_and_text.append(ch)
        self._index += 1

    def _consume_operation(self) -> None:
        """
        The current character is the operation character.  Decide which
        escape sequence follows and delegate accordingly.
        """
        # Peek at what comes after the operation character.
        next_char = self._peek(offset=1)

        if next_char is None:
            # Trailing operation character with nothing after it – treat as literal.
            self._consume_literal_char(self._operation_character)
            return

        if next_char == self._operation_character:
            self._styles_and_text.append(self._operation_character)
            self._index += 2
            return

        # &B → background modifier (followed by either '#' or a palette code).
        if next_char == "B":
            self._consume_background_operation()
            return

        # &# → 24-bit foreground hex colour.
        if next_char == "#":
            self._consume_hex_color_operation(is_background=False)
            return

        # &<palette-code> → foreground colour or text-decoration toggle.
        self._consume_palette_or_decoration_operation(next_char)

    def _consume_background_operation(self) -> None:
        """
        Parse `&B<code>` or `&B#<rrggbb>` and emit a background TextStyle.

        If the token is malformed the whole sequence is treated as literal text
        so the end user sees exactly what was typed rather than silent corruption.
        """
        # After &B we expect either '#' (hex) or a palette character.
        char_after_b_code = self._peek(offset=2)

        if char_after_b_code is None:
            # &B with nothing after it – treat &B as literal.
            self._consume_literal_char(self._operation_character)
            return

        if char_after_b_code == "#":
            self._consume_hex_color_operation(is_background=True)
            return

        # Otherwise expect a single palette code character.
        color = self.COLOR_CODE_MAPPING.get(char_after_b_code)
        if color is None:
            # Unrecognised code – emit the three characters literally.
            for i in range(3):
                char = self._peek(offset=i)
                if char is not None:
                    self._styles_and_text.append(char)

            self._index += 3
            return

        self._styles_and_text.append(TextStyle(background_color=color))
        self._index += 3  # consume op + 'B' + code

    def _consume_hex_color_operation(self, is_background: bool) -> None:
        """
        Parse `&#<rrggbb>` (foreground) or `&B#<rrggbb>` (background).

        `is_background` controls whether the B modifier is present.
        The offset to the '#' character differs accordingly:
          - foreground: op '#' hex×6   → total width 8, '#' at offset 1
          - background: op 'B' '#' hex×6 → total width 9, '#' at offset 2
        """
        hash_offset = 2 if is_background else 1
        hex_start = hash_offset + 1  # first hex digit
        total_width = hex_start + 6  # chars consumed in total

        hex_str = self._peek_slice(offset=hex_start, length=6)

        if hex_str is None or not self._HEX_COLOR_PATTERN.match(hex_str):
            # Malformed – emit everything up to where we stopped as literals.
            for i in range(min(total_width, len(self._text) - self._index)):
                char = self._peek(offset=i)
                if char is not None:
                    self._styles_and_text.append(char)

            self._index += min(total_width, len(self._text) - self._index)
            return

        color = ColorTools.to_rgb(hex_str)
        style = (
            TextStyle(background_color=color) if is_background else TextStyle(color=color)
        )
        self._styles_and_text.append(style)
        self._index += total_width

    def _consume_palette_or_decoration_operation(self, code: str) -> None:
        """
        Parse `&<code>` where `code` is a single palette or decoration character.

        Unknown codes are emitted as literal text (the op char + code char).
        """
        style = self._build_style_for_code(code)

        if style is None:
            # Unrecognised code – pass both characters through literally.
            self._styles_and_text.append(self._operation_character)
            self._styles_and_text.append(code)
            self._index += 2
            return

        self._styles_and_text.append(style)
        self._index += 2  # consume op + code

    def _build_style_for_code(self, code: str) -> Optional[TextStyle]:
        """
        Return the TextStyle that corresponds to a single-character code, or
        None when the code is not part of the known vocabulary.
        """
        # Palette colour codes.
        color = self.COLOR_CODE_MAPPING.get(code)
        if color is not None:
            return TextStyle(color=color)

        # Decoration and control codes.
        decoration_map: Dict[str, TextStyle] = {
            "l": TextStyle(bold=True),
            "o": TextStyle(italic=True),
            "n": TextStyle(underline=True),
            "m": TextStyle(strikethrough=True),
            "r": TextStyle(color=DEFAULT_COLOR_FLAG, background_color=DEFAULT_COLOR_FLAG, bold=False, italic=False,
                           underline=False, strikethrough=False),
        }
        return decoration_map.get(code)

    def _current_char(self) -> str:
        return self._text[self._index]

    def _peek(self, offset: int) -> Optional[str]:
        """Return the character at `_index + offset`, or None if out of range."""
        pos = self._index + offset
        return self._text[pos] if pos < len(self._text) else None

    def _peek_slice(self, offset: int, length: int) -> Optional[str]:
        """
        Return a slice of `length` characters starting at `_index + offset`,
        or None if the slice would extend past the end of the string.
        """
        start = self._index + offset
        end = start + length
        if end > len(self._text):
            return None
        return self._text[start:end]

    def _resolve_tokens(self) -> List[TextSpan]:
        """
        Walk the flat token list produced by _tokenise and return a list of
        TextSpans with fully resolved styles.

        Adjacent character tokens that share an identical resolved style are merged
        into a single span to keep the output compact.
        """
        current_style = TextStyle()
        spans: List[TextSpan] = []
        pending_chars: List[str] = []

        for token in self._styles_and_text:
            if isinstance(token, TextStyle):
                self._flush_pending_chars(pending_chars, current_style, spans)
                current_style = self._apply_directive(current_style, token)
            else:
                pending_chars.append(token)

        self._flush_pending_chars(pending_chars, current_style, spans)
        return spans

    def _apply_directive(self, current_style: TextStyle, directive: TextStyle) -> TextStyle:
        """
        Return a new TextStyle that represents `current_style` with `directive`
        merged in.

        Color fields: None = no change, DEFAULT_COLOR_FLAG = clear, RGB = set.
        Bool fields:   None = no change, bool = set.
        """
        return TextStyle(
            color=directive.color if directive.color is not None else current_style.color,
            background_color=directive.background_color if directive.background_color is not None else current_style.background_color,
            bold=directive.bold if directive.bold is not None else current_style.bold,
            italic=directive.italic if directive.italic is not None else current_style.italic,
            underline=directive.underline if directive.underline is not None else current_style.underline,
            strikethrough=directive.strikethrough if directive.strikethrough is not None else current_style.strikethrough,
        )

    @staticmethod
    def _flush_pending_chars(
            pending: List[str],
            current_style: TextStyle,
            spans: List[TextSpan],
    ) -> None:
        """
        Drain `pending` into a new TextSpan, merging with the previous span when
        the resolved style is identical. Clears `pending` in place.
        """
        if not pending:
            return

        text = "".join(pending)
        pending.clear()

        if spans and spans[-1].style == current_style:
            spans[-1] = TextSpan(text=spans[-1].text + text, style=current_style)
        else:
            spans.append(TextSpan(text=text, style=current_style))
