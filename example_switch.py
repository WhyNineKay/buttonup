raise NotImplementedError("This is a WIP example, and is not yet ready for use.")

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

        self.rail_rect = pygame.Rect(100, 100, 200, 100)
        self.switch_rect = pygame.Rect(110, 110, 80, 80)

        self.dragged = False
        self.prev_click = False
        self.rel_click_pos = (0, 0)

        self.start_drag_x = 0
        self.start_mouse_x = 0
        self.switched_on = False
        self.target_x = self.switch_rect.x

        self.theme = buttonup.theme.load_theme("dark")

        self.dt = 0.0


    def draw(self) -> None:
        self.window.fill(self.theme.color.background)

        pygame.draw.rect(self.window, (100, 100, 100), self.rail_rect, border_radius=50)
        pygame.draw.rect(self.window, (200, 200, 200), self.switch_rect, border_radius=40)

        pygame.display.flip()

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        just_pressed = mouse_pressed and not self.prev_click
        just_released = not mouse_pressed and self.prev_click

        rail_padding = 10

        switch_off_x = self.rail_rect.left + rail_padding
        switch_on_x = self.rail_rect.right - self.switch_rect.width - rail_padding

        drag_distance_required = 5

        if just_pressed:
            if self.switch_rect.collidepoint(mouse_pos):
                self.dragged = True

                self.rel_click_pos = (
                    mouse_pos[0] - self.switch_rect.x,
                    0
                )

                self.start_drag_x = self.switch_rect.x
                self.start_mouse_x = mouse_pos[0]

        if self.dragged and mouse_pressed:
            rel_x = self.rel_click_pos[0]

            new_x = mouse_pos[0] - rel_x
            new_x = max(switch_off_x, min(new_x, switch_on_x))

            self.switch_rect.x = new_x
            self.target_x = new_x

        if just_released:
            if self.dragged:
                mouse_movement = abs(mouse_pos[0] - self.start_mouse_x)

                if mouse_movement < drag_distance_required:
                    self.switched_on = not self.switched_on

                else:
                    rail_center_x = self.rail_rect.centerx
                    self.switched_on = self.switch_rect.centerx >= rail_center_x

                if self.switched_on:
                    self.target_x = switch_on_x
                else:
                    self.target_x = switch_off_x

            self.dragged = False

        self.prev_click = mouse_pressed

        if not self.dragged:
            self.switch_rect.x += (self.target_x - self.switch_rect.x) * min(1, self.dt * 10)

            if abs(self.target_x - self.switch_rect.x) < 0.5:
                self.switch_rect.x = self.target_x

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