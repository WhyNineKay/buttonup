import pygame
import buttonup
from base import ExampleBase


class DraggableLabel(buttonup.element.DraggableElement, buttonup.Label):
    def __init__(self, x: int, y: int, theme: buttonup.Theme, text: str) -> None:
        buttonup.Label.__init__(
            self,
            x=x,
            y=y,
            theme=theme,
            text=text
        )

        self._drag_mouse_offset: tuple[int, int] = (0, 0)

        buttonup.element.DraggableElement.__init__(
            self,
            x=x,
            y=y,
            width=self.width,
            height=self.height,
            on_drag_start=self._on_drag_start,
            on_drag=self._on_drag
        )

    def _on_drag_start(self) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self._drag_mouse_offset = (
            mouse_x - self.x,
            mouse_y - self.y
        )

    def _on_drag(self) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        new_x = mouse_x - self._drag_mouse_offset[0]
        new_y = mouse_y - self._drag_mouse_offset[1]

        self._update_position(new_x, new_y)

    def draw(self, surface: pygame.Surface) -> None:
        # Draw rect
        pygame.draw.rect(surface, self._text_color, self.rect, 1, border_radius=5)

        super().draw(surface)

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

        self.slider1 = buttonup.Slider(x=0, y=0, theme=self.theme, step=0.25)
        self.slider2 = buttonup.Slider(x=0, y=0, theme=self.theme, axis=buttonup.Axis.VERTICAL, on_change=self._on_slider2_change)

        self.draggable_label = DraggableLabel(x=0, y=0, theme=self.theme, text="Drag me!")

        self.vbox = buttonup.VBox(x=50, y=200, width=600, height=600)
        self.vbox.add(self.label1)
        self.vbox.add(self.button1)
        self.vbox.add(self.button2)
        self.vbox.add(self.panel)
        self.vbox.add(self.text_input)
        self.vbox.add(self.switch)
        self.vbox.add(self.slider1)
        self.vbox.add(self.slider2)
        self.vbox.apply()

    def _on_slider2_change(self, value: float) -> None:
        self.draggable_label.font_size = 12 + int(value * 24)

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

        self.draggable_label.draw(surface)

    def update(self, dt: float) -> None:
        self.vbox.update(dt)
        self.draggable_label.update(dt)

    def handle_event(self, event: pygame.event.Event) -> None:
        self.vbox.handle_event(event)