from enum import Enum as _Enum
import logging

log = logging.getLogger(__name__)

__all__ = [
    'States',
    'Alignments'
]


class States(_Enum):
    INACTIVE = "INACTIVE"
    HOVERED = "HOVERED"
    PRESSED = "PRESSED"
    DISABLED = "DISABLED"


class Alignments(_Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    CENTER = "CENTER"
    TOP = "TOP"
    BOTTOM = "BOTTOM"
    MIDDLE = "CENTER"  # middle and center are the same thing


_THEME_COLOR_ELEMENTS = [
    "primary",
    "primary-variant",
    "secondary",
    "secondary-variant",
    "background",
    "surface",
    "error",
    "on-primary",
    "on-secondary",
    "on-background",
    "on-surface",
    "on-error",
    "brightness-offsets"
]

SMART_ROUNDED_CORNERS_MULTIPLIER = 7  # Lower = more rounded corners

COLOR_RESET = "RESET"

DEFAULT_TEXT = "hello!"

VERSION_MAJOR = 0
VERSION_MINOR = 3
VERSION_PATCH = 0

VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"


def dummy_function():
    pass
