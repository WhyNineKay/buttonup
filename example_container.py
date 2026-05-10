import random
import pygame
import buttonup
from buttonup.buttonup_types import RGB
from buttonup.elements.element import SizedElement, Element
from buttonup.elements.container import PerpendicularOverflowBehaviour

pygame.init()

DISPLAY_INFO = pygame.display.Info()

WINDOW_WIDTH = min(DISPLAY_INFO.current_w, 1920)
WINDOW_HEIGHT = min(DISPLAY_INFO.current_h, 1080)
WINDOW_FPS = 60

pygame.font.init()


class Rectangle(SizedElement, Element):
    def __init__(self, x: int, y: int, width: int, height: int, color: RGB) -> None:
        super().__init__(x, y, width, height)
        self.color = color

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)


class MainWindow:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.theme = buttonup.theme.load_theme("dark")

        self._container_box = buttonup.VBox(
            x=50, y=50, width=200, height=370, padding=10, spacing=10, overflow_behavior=PerpendicularOverflowBehaviour.FIXED
        )

        self.generate_elements()

        self._container_box.apply()

        self.dt = 0.0

    def generate_elements(self) -> None:
        for i in range(10):
            rectangle = Rectangle(x=0, y=0, width=random.choice([50, 150]), height=random.choice([50, 100, 150]),
                                  color=(255, 255, 0))
            self._container_box.add(rectangle)

    def draw(self) -> None:
        self.window.fill(self.theme.color.background)

        self._container_box.draw(self.window)
        self._container_box.debug_draw(self.window)

        pygame.display.flip()

    def update(self) -> None:
        self._container_box.update(self.dt)

    def events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self) -> None:
        while self.running:
            self.events()
            self.update()
            self.draw()

            self.dt = self.clock.tick(WINDOW_FPS) / 1000


def main() -> None:
    window = MainWindow()
    window.run()


if __name__ == "__main__":
    main()
