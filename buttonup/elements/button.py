from typing import SupportsInt, Union, Optional, Tuple, Dict

import pygame

from .. import constants
from ..utils import ColorTools, draw_vertical_plane, draw_horizontal_plane, generate_debug_image, \
    apply_surface_border_radius, Colors
from .label import Label
from ..utils import InteractionState, Alignment
from ..buttonup_types import Callback, RGB, FontLike, ColorLike
from ..theme import ThemeLike, load_default_theme
from ..utils import CallbackPackage, TEMP_COLOR
from .element import Element, ResizableElement, InteractiveElement, ThemedElement, FontElement


class BaseButton(InteractiveElement, ResizableElement, ThemedElement):
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

        self._border_radius = self._parse_border_radius(border_radius)

        if border_width is None:
            border_width = constants.DEFAULT_BUTTON_BORDER_WIDTH

        self._border_width = self._parse_border_width(border_width)

        InteractiveElement.__init__(self, x=x, y=y, width=width, height=height, on_click=on_click, on_hover=on_hover)

        self._base_color: RGB = TEMP_COLOR
        self._base_color_pressed: RGB = TEMP_COLOR
        self._base_color_hovered: RGB = TEMP_COLOR
        self._base_color_disabled: RGB = TEMP_COLOR
        self._border_color: RGB = TEMP_COLOR
        self._border_color_pressed: RGB = TEMP_COLOR
        self._border_color_hovered: RGB = TEMP_COLOR
        self._border_color_disabled: RGB = TEMP_COLOR
        self._text_color: RGB = TEMP_COLOR
        self._text_color_pressed: RGB = TEMP_COLOR
        self._text_color_hovered: RGB = TEMP_COLOR
        self._text_color_disabled: RGB = TEMP_COLOR

        if theme is None:
            theme = load_default_theme()

        ThemedElement.__init__(self, theme=theme)

    def disable(self) -> None:
        self._state = InteractionState.DISABLED

    def enable(self) -> None:
        self._state = InteractionState.INACTIVE

    def _update_colors(self) -> None:
        self._base_color = self.theme.button_theme.base_color
        self._base_color_pressed = self.theme.button_theme.base_color_pressed
        self._base_color_hovered = self.theme.button_theme.base_color_hovered
        self._base_color_disabled = self.theme.button_theme.base_color_disabled
        self._border_color = self.theme.button_theme.border_color
        self._border_color_pressed = self.theme.button_theme.border_color_pressed
        self._border_color_hovered = self.theme.button_theme.border_color_hovered
        self._border_color_disabled = self.theme.button_theme.border_color_disabled

    def _parse_border_radius(self, border_radius: SupportsInt) -> int:
        if not hasattr(border_radius, "__int__"):
            raise TypeError(
                f"Border radius must be of type 'int' or support __int__ conversion, not '{type(border_radius)}'.")

        border_radius = int(border_radius)

        if border_radius < 0:
            raise ValueError(f"Border radius must be non-negative, not '{border_radius}'.")

        return border_radius

    def _parse_border_width(self, border_width: SupportsInt) -> int:
        if not hasattr(border_width, "__int__"):
            raise TypeError(
                f"Border width must be of type 'int' or support __int__ conversion, not '{type(border_width)}'.")

        border_width = int(border_width)

        if border_width < 0:
            raise ValueError(f"Border width must be non-negative, not '{border_width}'.")

        return border_width

    def update(self, dt: float) -> None:
        InteractiveElement.update(self, dt)

        if self._state == InteractionState.INACTIVE:
            self._base_color = self.theme.button_theme.base_color
            self._border_color = self.theme.button_theme.border_color
        elif self._state == InteractionState.HOVERED:
            self._base_color = self.theme.button_theme.base_color_hovered
            self._border_color = self.theme.button_theme.border_color_hovered
        elif self._state == InteractionState.CLICKED:
            self._base_color = self.theme.button_theme.base_color_pressed
            self._border_color = self.theme.button_theme.border_color_pressed
        elif self._state == InteractionState.DISABLED:
            self._base_color = self.theme.button_theme.base_color_disabled
            self._border_color = self.theme.button_theme.border_color_disabled

    def draw(self, surface: pygame.Surface) -> None:
        # Draw base
        pygame.draw.rect(surface, self._base_color, self.rect, border_radius=self._border_radius)

        # Draw border
        pygame.draw.rect(surface, self._border_color, self.rect, width=self._border_width,
                         border_radius=self._border_radius)

    def _update_border_radius(self, border_radius: int) -> None:
        self._border_radius = border_radius

    @property
    def base_color(self) -> RGB:
        return self._base_color

    @base_color.setter
    def base_color(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._base_color = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"Color 'base_color' must be a valid color, not '{value}'.")

    @property
    def base_color_pressed(self) -> RGB:
        return self._base_color_pressed

    @base_color_pressed.setter
    def base_color_pressed(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._base_color_pressed = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"Color 'base_color_pressed' must be a valid color, not '{value}'.")

    @property
    def base_color_hovered(self) -> RGB:
        return self._base_color_hovered

    @base_color_hovered.setter
    def base_color_hovered(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._base_color_hovered = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"Color 'base_color_hovered' must be a valid color, not '{value}'.")

    @property
    def base_color_disabled(self) -> RGB:
        return self._base_color_disabled

    @base_color_disabled.setter
    def base_color_disabled(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._base_color_disabled = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"Color 'base_color_disabled' must be a valid color, not '{value}'.")

    @property
    def border_color(self) -> RGB:
        return self._border_color

    @border_color.setter
    def border_color(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._border_color = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"Color 'border_color' must be a valid color, not '{value}'.")

    @property
    def border_color_pressed(self) -> RGB:
        return self._border_color_pressed

    @border_color_pressed.setter
    def border_color_pressed(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._border_color_pressed = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"Color 'border_color_pressed' must be a valid color, not '{value}'.")

    @property
    def border_color_hovered(self) -> RGB:
        return self._border_color_hovered

    @border_color_hovered.setter
    def border_color_hovered(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._border_color_hovered = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"Color 'border_color_hovered' must be a valid color, not '{value}'.")

    @property
    def border_color_disabled(self) -> RGB:
        return self._border_color_disabled

    @border_color_disabled.setter
    def border_color_disabled(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._border_color_disabled = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"Color 'border_color_disabled' must be a valid color, not '{value}'.")

    @property
    def border_radius(self) -> int:
        return self._border_radius

    @border_radius.setter
    def border_radius(self, value: SupportsInt) -> None:
        border_radius = self._parse_border_radius(value)
        self._update_border_radius(border_radius)

    @property
    def border_width(self) -> int:
        return self._border_width

    @border_width.setter
    def border_width(self, value: SupportsInt) -> None:
        self._border_width = self._parse_border_width(value)

    def debug_draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (255, 0, 0), self.rect, width=1)


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
        self._text_color: RGB = TEMP_COLOR
        self._text_color_pressed: RGB = TEMP_COLOR
        self._text_color_hovered: RGB = TEMP_COLOR
        self._text_color_disabled: RGB = TEMP_COLOR

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

        BaseButton.__init__(self, x=x, y=y, width=width, height=height, theme=theme, on_click=on_click,
                            on_hover=on_hover, border_radius=border_radius, border_width=border_width)

    def _parse_text_padding(self, text_padding: SupportsInt) -> int:
        if not hasattr(text_padding, "__int__"):
            raise TypeError(
                f"Text padding must be of type 'int' or support __int__ conversion, not '{type(text_padding)}'.")

        text_padding = int(text_padding)

        if text_padding < 0:
            raise ValueError(f"Text padding must be non-negative, not '{text_padding}'.")

        return text_padding

    def _parse_text_alignment(self, text_alignment: Alignment) -> Alignment:
        if not isinstance(text_alignment, Alignment):
            raise TypeError(f"Text alignment must be of type 'Alignment', not '{type(text_alignment)}'.")
        return text_alignment

    def _update_colors(self) -> None:
        super()._update_colors()
        self._text_color = self.theme.button_theme.text_color
        self._text_color_pressed = self.theme.button_theme.text_color_pressed
        self._text_color_hovered = self.theme.button_theme.text_color_hovered
        self._text_color_disabled = self.theme.button_theme.text_color_disabled

        self._button_label.text_color = self._text_color

    def _update_label_position(self) -> None:
        if self._text_alignment == Alignment.CENTER:
            self._button_label.center = self.center
        elif self._text_alignment == Alignment.TOP_LEFT:
            self._button_label.x = self.x + self._text_padding
            self._button_label.y = self.y + self._text_padding
        elif self._text_alignment == Alignment.TOP_RIGHT:
            self._button_label.x = self.x + self.width - self._text_padding - self._button_label.width
            self._button_label.y = self.y + self._text_padding
        elif self._text_alignment == Alignment.BOTTOM_LEFT:
            self._button_label.x = self.x + self._text_padding
            self._button_label.y = self.y + self.height - self._text_padding - self._button_label.height
        elif self._text_alignment == Alignment.BOTTOM_RIGHT:
            self._button_label.x = self.x + self.width - self._text_padding - self._button_label.width
            self._button_label.y = self.y + self.height - self._text_padding - self._button_label.height
        elif self._text_alignment == Alignment.CENTER_LEFT:
            self._button_label.x = self.x + self._text_padding
            self._button_label.centery = self.centery
        elif self._text_alignment == Alignment.CENTER_RIGHT:
            self._button_label.x = self.x + self.width - self._text_padding - self._button_label.width
            self._button_label.centery = self.centery
        elif self._text_alignment == Alignment.TOP_CENTER:
            self._button_label.centerx = self.centerx
            self._button_label.y = self.y + self._text_padding
        elif self._text_alignment == Alignment.BOTTOM_CENTER:
            self._button_label.centerx = self.centerx
            self._button_label.y = self.y + self.height - self._text_padding - self._button_label.height
        else:
            raise ValueError(f"Unsupported text alignment '{self._text_alignment}'.")

    def _update_position(self, x: SupportsInt, y: SupportsInt) -> None:
        super()._update_position(x, y)
        self._update_label_position()

    def _update_size(self, width: SupportsInt, height: SupportsInt) -> None:
        super()._update_size(width, height)
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
            self._button_label.text_color = self._text_color
        elif self._state == InteractionState.HOVERED:
            self._button_label.text_color = self._text_color_hovered
        elif self._state == InteractionState.CLICKED:
            self._button_label.text_color = self._text_color_pressed
        elif self._state == InteractionState.DISABLED:
            self._button_label.text_color = self._text_color_disabled

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

    @property
    def text_color(self) -> RGB:
        return self._text_color

    @text_color.setter
    def text_color(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._text_color = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"Color 'text_color' must be a valid color, not '{value}'.")

    @property
    def text_color_pressed(self) -> RGB:
        return self._text_color_pressed

    @text_color_pressed.setter
    def text_color_pressed(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._text_color_pressed = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"Color 'text_color_pressed' must be a valid color, not '{value}'.")

    @property
    def text_color_hovered(self) -> RGB:
        return self._text_color_hovered

    @text_color_hovered.setter
    def text_color_hovered(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._text_color_hovered = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"Color 'text_color_hovered' must be a valid color, not '{value}'.")

    @property
    def text_color_disabled(self) -> RGB:
        return self._text_color_disabled

    @text_color_disabled.setter
    def text_color_disabled(self, value: ColorLike) -> None:
        if ColorTools.is_color(value):
            self._text_color_disabled = ColorTools.to_rgb(value)
        else:
            raise ValueError(f"Color 'text_color_disabled' must be a valid color, not '{value}'.")

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
            image = generate_debug_image((constants.DEFAULT_BUTTON_WIDTH, constants.DEFAULT_BUTTON_WIDTH), colors=(Colors.PINK, Colors.PURPLE))

        self._original_image = self._parse_image(image)

        self._image = self._original_image
        self._hovered_image = self._original_image
        self._pressed_image = self._original_image
        self._disabled_image = self._original_image

        BaseButton.__init__(self, x=x, y=y, width=width, height=height, theme=theme, on_click=on_click,
                            on_hover=on_hover, border_radius=border_radius, border_width=border_width)

    def _parse_padding(self, padding: SupportsInt) -> int:
        if not hasattr(padding, "__int__"):
            raise TypeError(f"Padding must be of type 'int' or support __int__ conversion, not '{type(padding)}'.")

        padding = int(padding)

        if padding < 0:
            raise ValueError(f"Padding must be non-negative, not '{padding}'.")

        return padding

    def _parse_preserve_aspect_ratio(self, preserve_aspect_ratio: bool) -> bool:
        if not isinstance(preserve_aspect_ratio, bool):
            raise TypeError(f"Preserve aspect ratio flag must be of type 'bool', not '{type(preserve_aspect_ratio)}'.")
        return preserve_aspect_ratio

    def _parse_image_size_dominant(self, image_size_dominant: bool) -> bool:
        if not isinstance(image_size_dominant, bool):
            raise TypeError(f"Image size dominant flag must be of type 'bool', not '{type(image_size_dominant)}'.")
        return image_size_dominant

    def _parse_state_changing_images(self, state_changing_images: bool) -> bool:
        if not isinstance(state_changing_images, bool):
            raise TypeError(f"State changing images flag must be of type 'bool', not '{type(state_changing_images)}'.")
        return state_changing_images

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
        elif self._state == InteractionState.CLICKED:
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

    def _update_size(self, width: SupportsInt, height: SupportsInt) -> None:
        if self._image_size_dominant:
            # If the image size is dominant, we update the button size to fit the image with padding.
            image_width = self._original_image.get_width()
            image_height = self._original_image.get_height()
            width = image_width + self._padding * 2
            height = image_height + self._padding * 2

        super()._update_size(width, height)

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
        self._update_size(self._width, self._height)

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
        self._update_size(self._width, self._height)

    @property
    def preserve_aspect_ratio(self) -> bool:
        return self._preserve_aspect_ratio

    @preserve_aspect_ratio.setter
    def preserve_aspect_ratio(self, value: bool) -> None:
        self._preserve_aspect_ratio = self._parse_preserve_aspect_ratio(value)
        self._update_size(self._width, self._height)

    @property
    def padding(self) -> int:
        return self._padding

    @padding.setter
    def padding(self, value: SupportsInt) -> None:
        self._padding = self._parse_padding(value)
        self._update_size(self._width, self._height)

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
                InteractionState.INACTIVE: generate_debug_image((constants.DEFAULT_BUTTON_WIDTH, constants.DEFAULT_BUTTON_HEIGHT), colors=(Colors.PINK, Colors.PURPLE)),
                InteractionState.HOVERED: generate_debug_image((constants.DEFAULT_BUTTON_WIDTH, constants.DEFAULT_BUTTON_HEIGHT), colors=(Colors.BLUE, Colors.AQUA)),
                InteractionState.CLICKED: generate_debug_image((constants.DEFAULT_BUTTON_WIDTH, constants.DEFAULT_BUTTON_HEIGHT), colors=(Colors.GREEN, Colors.LIME)),
                InteractionState.DISABLED: generate_debug_image((constants.DEFAULT_BUTTON_WIDTH, constants.DEFAULT_BUTTON_HEIGHT), colors=(Colors.RED, Colors.ORANGE)),
            }

        self._original_sprite_sheet = self._parse_sprite_sheet(sprite_sheet)
        self._original_image_aspect_ratio = self._original_sprite_sheet[InteractionState.INACTIVE].get_width() / self._original_sprite_sheet[InteractionState.INACTIVE].get_height()

        self._sprite_sheet = {
            state: self._original_sprite_sheet[state].copy() for state in InteractionState
        }

        if preserve_aspect_ratio is None:
            preserve_aspect_ratio = True

        self._preserve_aspect_ratio = self._parse_preserve_aspect_ratio(preserve_aspect_ratio)

        BaseButton.__init__(self, x=x, y=y, width=width, height=height, theme=None, on_click=on_click,
                            on_hover=on_hover, border_radius=0, border_width=0)

    def _parse_preserve_aspect_ratio(self, preserve_aspect_ratio: bool) -> bool:
        if not isinstance(preserve_aspect_ratio, bool):
            raise TypeError(f"Preserve aspect ratio flag must be of type 'bool', not '{type(preserve_aspect_ratio)}'.")
        return preserve_aspect_ratio

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
                self._update_size(new_width, new_height)  # Recursively reach equilibrium size
                return

        for state in InteractionState:
            self._sprite_sheet[state] = pygame.transform.scale(self._original_sprite_sheet[state], (self._width, self._height))

    def _parse_sprite_sheet(self, sprite_sheet: Dict[InteractionState, pygame.Surface]) -> Dict[InteractionState, pygame.Surface]:
        if not isinstance(sprite_sheet, dict):
            raise TypeError(f"Sprite sheet must be of type 'dict', not '{type(sprite_sheet)}'.")

        size = None

        for state in InteractionState:
            if state not in sprite_sheet:
                raise ValueError(f"Sprite sheet is missing image for state '{state}'.")

            if not isinstance(sprite_sheet[state], pygame.Surface):
                raise TypeError(f"Sprite sheet image for state '{state}' must be of type 'pygame.Surface', not '{type(sprite_sheet[state])}'.")

            if size is None:
                size = sprite_sheet[state].get_size()
            elif sprite_sheet[state].get_size() != size:
                raise ValueError(f"All images in the sprite sheet must be the same size. Expected size {size}, but got {sprite_sheet[state].get_size()} for state '{state}'.")

        return sprite_sheet

    def draw(self, surface: pygame.Surface) -> None:
        image = self._sprite_sheet[self._state]
        image_rect = image.get_rect()
        image_rect.center = self.center
        surface.blit(image, image_rect)


    def _update_size(self, width: SupportsInt, height: SupportsInt) -> None:
        super()._update_size(width, height)
        self._resize_sprite_sheet()


