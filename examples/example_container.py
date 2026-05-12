import random
import pygame
import buttonup
from base import ExampleBase


class Rectangle(buttonup.element.SizedElement, buttonup.element.Element):
    def __init__(self, x: int, y: int, width: int, height: int, color: buttonup.types.RGB) -> None:
        super().__init__(x, y, width, height)
        self.color = color

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)


class ExampleContainer(ExampleBase):
    def __init__(self, WINDOW_WIDTH: int, WINDOW_HEIGHT: int) -> None:
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.theme = buttonup.theme.load_theme("dark")

        self._container_box = buttonup.VBox(
            x=50, y=50, width=200, height=370, padding=10, spacing=10,
            overflow_behavior=buttonup.container.PerpendicularOverflowBehaviour.FIXED
        )

        self.generate_elements()
        self._container_box.apply()

    def generate_elements(self) -> None:
        for i in range(10):
            rectangle = Rectangle(
                x=0, y=0, width=random.choice([50, 150]), height=random.choice([50, 100, 150]),
                color=(255, 255, 0)
            )
            self._container_box.add(rectangle)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self.theme.color.background)
        self._container_box.draw(surface)
        self._container_box.debug_draw(surface)

    def update(self, dt: float) -> None:
        self._container_box.update(dt)

    def handle_event(self, event: pygame.event.Event) -> None:
        pass