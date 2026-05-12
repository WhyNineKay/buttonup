import pygame
import buttonup
from buttonup import CallbackPackage, Alignment

pygame.init()

DISPLAY_INFO = pygame.display.Info()

WINDOW_WIDTH = min(DISPLAY_INFO.current_w, 1920)
WINDOW_HEIGHT = min(DISPLAY_INFO.current_h, 1080)
WINDOW_FPS = 60

pygame.font.init()


class MainWindow:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.theme = buttonup.theme.load_theme("dark")

        self.text_input = buttonup.TextInput(
            x=50, y=100, theme=self.theme, text=""
        )

        self.dt = 0.0

    def draw(self) -> None:
        self.window.fill(self.theme.color.background)
        self.text_input.draw(self.window)
        pygame.display.flip()

    def update(self) -> None:
        self.text_input.update(self.dt)

    def events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.text_input.handle_event(event)

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