import pygame
import buttonup
from base import ExampleBase


class ExampleCheckbox(ExampleBase):
    def __init__(self, WINDOW_WIDTH: int, WINDOW_HEIGHT: int) -> None:
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.theme = buttonup.theme.load_theme("dark")

        self.checkbox = buttonup.Checkbox(
            x=50, y=100, theme=self.theme, on_toggle=buttonup.CallbackPackage(self.on_checkbox_toggle, (), {}),
            text="Hello!", check_style=buttonup.CheckStyle.CHECK, border_radius=7
        )

    def on_checkbox_toggle(self, checked: bool) -> None:
        print(f"Checkbox is now {'checked' if checked else 'unchecked'}")

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self.theme.color.background)
        self.checkbox.draw(surface)

    def update(self, dt: float) -> None:
        self.checkbox.update(dt)

    def handle_event(self, event: pygame.event.Event) -> None:
        self.checkbox.handle_event(event)