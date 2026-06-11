import pygame
import buttonup
from base import ExampleBase


class ExampleTextInput(ExampleBase):
    def __init__(self, WINDOW_WIDTH: int, WINDOW_HEIGHT: int) -> None:
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.theme = buttonup.theme.load_theme("dark")

        self.text_input = buttonup.TextInput(
            x=50, y=100, theme=self.theme, text=""
        )

        self.vbox = buttonup.Grid(x=50, y=200, width=130, height=200, row_height=50, columns=2)
        self.text_boxes_focus_example: list[buttonup.TextInput] = []

        for i in range(4):
            text_input = buttonup.TextInput(
                x=0, y=0, width=50, height=50, theme=self.theme, placeholder="...", on_submit=buttonup.CallbackPackage(self.focus_next_text_input, (i,), {})
            )
            self.text_boxes_focus_example.append(text_input)
            self.vbox.add(text_input)

        self.vbox.apply()

    def focus_next_text_input(self, current_text_input_index: int) -> None:
        for text_input in self.text_boxes_focus_example:
            text_input.focused = False

        # Focus index at i + 1
        next_index = (current_text_input_index + 1)

        if next_index < len(self.text_boxes_focus_example):
            self.text_boxes_focus_example[next_index].focused = True

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self.theme.color.background)
        self.text_input.draw(surface)
        self.vbox.draw(surface)

    def update(self, dt: float) -> None:
        self.text_input.update(dt)
        self.vbox.update(dt)

    def handle_event(self, event: pygame.event.Event) -> None:
        self.text_input.handle_event(event)
        self.vbox.handle_event(event)