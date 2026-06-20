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
        )
        self._grid_box = buttonup.UniformGrid(
            x=300, y=50, width=240, height=240, rows=4, columns=4, padding=0, spacing=0,
            content_alignment=buttonup.Alignment.CENTER,
            fill_order=buttonup.GridFillOrder.COLUMN_FIRST
        )

        colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255))

        for i in range(9):
            rectangle = Rectangle(
                x=0, y=0, width=60, height=60,
                color=colors[i % len(colors)]
            )
            self._grid_box.add(rectangle)

        self._grid_box.apply()

        self._panel = buttonup.Panel(
            x=600, y=50, width=150, height=150, padding=10,
            draw_background=True, element=Rectangle(0, 0, 100, 30, (255, 0, 0)),
            content_alignment=buttonup.Alignment.CENTER_RIGHT
        )
        self._panel.apply()

        # self.generate_elements()
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
        self._grid_box.draw(surface)
        # self._grid_box.debug_draw(surface)
        self._panel.draw(surface)

    def update(self, dt: float) -> None:
        self._container_box.update(dt)

        # mouse_pos = pygame.mouse.get_pos()
        # self._grid_box.width = max(mouse_pos[0] - self._grid_box.x, 0)
        # self._grid_box.height = max(mouse_pos[1] - self._grid_box.y, 0)

    def handle_event(self, event: pygame.event.Event) -> None:
        pass