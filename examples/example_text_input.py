import pygame
import buttonup
from base import ExampleBase


class ExampleTextInput(ExampleBase):
    def __init__(self, WINDOW_WIDTH: int, WINDOW_HEIGHT: int) -> None:
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.theme = buttonup.theme.load_theme("dark")

        self.text_input = buttonup.TextInput(
            x=50, y=100, theme=self.theme, text=""
        )

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self.theme.color.background)
        self.text_input.draw(surface)

    def update(self, dt: float) -> None:
        self.text_input.update(dt)

    def handle_event(self, event: pygame.event.Event) -> None:
        self.text_input.handle_event(event)