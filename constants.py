from enum import Enum as _Enum

__all__ = [
    'States'
]


class States(_Enum):
    INACTIVE = "INACTIVE"
    HOVERED = "HOVERED"
    PRESSED = "PRESSED"
    DISABLED = "DISABLED"


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
VERSION_MINOR = 2
VERSION_PATCH = 7

VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"