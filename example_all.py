import pygame
import buttonup
from buttonup.utils import CallbackPackage, Alignment, InteractionState

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

        self.theme = buttonup.theme.load_theme("night")

        self.label1 = buttonup.Label(
            x=0, y=0, text="This is a label!", theme=self.theme
        )
        self.button1 = buttonup.TextButton(
            x=0, y=0, theme=self.theme, text="Click me!", on_click=self.toggle_checkbox
        )
        self.button2 = buttonup.TextButton(
            x=0, y=0, theme=self.theme, text="Disabled :("
        )
        self.button2.disable()

        self.checkbox = buttonup.Checkbox(
            x=0, y=0, theme=self.theme, text="Check me!", on_toggle=self.toggle_text_input
        )

        self.text_input = buttonup.TextInput(
            x=0, y=0, theme=self.theme, text="", char_transform_function=self.char_transform_function
        )
        self.panel = buttonup.Panel(x=0, y=0, width=200, height=200, theme=self.theme)
        self.panel.element = self.checkbox

        self.vbox = buttonup.VBox(x=50, y=200, width=600, height=600)
        self.vbox.add(self.label1)
        self.vbox.add(self.button1)
        self.vbox.add(self.button2)
        self.vbox.add(self.panel)
        self.vbox.add(self.text_input)
        self.vbox.apply()

        self.dt = 0.0

    def char_transform_function(self, char: str) -> str:
        return char.lower()

    def toggle_text_input(self, state: bool) -> None:
        if not state:
            self.text_input._state = InteractionState.INACTIVE
        else:
            self.text_input._state = InteractionState.DISABLED

    def toggle_checkbox(self) -> None:
        if self.checkbox._state == InteractionState.DISABLED:
            self.checkbox._state = InteractionState.INACTIVE
        else:
            self.checkbox._state = InteractionState.DISABLED


    def draw(self) -> None:
        self.window.fill(self.theme.color.background)
        self.vbox.draw(self.window)
        pygame.display.flip()

    def update(self) -> None:
        self.vbox.update(self.dt)

    def events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.vbox.handle_event(event)

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