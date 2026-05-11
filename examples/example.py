import pygame
import buttonup
from buttonup.utils import CallbackPackage, Alignment
from examples.example_button import ButtonExample

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
        self.dt = 0.0

        self.theme = buttonup.theme.load_theme("dark")

        self.example_instances = {
            "button": ButtonExample(WINDOW_WIDTH, WINDOW_HEIGHT),
        }

        self.selection_box = self._generate_selection_vbox()

        self.example_instance = None

    def _generate_selection_vbox(self) -> buttonup.VBox:
        vbox = buttonup.VBox(x=0, y=0, width=200, height=400)

        for example_name in self.example_instances.keys():
            button = buttonup.TextButton(
                x=0, y=0, theme=self.theme, text=example_name,
                on_click=CallbackPackage(callback=self.select_example, args=(example_name,), kwargs={})
            )
            vbox.add(button)

        vbox.apply()

        vbox.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        return vbox

    def select_example(self, example_name: str) -> None:
        self.example_instance = self.example_instances[example_name]

    def draw(self) -> None:
        self.window.fill(self.theme.color.background)

        if self.example_instance:
            self.example_instance.draw(self.window)
        else:
            self.selection_box.draw(self.window)

        pygame.display.flip()

    def update(self) -> None:
        if self.example_instance:
            self.example_instance.update(self.dt)
        else:
            self.selection_box.update(self.dt)

    def events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.example_instance:
                self.example_instance.handle_event(event)
            else:
                self.selection_box.handle_event(event)

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