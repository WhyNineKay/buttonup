from typing import SupportsInt, Union, Tuple, Dict, List

import pygame

from .element import ResizableElement, InteractiveElement, ThemedElement, BorderedElement
from .label import Label
from .. import constants
from ..buttonup_types import Callback, RGB, FontLike, ColorLike
from ..theme import ThemeLike, load_default_theme
from ..utils import CallbackPackage, UNINITIALIZED_COLOR, ParsingTools
from ..utils import ColorTools, draw_vertical_plane, draw_horizontal_plane, generate_debug_image, \
    apply_surface_border_radius, SystemColors
from ..utils import InteractionState, Alignment


class BaseButton(InteractiveElement, ResizableElement, ThemedElement, BorderedElement):
    """Base button class"""

    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 width: SupportsInt = None,
                 height: SupportsInt = None,
                 theme: ThemeLike = None,
                 on_click: Union[CallbackPackage, Callback] = None,
                 on_hover: Union[CallbackPackage, Callback] = None,
                 border_radius: SupportsInt = None,
                 border_width: SupportsInt = None
                 ) -> None:
        if width is None:
            width = constants.DEFAULT_BUTTON_WIDTH

        if height is None:
            height = constants.DEFAULT_BUTTON_HEIGHT

        if border_radius is None:
            border_radius = constants.DEFAULT_BUTTON_BORDER_RADIUS

        if border_width is None:
            border_width = constants.DEFAULT_BUTTON_BORDER_WIDTH

        BorderedElement.__init__(self, border_radius=border_radius, border_width=border_width)

        InteractiveElement.__init__(self, x=x, y=y, width=width, height=height, on_click=on_click, on_hover=on_hover)

        if theme is None:
            theme = load_default_theme()

        ThemedElement.__init__(self, theme=theme)

        self._button_theme = self._theme.button_theme

    def _update_colors(self) -> None:
        self._button_theme = self._theme.button_theme

    def update(self, dt: float) -> None:
        InteractiveElement.update(self, dt)

    def draw(self, surface: pygame.Surface) -> None:
        if self._state == InteractionState.INACTIVE:
            base_color = self._button_theme.base_color
            border_color = self._button_theme.border_color
        elif self._state == InteractionState.HOVERED:
            base_color = self._button_theme.base_color_hovered
            border_color = self._button_theme.border_color_hovered
        elif self._state == InteractionState.PRESSED:
            base_color = self._button_theme.base_color_pressed
            border_color = self._button_theme.border_color_pressed
        elif self._state == InteractionState.DISABLED:
            base_color = self._button_theme.base_color_disabled
            border_color = self._button_theme.border_color_disabled
        else:
            base_color = self._button_theme.base_color
            border_color = self._button_theme.border_color

        # Draw base
        pygame.draw.rect(surface, base_color, self.rect, border_radius=self._border_radius)

        # Draw border
        pygame.draw.rect(surface, border_color, self.rect, width=self._border_width,
                         border_radius=self._border_radius)

    def debug_draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (255, 0, 0), self.rect, width=1)

    @property
    def on_click(self) -> CallbackPackage:
        return self._on_click_callback_package

    @on_click.setter
    def on_click(self, value: Union[CallbackPackage, Callback, None]) -> None:
        self._on_click_callback_package = self._parse_named_callback(value, "on_click")

    @property
    def on_hover(self) -> CallbackPackage:
        return self._on_hover_callback_package

    @on_hover.setter
    def on_hover(self, value: Union[CallbackPackage, Callback, None]) -> None:
        self._on_hover_callback_package = self._parse_named_callback(value, "on_hover")

    @property
    def base_color(self) -> RGB:
        return self._button_theme.base_color

    @base_color.setter
    def base_color(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._button_theme.base_color = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"color value must be a color (RGB, hex, or pygame.Color), not '{type(value).__name__}'.")

    @property
    def base_color_pressed(self) -> RGB:
        return self._button_theme.base_color_pressed

    @base_color_pressed.setter
    def base_color_pressed(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._button_theme.base_color_pressed = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"color value must be a color (RGB, hex, or pygame.Color), not '{type(value).__name__}'.")

    @property
    def base_color_hovered(self) -> RGB:
        return self._button_theme.base_color_hovered

    @base_color_hovered.setter
    def base_color_hovered(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._button_theme.base_color_hovered = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"color value must be a color (RGB, hex, or pygame.Color), not '{type(value).__name__}'.")

    @property
    def base_color_disabled(self) -> RGB:
        return self._button_theme.base_color_disabled

    @base_color_disabled.setter
    def base_color_disabled(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._button_theme.base_color_disabled = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"color value must be a color (RGB, hex, or pygame.Color), not '{type(value).__name__}'.")

    @property
    def border_color(self) -> RGB:
        return self._button_theme.border_color

    @border_color.setter
    def border_color(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._button_theme.border_color = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"color value must be a color (RGB, hex, or pygame.Color), not '{type(value).__name__}'.")

    @property
    def border_color_pressed(self) -> RGB:
        return self._button_theme.border_color_pressed

    @border_color_pressed.setter
    def border_color_pressed(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._button_theme.border_color_pressed = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"color value must be a color (RGB, hex, or pygame.Color), not '{type(value).__name__}'.")

    @property
    def border_color_hovered(self) -> RGB:
        return self._button_theme.border_color_hovered

    @border_color_hovered.setter
    def border_color_hovered(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._button_theme.border_color_hovered = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"color value must be a color (RGB, hex, or pygame.Color), not '{type(value).__name__}'.")

    @property
    def border_color_disabled(self) -> RGB:
        return self._button_theme.border_color_disabled

    @border_color_disabled.setter
    def border_color_disabled(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._button_theme.border_color_disabled = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"color value must be a color (RGB, hex, or pygame.Color), not '{type(value).__name__}'.")


