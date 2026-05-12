import pygame
import buttonup
from buttonup.richtext import RichText, InlineDeveloperParser
from base import ExampleBase


class ExampleRichText(ExampleBase):
    def __init__(self, WINDOW_WIDTH: int, WINDOW_HEIGHT: int) -> None:
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.theme = buttonup.theme.load_theme("dark")

        self.parser = InlineDeveloperParser(
            f"Type &f&&3&3some &f&&l&&4&l&4rich &r&f&&o&&5&5&otext &r&f&&6&6here! {self.generate_color_spectrum()}"
        )

        self.label = buttonup.Label(
            x=50, y=100, text=">", theme=self.theme, font_size=30
        )

        self.previous_text = self.label.text

        self.rich_text = RichText(
            spans=self.parser.parse(), font_size=30
        )

        self.rich_text.render()

    def generate_color_spectrum(self) -> str:
        string = ""
        for c in InlineDeveloperParser.COLOR_CODE_MAPPING.keys():
            string += f"&{c}#"
        return string

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self.theme.color.background)

        x = 50
        for rendered_form in self.rich_text.rendered_forms:
            surface.blit(rendered_form.surface, (x, 50))
            x += rendered_form.width

        self.label.draw(surface)

    def update(self, dt: float) -> None:
        if self.label.text != self.previous_text:
            self.parser = InlineDeveloperParser(self.label.text)
            self.rich_text = RichText(
                spans=self.parser.parse(), font_size=30
            )

        self.previous_text = self.label.text

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.unicode.isprintable():
                self.label.text += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                if len(self.label.text) > 1:
                    self.label.text = self.label.text[:-1]