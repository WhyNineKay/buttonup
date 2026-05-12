import pygame
import buttonup
from base import ExampleBase


class ExampleSwitch(ExampleBase):
    def __init__(self, WINDOW_WIDTH: int, WINDOW_HEIGHT: int) -> None:
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.theme = buttonup.theme.load_theme("dark")

        self.switch = buttonup.Switch(x=50, y=50, theme=self.theme, on_click=self.on_click)

    def on_click(self) -> None:
        print("user click")

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self.theme.color.background)
        self.switch.draw(surface)

    def update(self, dt: float) -> None:
        self.switch.update(dt)

    def handle_event(self, event: pygame.event.Event) -> None:
        self.switch.handle_event(event)