class TextButton(BaseButton):
    """Base button class with text"""

    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 width: SupportsInt = None,
                 height: SupportsInt = None,
                 theme: ThemeLike = None,
                 text: str = None,
                 font: FontLike = None,
                 font_size: SupportsInt = None,
                 on_click: Union[CallbackPackage, Callback] = None,
                 on_hover: Union[CallbackPackage, Callback] = None,
                 text_alignment: Alignment = None,
                 text_padding: SupportsInt = None,
                 border_radius: SupportsInt = None,
                 border_width: SupportsInt = None
                 ) -> None:

        BaseButton.__init__(self, x=x, y=y, width=width, height=height, theme=theme, on_click=on_click,
                            on_hover=on_hover, border_radius=border_radius, border_width=border_width)

        if text is None:
            text = constants.DEFAULT_BUTTON_TEXT

        if font_size is None:
            font_size = constants.DEFAULT_FONT_SIZE

        if font is None:
            font = constants.DEFAULT_FONT_NAME

        if text_padding is None:
            text_padding = constants.DEFAULT_BUTTON_TEXT_PADDING

        self._text_padding = self._parse_text_padding(text_padding)

        self._button_label = Label(
            x=0,
            y=0,
            text=text,
            theme=theme,
            font=font,
            font_size=font_size
        )

        if text_alignment is None:
            text_alignment = Alignment.CENTER

        self._text_alignment = self._parse_text_alignment(text_alignment)

        self._button_label.text_color = self._button_theme.text_color

        self._update_position(self._x, self._y)

    def _parse_text_padding(self, text_padding: SupportsInt) -> int:
        return ParsingTools.parse_non_negative_int(text_padding, "text_padding")

    def _parse_text_alignment(self, text_alignment: Alignment) -> Alignment:
        if not isinstance(text_alignment, Alignment):
            raise TypeError(f"Text alignment must be of type 'Alignment', not '{type(text_alignment)}'.")
        return text_alignment

    def _update_colors(self) -> None:
        super()._update_colors()
        self._button_label.text_color = self._button_theme.text_color

    def _align_label_center(self) -> None:
        self._button_label.center = self.center

    def _align_label_top_left(self) -> None:
        self._button_label.x = self.x + self._text_padding
        self._button_label.y = self.y + self._text_padding

    def _align_label_top_right(self) -> None:
        self._button_label.x = self.x + self.width - self._text_padding - self._button_label.width
        self._button_label.y = self.y + self._text_padding

    def _align_label_bottom_left(self) -> None:
        self._button_label.x = self.x + self._text_padding
        self._button_label.y = self.y + self.height - self._text_padding - self._button_label.height

    def _align_label_bottom_right(self) -> None:
        self._button_label.x = self.x + self.width - self._text_padding - self._button_label.width
        self._button_label.y = self.y + self.height - self._text_padding - self._button_label.height

    def _align_label_center_left(self) -> None:
        self._button_label.x = self.x + self._text_padding
        self._button_label.centery = self.centery

    def _align_label_center_right(self) -> None:
        self._button_label.x = self.x + self.width - self._text_padding - self._button_label.width
        self._button_label.centery = self.centery

    def _align_label_top_center(self) -> None:
        self._button_label.centerx = self.centerx
        self._button_label.y = self.y + self._text_padding

    def _align_label_bottom_center(self) -> None:
        self._button_label.centerx = self.centerx
        self._button_label.y = self.y + self.height - self._text_padding - self._button_label.height

    def _align_label(self) -> None:
        alignment_mapping = {
            Alignment.CENTER: self._align_label_center,
            Alignment.TOP_LEFT: self._align_label_top_left,
            Alignment.TOP_RIGHT: self._align_label_top_right,
            Alignment.BOTTOM_LEFT: self._align_label_bottom_left,
            Alignment.BOTTOM_RIGHT: self._align_label_bottom_right,
            Alignment.CENTER_LEFT: self._align_label_center_left,
            Alignment.CENTER_RIGHT: self._align_label_center_right,
            Alignment.TOP_CENTER: self._align_label_top_center,
            Alignment.BOTTOM_CENTER: self._align_label_bottom_center
        }
        if self._text_alignment in alignment_mapping:
            alignment_mapping[self._text_alignment]()
        else:
            raise ValueError(f"Unsupported text alignment '{self._text_alignment}'.")

    def _update_label_position(self) -> None:
        self._align_label()

    def _update_position(self, x: SupportsInt, y: SupportsInt) -> None:
        super()._update_position(x, y)
        self._update_label_position()

    def _update_dimensions(self, width: SupportsInt, height: SupportsInt) -> None:
        super()._update_dimensions(width, height)
        self._update_label_position()

    @property
    def text(self) -> str:
        return self._button_label.text

    @text.setter
    def text(self, value: str) -> None:
        self._button_label.text = value
        self._update_label_position()

    # Font setters
    @property
    def font(self) -> pygame.font.Font:
        return self._button_label.font

    @font.setter
    def font(self, value: pygame.font.Font) -> None:
        self._button_label.font = value
        self._update_label_position()

    @property
    def font_size(self) -> int:
        return self._button_label.font_size

    @font_size.setter
    def font_size(self, value: SupportsInt) -> None:
        self._button_label.font_size = value
        self._update_label_position()

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        self._button_label.draw(surface)

    def update(self, dt: float) -> None:
        super().update(dt)

        # Update label text color based on button state
        if self._state == InteractionState.INACTIVE:
            self._button_label.text_color = self._button_theme.text_color
        elif self._state == InteractionState.HOVERED:
            self._button_label.text_color = self._button_theme.text_color_hovered
        elif self._state == InteractionState.PRESSED:
            self._button_label.text_color = self._button_theme.text_color_pressed
        elif self._state == InteractionState.DISABLED:
            self._button_label.text_color = self._button_theme.text_color_disabled

    @property
    def text_alignment(self) -> Alignment:
        return self._text_alignment

    @text_alignment.setter
    def text_alignment(self, value: Alignment) -> None:
        self._text_alignment = self._parse_text_alignment(value)
        self._update_label_position()

    @property
    def text_padding(self) -> int:
        return self._text_padding

    @text_padding.setter
    def text_padding(self, value: SupportsInt) -> None:
        self._text_padding = self._parse_text_padding(value)
        self._update_label_position()

    def debug_draw(self, surface: pygame.Surface) -> None:
        super().debug_draw(surface)
        self._button_label.debug_draw(surface)
        if not self._text_alignment == Alignment.CENTER:
            draw_vertical_plane(surface, (0, 255, 0), (self._button_label.x, self._button_label.centery),
                                length=self.height)
            draw_vertical_plane(surface, (0, 255, 0),
                                (self._button_label.x + self._button_label.width, self._button_label.centery),
                                length=self.height)

            draw_horizontal_plane(surface, (0, 255, 0), (self._button_label.centerx, self._button_label.y),
                                  length=self.width)
            draw_horizontal_plane(surface, (0, 255, 0),
                                  (self._button_label.centerx, self._button_label.y + self._button_label.height),
                                  length=self.width)

    @property
    def text_surfaces(self) -> List[pygame.Surface]:
        return self._button_label.text_surfaces

    @property
    def text_color(self) -> RGB:
        return self._button_theme.text_color

    @text_color.setter
    def text_color(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._button_theme.text_color = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"color value must be a color (RGB, hex, or pygame.Color), not '{type(value).__name__}'.")

    @property
    def text_color_pressed(self) -> RGB:
        return self._button_theme.text_color_pressed

    @text_color_pressed.setter
    def text_color_pressed(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._button_theme.text_color_pressed = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"color value must be a color (RGB, hex, or pygame.Color), not '{type(value).__name__}'.")

    @property
    def text_color_hovered(self) -> RGB:
        return self._button_theme.text_color_hovered

    @text_color_hovered.setter
    def text_color_hovered(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._button_theme.text_color_hovered = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"color value must be a color (RGB, hex, or pygame.Color), not '{type(value).__name__}'.")

    @property
    def text_color_disabled(self) -> RGB:
        return self._button_theme.text_color_disabled

    @text_color_disabled.setter
    def text_color_disabled(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._button_theme.text_color_disabled = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"color value must be a color (RGB, hex, or pygame.Color), not '{type(value).__name__}'.")


