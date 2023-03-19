from .elements import button
from .elements import label
from .themes import themes
from .tools import colors
from .constants import States

import pygame

__all__ = ["button", "label", "themes", "globs", "colors", "States"]


print(f"buttonup {constants.VERSION}")

if not pygame.get_init():
    pygame.init()
