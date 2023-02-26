import random

from buttonup.constants import States, Alignments
import logging
import buttonup
import pygame
import time

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

LARGE_SENTENCE = "Don't step on the broken glass. He poured rocks in the dungeon of his mind. " \
                 "The clouds formed beautiful animals in the sky that eventually created a tornado to wreak havoc." \
                 " Everyone was busy, so I went to the movie alone."


def on_hover(a):
    print("hovered", a)


class Test:
    """Class to test the pygame window."""

    def __init__(self) -> None:
        """Initialize the pygame window."""
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0.0

        self.theme = buttonup.themes.get_default_theme()

        self.button_1 = buttonup.button.DefaultButton(100, 100, width=130, height=80, text="add 0.1", border_radius=15)
        self.button_2 = buttonup.button.DefaultButton(100, 200, width=130, height=40, text="disabled", border_radius=15)

        # self.button_2.state = constants.States.DISABLED
        self.button_2.state = States.DISABLED

        self.button_3 = buttonup.button.DefaultButton(100, 300, width=150, height=150, text="3",
                                                      text_alignment_margin=15,
                                                      text_alignment_x=Alignments.LEFT,
                                                      text_alignment_y=Alignments.TOP, border_radius=30)
        self.button_4 = buttonup.button.DefaultButton(300, 100, width=40, height=130, text="4", border_radius=15)
        self.button_5 = buttonup.button.DefaultButton(400, 100, width=130, height=40, text="swap")
        self.button_6 = buttonup.button.DefaultButton(400, 150, width=130, height=40, text="cycle")
        self.button_7 = buttonup.button.DefaultButton(400, 200, width=130, height=40, text="7",
                                                      border_radius=0)

        self.label_1 = buttonup.label.DefaultLabel(100, 500, text="Hello World! This is a label.", text_size=40)

        self.elements = [self.button_1, self.button_2, self.button_3, self.button_4,
                         self.button_5, self.button_6, self.button_7, self.label_1]

    def update(self) -> None:
        for e in self.elements:
            e.update(self.dt)

        self.button_3.text = str(self.button_3.state.value.capitalize())

    def events(self) -> None:
        """Handle events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            for e in self.elements:
                e.event(event)

    def draw(self) -> None:
        """Draw the pygame window."""
        self.screen.fill(self.theme.background)
        for e in self.elements:
            if getattr(e, "draw", False):
                e.draw(self.screen)
            else:
                raise AttributeError(f"{e} has no draw method.")

        pygame.display.flip()

    def run(self) -> float:
        """Run the pygame window.
        :return: Runtime in seconds.
        """

        time_start = time.time()
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(60) / 1000

        time_end = time.time()

        return time_end - time_start


if __name__ == "__main__":
    test = Test()
    time_run = test.run()
    print(f"Ran for {round(time_run, 3)}s.")
