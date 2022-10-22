import pygame

from buttonup.Themes import themes
from buttonup.Utility.globs import globs


class ToolTip:
    def __init__(self,
                 pos_x: int,
                 pos_y: int,
                 width: int = 200,
                 height: int = 40,
                 theme: themes.Theme | str = None,
                 text: str = "",
                 text_size: int = 20,
                 font: str = "consolas",
                 rounded_corners_amount: int = -1) -> None:
        """
        Initialize the ToolTip.
        :param pos_x: X coordinate of the ToolTip.
        :param pos_y: Y coordinate of the ToolTip.
        :param width: Width of the ToolTip.
        :param height: Height of the ToolTip.
        :param theme: Theme object. Defaults to globs.project_theme.
        :param text: Text to display in the ToolTip.
        :param text_size: Size of the text.
        :param font: Font to use.
        :param rounded_corners_amount: Amount of rounded corners. -1 means no rounded corners. Defaults to -1.
        :raise ValueError: If any of the parameters are invalid.
        """

        if isinstance(pos_x, int):
            self._pos_x = pos_x
        else:
            raise ValueError("position values must be of type <int>.")

        if isinstance(pos_y, int):
            self._pos_y = pos_y
        else:
            raise ValueError("position values must be of type <int>.")

        if isinstance(width, int):
            self._width = width
        else:
            raise ValueError("size values must be of type <int>.")

        if isinstance(height, int):
            self._height = height
        else:
            raise ValueError("size values must be of type <int>.")

        if isinstance(text, str):
            self._text = text
        else:
            raise ValueError("text argument must be of type <str>.")

        if isinstance(text_size, int):
            self._text_size = text_size
        else:
            raise ValueError("text_size must be of type <int>.")

        if isinstance(font, str):
            self._font = pygame.font.SysFont(font, text_size)
        else:
            raise ValueError("font argument must be of type <str>.")

        if isinstance(rounded_corners_amount, int):
            self._rounded_corners_amount = rounded_corners_amount
        else:
            raise ValueError("rounded_corners_amount must be of type <int>.")

        if theme is None:
            self._theme = globs.project_theme
        elif isinstance(theme, themes.Theme):
            self._theme = theme
        elif isinstance(theme, str):
            self._theme = themes.get_theme(str(theme))
        else:
            raise ValueError("theme argument must be of type <str> or <Theme>.")

        self._rect = pygame.Rect(self._pos_x, self._pos_y, self._width, self._height)
        self._text_surface = self._font.render(self._text, True, self._theme.on_surface)
        self._text_rect = self._text_surface.get_rect()
        self._hidden = False

    def update(self, dt: float) -> None:
        """
        Update the ToolTip.

        Main functions of the ToolTip.
        Cursor must be focused on the ToolTip for it to be active,
        otherwise it will be hidden.
        ToolTips should be positioned at the center of the cursor.
        Tooltips will not be re-used, so they must be created again if they are needed.
        Elements such as buttons and sliders must use their own system for whether a tooltip should be created.
        Tooltips are not hidden on initialization. Tooltips should be deleted if the _hidden attribute is True.

        :param dt: Time since last update.
        """

        if self._hidden:
            return

        mouse_pos = pygame.mouse.get_pos()

        if not self._rect.collidepoint(mouse_pos):
            self._hidden = True
            globs.focused_other = False
            return

        if globs.focused_other:
            self._hidden = True
            return
        else:
            globs.focused_other = True



