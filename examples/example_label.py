import math
import random
from typing import List

import pygame
import buttonup
from base import ExampleBase


class ExampleLabel(ExampleBase):
    def __init__(self, WINDOW_WIDTH: int, WINDOW_HEIGHT: int) -> None:
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT)

        theme = buttonup.theme.load_theme("dark")

        self.label = buttonup.Label(
            x=50, y=100, text="Hello,\nWorld!", theme=theme, font_size=100
        )
        self.label.centerx = WINDOW_WIDTH / 2
        self.label.centery = WINDOW_HEIGHT / 2

        self.velocity = pygame.Vector2(1000, 300)

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

        self.fonts = [
            "consolas",
            "courier new",
            "lucida console",
        ]

        self.text_target = random.choice(self.text_targets)
        self.timer = 0.25
        self.timer_seconds = 0.25
        self.text_eat_dir = -1

        colors = (
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0)
        )
        color_rects = self.generate_color_rects()

        self.color_rect_mapping = {}

        for rect, color in zip(color_rects, colors):
            self.color_rect_mapping[color] = rect

    def generate_color_rects(self) -> List[pygame.Rect]:
        rect_width = 10

        return [
            pygame.Rect(0, 0, rect_width, self.WINDOW_HEIGHT - rect_width),
            pygame.Rect(0, self.WINDOW_HEIGHT - rect_width, self.WINDOW_WIDTH - rect_width, rect_width),
            pygame.Rect(self.WINDOW_WIDTH - rect_width, rect_width, rect_width, self.WINDOW_HEIGHT - rect_width),
            pygame.Rect(rect_width, 0, self.WINDOW_WIDTH - rect_width, rect_width)
        ]

    def change_font(self) -> None:
        self.label.font = random.choice(self.fonts)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((30, 30, 30))

        for color, rect in self.color_rect_mapping.items():
            pygame.draw.rect(surface, color, rect)

        self.label.draw(surface)

    def update(self, dt: float) -> None:
        self.label.x += self.velocity.x * dt
        self.label.y += self.velocity.y * dt

        if self.label.x + self.label.width >= self.WINDOW_WIDTH:
            self.label.x = self.WINDOW_WIDTH - self.label.width
            self.velocity.x *= -1
            self.change_font()

        if self.label.y + self.label.height >= self.WINDOW_HEIGHT:
            self.label.y = self.WINDOW_HEIGHT - self.label.height
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

        self.timer -= dt
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

        # Set label color
        for color, rect in self.color_rect_mapping.items():
            rect: pygame.Rect

            if rect.colliderect(self.label.rect):
                if color == self.label.text_color:
                    continue

                self.update_label_color(color)
                break

    def update_label_color(self, color: buttonup.types.RGB) -> None:
        self.label.text_color = color


    def handle_event(self, event: pygame.event.Event) -> None:
        pass