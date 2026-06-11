import pygame
import buttonup
from base import ExampleBase


class ExampleSlider(ExampleBase):
    def __init__(self, WINDOW_WIDTH: int, WINDOW_HEIGHT: int) -> None:
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.theme = buttonup.theme.load_theme("dark")


        self.vbox = buttonup.VBox(x=100, y=100, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, spacing=20)

        self.slider1 = buttonup.Slider(
            x=0, y=0, theme=self.theme
        )
        self.vbox.add(self.slider1)

        for i in range(3):
            self.vbox.add(
                buttonup.Slider(
                    x=0, y=0, theme=self.theme, step=1 / int(((i+2) ** 1.5))
                )
            )

        self.vbox.add(
            buttonup.Slider(
                x=0, y=0, track_length=100, theme=self.theme
            )
        )

        self.vbox.apply()


    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self.theme.color.background)
        self.vbox.draw(surface)

    def update(self, dt: float) -> None:
        self.vbox.update(dt)
