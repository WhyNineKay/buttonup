import pygame

from .buttonup_types import RGB, ColorLike

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Tuple


class InteractionState(Enum):
    INACTIVE = auto()
    HOVERED = auto()
    CLICKED = auto()
    DISABLED = auto()


TEMP_COLOR = (0, 0, 0)


class Alignment(Enum):
    CENTER_LEFT = auto()
    CENTER = auto()
    CENTER_RIGHT = auto()
    TOP_LEFT = auto()
    TOP_CENTER = auto()
    TOP_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_CENTER = auto()
    BOTTOM_RIGHT = auto()


@dataclass
class CallbackPackage:
    """Container for a callable with positional and keyword arguments.

    Attributes:
        callback: A callable accepting any positional and keyword arguments.
        args: Tuple of positional arguments to pass to the callable.
        kwargs: Mapping of keyword arguments to pass to the callable.
    """
    callback: Callable[..., Any]
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]

    def call(self) -> None:
        """Invoke the stored callback with the stored arguments."""
        self.callback(*self.args, **self.kwargs)


class Colors:
    RED = (255, 0, 0)
    ORANGE = (255, 165, 0)
    PINK = (255, 0, 255)
    PURPLE = (128, 0, 128)
    BLUE = (0, 0, 255)
    AQUA = (0, 255, 255)
    LIME = (0, 255, 0)
    GREEN = (0, 128, 0)

class ColorTools:
    @classmethod
    def is_hex(cls, value: Any) -> bool:
        if not isinstance(value, str):
            return False
        value = value.lstrip("#")
        if len(value) != 6:
            return False
        try:
            int(value, 16)
            return True
        except ValueError:
            return False

    @classmethod
    def is_rgb(cls, value: Any) -> bool:
        if not isinstance(value, tuple):
            return False
        if len(value) != 3:
            return False
        if not all(isinstance(component, int) for component in value):
            return False
        if not all(0 <= component <= 255 for component in value):
            return False
        return True

    @classmethod
    def is_pygame_color(cls, value: Any) -> bool:
        return isinstance(value, pygame.Color)

    @classmethod
    def is_color(cls, value: Any) -> bool:
        return cls.is_hex(value) or cls.is_rgb(value) or cls.is_pygame_color(value)

    @classmethod
    def to_hex(cls, value: Any) -> str:
        if isinstance(value, str):
            if cls.is_hex(value):
                return value.upper()
            else:
                raise TypeError(f"String value '{value}' is not a valid hex color.")

        elif cls.is_rgb(value):
            return "#" + "".join(f"{component:02X}" for component in value)
        elif cls.is_pygame_color(value):
            return "#" + "".join(f"{component:02X}" for component in value[:3])
        else:
            raise TypeError(f"Value '{value}' is not a valid color format.")

    @classmethod
    def to_rgb(cls, value: Any) -> RGB:
        if cls.is_hex(value):
            value = value.lstrip("#")
            return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))
        elif cls.is_rgb(value):
            return value
        elif cls.is_pygame_color(value):
            return tuple(value[:3])
        else:
            raise TypeError(f"Value '{value}' is not a valid color format.")

    @classmethod
    def get_contrasting_color(cls, color: ColorLike) -> RGB:
        """
        Return either black or white, depending on which has better contrast with the given color.
        """
        rgb = cls.to_rgb(color)
        # Calculate the relative luminance of the color using the formula:
        # L = 0.2126*R + 0.7152*G + 0.0722*B
        luminance = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]

        return (255, 255, 255) if luminance < 128 else (0, 0, 0)



def draw_vertical_plane(surface: pygame.Surface, color: ColorLike, pos: Tuple[int, int], width: int = 1,
                        length: int = 10) -> None:
    half_length = length // 2

    y1 = pos[1] - half_length
    y2 = pos[1] + half_length

    pygame.draw.line(surface, color, (pos[0], y1), (pos[0], y2), width)


def draw_horizontal_plane(surface: pygame.Surface, color: ColorLike, pos: Tuple[int, int], width: int = 1,
                          length: int = 10) -> None:
    half_length = length // 2

    x1 = pos[0] - half_length
    x2 = pos[0] + half_length

    pygame.draw.line(surface, color, (x1, pos[1]), (x2, pos[1]), width)


def generate_debug_image(size: Tuple[int, int], colors: Tuple[RGB, RGB]) -> pygame.Surface:
    surface = pygame.Surface((2, 2))



    surface.set_at((0, 0), colors[0])
    surface.set_at((1, 0), colors[1])
    surface.set_at((0, 1), colors[1])
    surface.set_at((1, 1), colors[0])

    smallest_dimension = min(size)

    return pygame.transform.scale(surface, (smallest_dimension, smallest_dimension))


def apply_surface_border_radius(surface: pygame.Surface, radius: int) -> pygame.Surface:
    if radius <= 0:
        return surface

    # Create a white RGB mask with zero alpha outside the rounded rect.
    # Filling RGB with 255 ensures RGB channels are preserved when we
    # multiply the source surface by the mask; only the alpha channel
    # will be zeroed outside the rounded area.
    mask = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    mask.fill((255, 255, 255, 0))

    rect = mask.get_rect()
    pygame.draw.rect(mask, (255, 255, 255, 255), rect, border_radius=radius)

    # Ensure result has per-pixel alpha so transparency is preserved
    # when the returned surface is blitted onto other surfaces.
    result = surface.copy().convert_alpha()
    # Multiply color and alpha channels by the mask. Because the mask RGB
    # is 255 everywhere, RGB channels remain unchanged; the mask alpha
    # will zero out pixels outside the rounded rect.
    result.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    return result
