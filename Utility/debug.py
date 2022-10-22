"""
Debug file.
"""

import pygame

pygame.font.init()


class Debug:
    """Debug class."""

    def __init__(self) -> None:
        self.console_log_call_count = 0
        self.font = pygame.font.SysFont("consolas", 30)

    def console_log(self, text: str) -> None:
        """Print text to console."""
        print(f"{self.console_log_call_count}: {text}")
        self.console_log_call_count += 1

    def pygame_display_text(self, text: str, *, color: tuple = (255, 255, 255),
                            font_size: int = 30, pos_x: int = 300, pos_y: int = 300) -> None:
        """Display text to pygame window."""
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (pos_x, pos_y)
        pygame.display.get_surface().blit(text_surface, text_rect)


debugger = Debug()
