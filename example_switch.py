import pygame
import buttonup
from buttonup.elements.element import DraggableElement, Element

pygame.init()

DISPLAY_INFO = pygame.display.Info()

WINDOW_WIDTH = min(DISPLAY_INFO.current_w, 1920)
WINDOW_HEIGHT = min(DISPLAY_INFO.current_h, 1080)
WINDOW_FPS = 165

pygame.font.init()


class MainWindow:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.theme = buttonup.theme.load_theme("dark")

        self.switch = buttonup.Switch(x=50, y=50, theme=self.theme, on_click=self.on_click)

        self.dt = 0.0

    def on_click(self) -> None:
        print("user click")

    def draw(self) -> None:
        self.window.fill(self.theme.color.background)

        self.switch.draw(self.window)

        pygame.display.flip()

    def update(self) -> None:
        self.switch.update(self.dt)

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