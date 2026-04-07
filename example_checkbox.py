import pygame
import buttonup
from buttonup.elements.checkbox import CheckStyle
from buttonup.utils import CallbackPackage, Alignment

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

        self.checkbox = buttonup.Checkbox(
            x=50, y=100, theme=self.theme, on_toggle=CallbackPackage(self.on_checkbox_toggle, (), {}),
            text="Hello!", check_style=CheckStyle.CHECK, border_radius=7
        )

        self.dt = 0.0

    def on_checkbox_toggle(self, checked: bool) -> None:
        print(f"Checkbox is now {'checked' if checked else 'unchecked'}")

    def draw(self) -> None:
        self.window.fill(self.theme.color.background)
        self.checkbox.draw(self.window)
        # self.checkbox.debug_draw(self.window)
        pygame.display.flip()

    def update(self) -> None:
        self.checkbox.update(self.dt)

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