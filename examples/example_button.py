import pygame

from .base import ExampleBase
from buttonup.utils import CallbackPackage, Alignment
import buttonup

class ButtonExample(ExampleBase):
    def __init__(self, WINDOW_WIDTH: int, WINDOW_HEIGHT: int) -> None:
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.theme = buttonup.theme.load_theme("dark")

        self.button = buttonup.TextButton(
            x=50, y=100, theme=self.theme,
            on_click=CallbackPackage(callback=print, args=("Button clicked!",), kwargs={}),
            border_radius=15, border_width=3, text="HELLO"
        )

        self.image_button = buttonup.ImageButton(
            x=300, y=50, theme=self.theme,
            on_click=CallbackPackage(callback=print, args=("Image button clicked!",), kwargs={}),
            border_radius=10, border_width=3, width=200, height=200, padding=20, image_size_dominant=False
        )

        sprite_sheet = {
            buttonup.InteractionState.INACTIVE: pygame.image.load("example_assets/main_menu_base.png").convert_alpha(),
            buttonup.InteractionState.HOVERED: pygame.image.load(
                "example_assets/main_menu_hovered.png").convert_alpha(),
            buttonup.InteractionState.PRESSED: pygame.image.load(
                "example_assets/main_menu_clicked.png").convert_alpha(),
            buttonup.InteractionState.DISABLED: pygame.image.load(
                "example_assets/main_menu_disabled.png").convert_alpha(),
        }

        self.sprite_button = buttonup.SpriteButton(
            x=600, y=50, on_click=CallbackPackage(callback=print, args=("Sprite button clicked!",), kwargs={}),
            sprite_sheet=sprite_sheet, width=500, height=500, preserve_aspect_ratio=True
        )

        self.button_2 = buttonup.TextButton(
            x=50, y=350, theme=self.theme, text="Disabled Button", on_click=self.disable_button_2
        )

        self.timer = 0.0

    def disable_button_2(self) -> None:
        print("Button should be disabled!")
        self.button_2.disable()

    def draw(self, surface: pygame.Surface) -> None:
        self.button.draw(surface)
        self.button_2.draw(surface)
        self.image_button.draw(surface)
        self.sprite_button.draw(surface)

    def update(self, dt: float) -> None:
        self.button.update(dt)
        self.button_2.update(dt)
        self.image_button.update(dt)
        self.sprite_button.update(dt)

        self.timer += dt

        if 0.5 >= self.timer >= 0.0:
            pass
        if 1.0 >= self.timer >= 0.5:
            self.button.centerx = self.WINDOW_WIDTH / 2
        if 1.5 >= self.timer >= 1.0:
            self.button.centery = self.WINDOW_HEIGHT / 2
        if 2.0 >= self.timer >= 1.5:
            self.button.text = "Centered."
        if 2.5 >= self.timer >= 2.0:
            self.button.width = 300
        if 3.0 >= self.timer >= 2.5:
            self.button.height = 300
        if 3.5 >= self.timer >= 3.0:
            self.button.center = (self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2)
        if 4.0 >= self.timer >= 3.5:
            self.button.text = "Top Left"
            self.button.text_alignment = Alignment.TOP_LEFT
        if 4.5 >= self.timer >= 4.0:
            self.button.text = "Top Center"
            self.button.text_alignment = Alignment.TOP_CENTER
        if 5.0 >= self.timer >= 4.5:
            self.button.text = "Top Right"
            self.button.text_alignment = Alignment.TOP_RIGHT
        if 5.5 >= self.timer >= 5.0:
            self.button.text = "Center Right"
            self.button.text_alignment = Alignment.CENTER_RIGHT
        if 6.0 >= self.timer >= 5.5:
            self.button.text = "Bottom Right"
            self.button.text_alignment = Alignment.BOTTOM_RIGHT
        if 6.5 >= self.timer >= 6.0:
            self.button.text = "Bottom Center"
            self.button.text_alignment = Alignment.BOTTOM_CENTER
        if 7.0 >= self.timer >= 6.5:
            self.button.text = "Bottom Left"
            self.button.text_alignment = Alignment.BOTTOM_LEFT
        if 7.5 >= self.timer >= 7.0:
            self.button.text = "Center Left"
            self.button.text_alignment = Alignment.CENTER_LEFT
        if 8.0 >= self.timer >= 7.5:
            self.button.text = "Center"
            self.button.text_alignment = Alignment.CENTER
        if 8.5 >= self.timer >= 8.0:
            self.button.text = "BIG!"
            self.button.font_size = buttonup.constants.DEFAULT_FONT_SIZE * 4
        if 9.0 >= self.timer >= 8.5:
            self.button.text = "disabled :("
            self.button.font_size = buttonup.constants.DEFAULT_FONT_SIZE
            self.button.text_alignment = Alignment.CENTER
            self.button.disable()

        # self.image_button.width = 300 + 150 * math.cos(self.timer * 2)
        # self.image_button.height = 300 + 150 * math.sin(self.timer * 2)

        # self.button.border_radius = 15 + 15 * math.sin(self.timer * 2)
        # self.button.text_padding = 15 + 15 * math.sin(self.timer * 3)

