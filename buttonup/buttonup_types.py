from pathlib import Path
from typing import Tuple, Union, Callable

import pygame


RGB = Tuple[int, int, int]
ColorLike = Union[RGB, str, pygame.Color]
Number = Union[int, float]
Callback = Callable[[], None]
FontLike = Union[str, pygame.font.Font, Path]
