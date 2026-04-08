import buttonup
import pygame

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

        self._container_box = buttonup.Grid(
            x=50, y=50, width=370, height=370, padding=10, spacing=10, columns=4
        )

        button_names = [
            "C", "±", "%", "÷",
            "7", "8", "9", "×",
            "4", "5", "6", "−",
            "1", "2", "3", "+",
            "0", ".", "="
        ]



        for name in button_names:
            width = 70 if name != "=" else 160
            button = buttonup.TextButton(
                x=0, y=0, width=width, height=70, text=name,
                theme=self.theme,
                on_click=lambda n=name: print(f"Clicked {n}!")
            )

            if name in {"C", "±", "%", "÷", "×", "−", "+", "="}:
                button.border_color = self.theme.color.secondary
                button.border_color_hovered = self.theme.color.primary
                button.border_color_pressed = self.theme.color.primary

            self._container_box.add(button)

        self._container_box.apply()

        self.dt = 0.0

    def draw(self) -> None:
        self.window.fill(self.theme.color.background)

        self._container_box.draw(self.window)
        # self._container_box.debug_draw(self.window)

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
