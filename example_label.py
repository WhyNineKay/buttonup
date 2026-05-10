import math
import random

import pygame

import buttonup

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

        theme = buttonup.theme.load_theme("dark")

        self.label = buttonup.Label(
            x=50, y=100, text="Hello,\nWorld!", theme=theme, font_size=100
        )
        self.label.centerx = WINDOW_WIDTH / 2
        self.label.centery = WINDOW_HEIGHT / 2

        self.velocity = pygame.Vector2(1000, 300)

        self.dt = 0.0


        self.text_targets = [
            "Hello, World!",
            "This is a test.",
            "Who would have thought?",
            "Thank you.",
            "The forest is blue...",
            "Not the sky!",
            "Beefy computers rule",
            "48192850178273428",
            "Code is just magic!"
        ]
        for i in range(len(self.text_targets)):
            self.text_targets[i] = self.text_targets[i].replace(" ", "\n")

        self.fonts = [  # monospaced
            "consolas",
            "courier new",
            "lucida console",
        ]

        self.text_target = random.choice(self.text_targets)
        self.timer = 0.25
        self.timer_seconds = 0.25
        self.text_eat_dir = -1

    def draw(self) -> None:
        self.window.fill((30, 30, 30))
        self.label.draw(self.window)
        pygame.display.flip()

    def change_font(self) -> None:
        self.label.font = random.choice(self.fonts)

    def update(self) -> None:
        self.label.x += self.velocity.x * self.dt
        self.label.y += self.velocity.y * self.dt

        if self.label.x + self.label.width >= WINDOW_WIDTH:
            self.label.x = WINDOW_WIDTH - self.label.width
            self.velocity.x *= -1
            self.change_font()

        if self.label.y + self.label.height >= WINDOW_HEIGHT:
            self.label.y = WINDOW_HEIGHT - self.label.height
            self.velocity.y *= -1
            self.change_font()

        if self.label.x <= 0:
            self.label.x = 0
            self.velocity.x *= -1
            self.change_font()

        if self.label.y <= 0:
            self.label.y = 0
            self.velocity.y *= -1
            self.change_font()


        self.timer -= self.dt
        self.label.font_size = int(50 + 20 * (1 + math.sin(pygame.time.get_ticks() / 500)))

        if self.timer <= 0:
            self.timer = self.timer_seconds

            if len(self.label.text) > 0:
                if self.text_eat_dir == -1:
                    self.label.text = self.label.text[:-1]

                elif self.text_eat_dir == 1:
                    self.label.text += self.text_target[0]
                    self.text_target = self.text_target[1:]

                if len(self.text_target) == 0:
                    self.text_eat_dir = -1
                    self.text_target = random.choice(self.text_targets)
            else:
                self.text_eat_dir = 1
                self.label.text += self.text_target[0]
                self.text_target = self.text_target[1:]


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