class ImageButton(BaseButton):
    """Base button class with image"""

    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 width: SupportsInt = None,
                 height: SupportsInt = None,
                 theme: ThemeLike = None,
                 image: pygame.Surface = None,
                 state_changing_images: bool = None,
                 image_size_dominant: bool = None,
                 on_click: Union[CallbackPackage, Callback] = None,
                 on_hover: Union[CallbackPackage, Callback] = None,
                 border_radius: SupportsInt = None,
                 border_width: SupportsInt = None,
                 padding: SupportsInt = None,
                 preserve_aspect_ratio: bool = None
                 ) -> None:
        if state_changing_images is None:
            state_changing_images = True

        self._state_changing_images = self._parse_state_changing_images(state_changing_images)

        if image_size_dominant is None:
            # If true, the image size will determine the button size. If false, the button size will determine the
            # image size.
            image_size_dominant = False

        self._image_size_dominant = self._parse_image_size_dominant(image_size_dominant)

        if padding is None:
            padding = constants.DEFAULT_BUTTON_IMAGE_PADDING

        self._padding = self._parse_padding(padding)

        if preserve_aspect_ratio is None:
            preserve_aspect_ratio = True

        self._preserve_aspect_ratio = self._parse_preserve_aspect_ratio(preserve_aspect_ratio)

        if image is None:
            image = generate_debug_image((constants.DEFAULT_BUTTON_WIDTH, constants.DEFAULT_BUTTON_WIDTH),
                                         colors=(SystemColors.PINK, SystemColors.PURPLE))

        self._original_image = self._parse_image(image)

        self._image = self._original_image
        self._hovered_image = self._original_image
        self._pressed_image = self._original_image
        self._disabled_image = self._original_image

        BaseButton.__init__(self, x=x, y=y, width=width, height=height, theme=theme, on_click=on_click,
                            on_hover=on_hover, border_radius=border_radius, border_width=border_width)

    def _parse_padding(self, padding: SupportsInt) -> int:
        return ParsingTools.parse_non_negative_int(padding, "padding")

    def _parse_preserve_aspect_ratio(self, preserve_aspect_ratio: bool) -> bool:
        return ParsingTools.parse_bool_strict(preserve_aspect_ratio, "preserve_aspect_ratio")

    def _parse_image_size_dominant(self, image_size_dominant: bool) -> bool:
        return ParsingTools.parse_bool_strict(image_size_dominant, "image_size_dominant")

    def _parse_state_changing_images(self, state_changing_images: bool) -> bool:
        return ParsingTools.parse_bool_strict(state_changing_images, "state_changing_images")

    def _generate_hovered_image(self) -> pygame.Surface:
        hovered_image = self._image.copy()
        hovered_image.fill((10, 10, 10), special_flags=pygame.BLEND_RGBA_ADD)
        return hovered_image

    def _generate_pressed_image(self) -> pygame.Surface:
        pressed_image = self._image.copy()
        pressed_image.fill((220, 220, 220), special_flags=pygame.BLEND_RGBA_MULT)
        return pressed_image

    def _generate_disabled_image(self) -> pygame.Surface:
        disabled_image = self._image.copy()
        disabled_image.fill((100, 100, 100), special_flags=pygame.BLEND_RGBA_MULT)
        return disabled_image

    def _parse_image(self, image: pygame.Surface) -> pygame.Surface:
        if not isinstance(image, pygame.Surface):
            raise TypeError(f"Image must be of type 'pygame.Surface', not '{type(image)}'.")

        return image

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        image_rect = self._image.get_rect()
        image_rect.center = self.center

        if not self._state_changing_images:
            surface.blit(self._image, image_rect)
            return

        if self._state == InteractionState.INACTIVE:
            surface.blit(self._image, image_rect)
        elif self._state == InteractionState.HOVERED:
            surface.blit(self._hovered_image, image_rect)
        elif self._state == InteractionState.PRESSED:
            surface.blit(self._pressed_image, image_rect)
        elif self._state == InteractionState.DISABLED:
            surface.blit(self._disabled_image, image_rect)

    def _update_border_radius(self, border_radius: int) -> None:
        super()._update_border_radius(border_radius)

        self._update_images_border_radius()

    def _update_state_images(self) -> None:
        if self._state_changing_images:
            self._hovered_image = self._generate_hovered_image()
            self._pressed_image = self._generate_pressed_image()
            self._disabled_image = self._generate_disabled_image()

    def _update_dimensions(self, width: SupportsInt, height: SupportsInt) -> None:
        if self._image_size_dominant:
            # If the image size is dominant, we update the button size to fit the image with padding.
            image_width = self._original_image.get_width()
            image_height = self._original_image.get_height()
            width = image_width + self._padding * 2
            height = image_height + self._padding * 2

        super()._update_dimensions(width, height)

        if not self._image_size_dominant:
            # If the button size is dominant, we update the image size to fit the button with padding.
            image_width = self._width - self._padding * 2
            image_height = self._height - self._padding * 2

            if self._preserve_aspect_ratio:
                original_aspect_ratio = self._original_image.get_width() / self._original_image.get_height()
                target_aspect_ratio = image_width / image_height

                if target_aspect_ratio > original_aspect_ratio:
                    # Target is wider than original, fit to height
                    image_width = int(image_height * original_aspect_ratio)
                else:
                    # Target is taller than original, fit to width
                    image_height = int(image_width / original_aspect_ratio)

            self._image = pygame.transform.scale(self._original_image, (image_width, image_height))

            self._update_state_images()
            self._update_images_border_radius()

    def _get_adjusted_border_radius(self) -> int:
        # Adjust border radius to fit the image size if necessary
        return max(self._border_radius - self._padding, 0)

    def _update_images_border_radius(self) -> None:
        adjusted_border_radius = self._get_adjusted_border_radius()
        self._image = apply_surface_border_radius(self._image, adjusted_border_radius)
        self._hovered_image = apply_surface_border_radius(self._hovered_image, adjusted_border_radius)
        self._pressed_image = apply_surface_border_radius(self._pressed_image, adjusted_border_radius)
        self._disabled_image = apply_surface_border_radius(self._disabled_image, adjusted_border_radius)

    @property
    def image(self) -> pygame.Surface:
        return self._original_image

    @image.setter
    def image(self, value: pygame.Surface) -> None:
        self._original_image = self._parse_image(value)
        self._update_dimensions(self._width, self._height)

    @property
    def state_changing_images(self) -> bool:
        return self._state_changing_images

    @state_changing_images.setter
    def state_changing_images(self, value: bool) -> None:
        self._state_changing_images = self._parse_state_changing_images(value)
        self._update_state_images()

    @property
    def image_size_dominant(self) -> bool:
        return self._image_size_dominant

    @image_size_dominant.setter
    def image_size_dominant(self, value: bool) -> None:
        self._image_size_dominant = self._parse_image_size_dominant(value)
        self._update_dimensions(self._width, self._height)

    @property
    def preserve_aspect_ratio(self) -> bool:
        return self._preserve_aspect_ratio

    @preserve_aspect_ratio.setter
    def preserve_aspect_ratio(self, value: bool) -> None:
        self._preserve_aspect_ratio = self._parse_preserve_aspect_ratio(value)
        self._update_dimensions(self._width, self._height)

    @property
    def padding(self) -> int:
        return self._padding

    @padding.setter
    def padding(self, value: SupportsInt) -> None:
        self._padding = self._parse_padding(value)
        self._update_dimensions(self._width, self._height)

    @property
    def image_width(self) -> int:
        return self._image.get_width()

    @property
    def image_height(self) -> int:
        return self._image.get_height()

    @property
    def image_size(self) -> Tuple[int, int]:
        return self._image.get_size()


