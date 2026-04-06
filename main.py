import pygame

import buttonup
from buttonup.richtext import TextSpan, RichText, TextStyle, InlineDeveloperParser

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
WINDOW_FPS = 60

pygame.font.init()


class MainWindow:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.theme = buttonup.theme.load_theme("dark")

        self.dt = 0.0

        self.parser = InlineDeveloperParser()

        self.rich_text = RichText(
            spans=self.parser.parse("&!Hello&l&r world"), font_size=30
        )

        self.rich_text.render()

    def draw(self) -> None:
        self.window.fill(self.theme.color.background)

        x = 50
        for rendered_form in self.rich_text.render():
            self.window.blit(rendered_form.surface, (x, 100))
            x += rendered_form.width

        pygame.display.flip()

    def update(self) -> None:
        pass

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