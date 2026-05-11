import pygame


class ExampleBase:
    def __init__(self, WINDOW_WIDTH: int, WINDOW_HEIGHT: int) -> None:
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        pass