class SpriteButton(BaseButton):
    """Base button class with sprite"""

    def __init__(self,
                 x: SupportsInt,
                 y: SupportsInt,
                 width: SupportsInt = None,
                 height: SupportsInt = None,
                 sprite_sheet: Dict[InteractionState, pygame.Surface] = None,
                 on_click: Union[CallbackPackage, Callback] = None,
                 on_hover: Union[CallbackPackage, Callback] = None,
                 preserve_aspect_ratio: bool = None
                 ) -> None:

        if sprite_sheet is None:
            sprite_sheet = {
                InteractionState.INACTIVE: generate_debug_image(
                    (constants.DEFAULT_BUTTON_WIDTH, constants.DEFAULT_BUTTON_HEIGHT),
                    colors=(SystemColors.PINK, SystemColors.PURPLE)),
                InteractionState.HOVERED: generate_debug_image(
                    (constants.DEFAULT_BUTTON_WIDTH, constants.DEFAULT_BUTTON_HEIGHT),
                    colors=(SystemColors.BLUE, SystemColors.AQUA)),
                InteractionState.PRESSED: generate_debug_image(
                    (constants.DEFAULT_BUTTON_WIDTH, constants.DEFAULT_BUTTON_HEIGHT),
                    colors=(SystemColors.GREEN, SystemColors.LIME)),
                InteractionState.DISABLED: generate_debug_image(
                    (constants.DEFAULT_BUTTON_WIDTH, constants.DEFAULT_BUTTON_HEIGHT),
                    colors=(SystemColors.RED, SystemColors.ORANGE)),
            }

        self._original_sprite_sheet = self._parse_sprite_sheet(sprite_sheet)
        sprite_sheet_inactive_image = self._original_sprite_sheet[InteractionState.INACTIVE]
        self._original_image_aspect_ratio = (
                sprite_sheet_inactive_image.get_width() / sprite_sheet_inactive_image.get_height()
        )

        self._sprite_sheet = {}
        for state in InteractionState:
            if state == InteractionState.DRAGGING:
                continue  # Dragging state is not required for sprite sheet

            self._sprite_sheet[state] = self._original_sprite_sheet[state].copy()

        if preserve_aspect_ratio is None:
            preserve_aspect_ratio = True

        self._preserve_aspect_ratio = self._parse_preserve_aspect_ratio(preserve_aspect_ratio)

        BaseButton.__init__(self, x=x, y=y, width=width, height=height, theme=None, on_click=on_click,
                            on_hover=on_hover, border_radius=0, border_width=0)

    def _parse_preserve_aspect_ratio(self, preserve_aspect_ratio: bool) -> bool:
        return ParsingTools.parse_bool_strict(preserve_aspect_ratio, "preserve_aspect_ratio")

    def _resize_sprite_sheet(self) -> None:
        if self._preserve_aspect_ratio:
            target_aspect_ratio = self._width / self._height

            if target_aspect_ratio > self._original_image_aspect_ratio:
                # Target is wider than original, fit to height
                new_width = int(self._height * self._original_image_aspect_ratio)
                new_height = self._height
            else:
                # Target is taller than original, fit to width
                new_width = self._width
                new_height = int(self._width / self._original_image_aspect_ratio)

            if new_width != self._width or new_height != self._height:
                self._update_dimensions(new_width, new_height)  # Recursively reach equilibrium size
                return

        for state in InteractionState:
            self._sprite_sheet[state] = pygame.transform.scale(self._original_sprite_sheet[state],
                                                               (self._width, self._height))

    def _parse_sprite_sheet(
            self,
            sprite_sheet: Dict[InteractionState, pygame.Surface]
    ) -> Dict[InteractionState, pygame.Surface]:
        if not isinstance(sprite_sheet, dict):
            raise TypeError(f"Sprite sheet must be of type 'dict', not '{type(sprite_sheet)}'.")

        size = None

        for state in InteractionState:
            if state == InteractionState.DRAGGING:
                continue  # Dragging state is not required for sprite sheet

            if state not in sprite_sheet:
                raise ValueError(f"Sprite sheet is missing image for state '{state}'.")

            if not isinstance(sprite_sheet[state], pygame.Surface):
                raise TypeError(
                    f"Sprite sheet image for state '{state}' must be of type 'pygame.Surface', not "
                    f"'{type(sprite_sheet[state])}'."
                )

            if size is None:
                size = sprite_sheet[state].get_size()
            elif sprite_sheet[state].get_size() != size:
                raise ValueError(
                    f"All images in the sprite sheet must be the same size. Expected size {size}, but got "
                    f"{sprite_sheet[state].get_size()} for state '{state}'."
                )

        return sprite_sheet

    def draw(self, surface: pygame.Surface) -> None:
        image = self._sprite_sheet[self._state]
        image_rect = image.get_rect()
        image_rect.center = self.center
        surface.blit(image, image_rect)

    def _update_dimensions(self, width: SupportsInt, height: SupportsInt) -> None:
        super()._update_dimensions(width, height)
        self._resize_sprite_sheet()
