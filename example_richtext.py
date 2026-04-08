import pygame

import buttonup
from buttonup.richtext import TextSpan, RichText, TextStyle, InlineDeveloperParser

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

        self.dt = 0.0

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

    def draw(self) -> None:
        self.window.fill(self.theme.color.background)

        x = 50
        for rendered_form in self.rich_text.rendered_forms:
            self.window.blit(rendered_form.surface, (x, 50))
            x += rendered_form.width

        self.label.draw(self.window)

        pygame.display.flip()

    def update(self) -> None:
        if self.label.text != self.previous_text:
            self.parser = InlineDeveloperParser(
                self.label.text
            )

            self.rich_text = RichText(
                spans=self.parser.parse(), font_size=30
            )

        self.previous_text = self.label.text

    def events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.unicode.isprintable():
                    self.label.text += event.unicode

                elif event.key == pygame.K_BACKSPACE:
                    # Backspace: delete the last character
                    if len(self.label.text) > 1:
                        self.label.text = self.label.text[:-1]

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
