import pygame
import buttonup
from buttonup.utils import CallbackPackage, Alignment
from examples.example_all import ExampleAll
from examples.example_button import ExampleButton
from examples.example_checkbox import ExampleCheckbox
from examples.example_container import ExampleContainer
from examples.example_label import ExampleLabel
from examples.example_richtext import ExampleRichText
from examples.example_slider import ExampleSlider
from examples.example_switch import ExampleSwitch
from examples.example_text_input import ExampleTextInput
from buttonup.logging_config import setup_logging
from examples.example_textbox import ExampleTextBox

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
        self.dt = 0.0

        self.theme = buttonup.theme.load_theme("dark")

        self.example_instances = {
            "all": ExampleAll(WINDOW_WIDTH, WINDOW_HEIGHT),
            "button": ExampleButton(WINDOW_WIDTH, WINDOW_HEIGHT),
            "checkbox": ExampleCheckbox(WINDOW_WIDTH, WINDOW_HEIGHT),
            "container": ExampleContainer(WINDOW_WIDTH, WINDOW_HEIGHT),
            "label": ExampleLabel(WINDOW_WIDTH, WINDOW_HEIGHT),
            "richtext": ExampleRichText(WINDOW_WIDTH, WINDOW_HEIGHT),
            "switch": ExampleSwitch(WINDOW_WIDTH, WINDOW_HEIGHT),
            "text_input": ExampleTextInput(WINDOW_WIDTH, WINDOW_HEIGHT),
            "slider": ExampleSlider(WINDOW_WIDTH, WINDOW_HEIGHT),
            "text_box": ExampleTextBox(WINDOW_WIDTH, WINDOW_HEIGHT)
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

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.example_instance = None

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
    setup_logging(debug=True)

    window = MainWindow()
    window.run()


if __name__ == "__main__":
    main()