from buttonup.Themes import themes
import logging
import pygame

log = logging.getLogger(__name__)


class Element:
    """Base Element Class"""
    def __init__(self) -> None:
        self._theme = themes.get_default_theme()

    def render(self, screen: pygame.Surface) -> None:
        """Renders the element to the screen."""
        pass

    def update(self, dt: float) -> None:
        """
        Updates the element.
        :param dt: Delta time. Optional for some elements.
        """
        pass

    def event(self, event: pygame.event.Event) -> None:
        """
        Handles a pygame event.
        Call this in the event loop.
        """
        pass

    @property
    def theme(self) -> themes.Theme:
        """
        Gets the current theme that the object is using.
        :return: Theme object.
        """
        return self._theme

    @theme.setter
    def theme(self, value: themes.Theme | str) -> None:
        """
        Sets the theme and reloads the colours.
        Returns the default theme if it is not found.

        :param value: Theme object or the name of the theme.
        :raises ValueError: If theme object is not a valid theme.
        """

        if not isinstance(value, themes.Theme) and not isinstance(value, str):
            raise ValueError("Invalid theme. Use a Theme object theme or a string of the name of the theme.")

        if isinstance(value, themes.Theme):
            theme = value

        elif isinstance(value, str):
            # it is a string
            theme = themes.get_theme(value)

        else:
            log.debug("Unreachable code. Defaulting to default theme.")
            theme = themes.get_default_theme()

        self._theme = theme

        self._create_colors()

    def _create_colors(self) -> None:
        pass
