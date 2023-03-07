from .Elements import button
from .Elements import label
from .Themes import themes
from .Tools import colors
from .constants import States

import pygame

__all__ = ["button", "label", "themes", "globs", "colors", "States"]


print(f"buttonup {constants.VERSION}")

if not pygame.get_init():
    pygame.init()
