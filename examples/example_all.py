import pygame
import buttonup
from base import ExampleBase


class ExampleAll(ExampleBase):
    def __init__(self, WINDOW_WIDTH: int, WINDOW_HEIGHT: int) -> None:
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.theme = buttonup.theme.load_theme("dark")

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

        self.switch = buttonup.Switch(x=0, y=0, theme=self.theme, text="Toggle me!")

        self.vbox = buttonup.VBox(x=50, y=200, width=600, height=600)
        self.vbox.add(self.label1)
        self.vbox.add(self.button1)
        self.vbox.add(self.button2)
        self.vbox.add(self.panel)
        self.vbox.add(self.text_input)
        self.vbox.add(self.switch)
        self.vbox.apply()

    def char_transform_function(self, char: str) -> str:
        return char.upper()

    def toggle_text_input(self, state: bool) -> None:
        if not state:
            self.text_input.enable()
        else:
            self.text_input.disable()

    def toggle_checkbox(self) -> None:
        if self.checkbox.state == buttonup.InteractionState.DISABLED:
            self.checkbox.enable()
        else:
            self.checkbox.disable()

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self.theme.color.background)
        self.vbox.draw(surface)

    def update(self, dt: float) -> None:
        self.vbox.update(dt)

    def handle_event(self, event: pygame.event.Event) -> None:
        self.vbox.handle_event(event)