from buttonup.Utility import errors
from buttonup import constants
import logging
import json
import sys
import os

_log = logging.getLogger(__name__)

_all_themes = []


class Theme:
    def __init__(self, theme_dict: dict, name: str) -> None:
        """

        Assumes the theme_dict is valid.

        :param theme_dict: Dict of the theme. Obtained using _get_theme().
        :raises ValueError: If the dict is invalid.
        :raises ValueError: If the name is not a string.
        """

        if isinstance(name, str):
            self.name = name
        else:
            raise ValueError("name argument must be of type <dict>.")

        if isinstance(theme_dict, dict):
            pass
        else:
            raise ValueError("theme_dict argument must be of type <dict>.")


        try:
            self.primary = theme_dict["primary"]
            self.primary_variant = theme_dict["primary-variant"]
            self.secondary = theme_dict["secondary"]
            self.secondary_variant = theme_dict["secondary-variant"]
            self.background = theme_dict["background"]
            self.surface = theme_dict["surface"]
            self.error = theme_dict["error"]
            self.on_primary = theme_dict["on-primary"]
            self.on_secondary = theme_dict["on-secondary"]
            self.on_background = theme_dict["on-background"]
            self.on_surface = theme_dict["on-surface"]
            self.on_error = theme_dict["on-error"]
            self.brightness_offsets = theme_dict["brightness-offsets"]
        except KeyError:
            _log.error(f"Theme dict is missing essential color elements for theme: '{name}'.")
            raise ValueError("Theme dict is missing essential color elements.")

        try:
            self.info: dict = theme_dict["info"]
        except KeyError:
            self.info: None = None

        _log.debug(f"Created theme object '{name}'.")


def get_default_theme() -> Theme:
    """
    Gets the default theme.
    """

    for theme in _all_themes:
        if theme.name == "default":
            return theme

    else:
        _log.critical("Default theme not found.'")
        raise errors.DefaultThemeNotFoundError("Default theme not found.")


def _validate_theme_dict(theme_dict: dict) -> bool:
    """
    Validates the theme.
    Returns whether the theme is valid or invalid.
    That means the theme is missing some color elements.

    :param theme_dict: Dict of the theme. Obtained using _get_theme().
    :returns bool: True or False.
    """

    color_elements = constants._THEME_COLOR_ELEMENTS

    for element in color_elements:
        if element not in theme_dict:
            return False
    else:
        return True


def _get_theme_from_file(theme_name: str) -> dict | None:
    """
    Gets a theme dictionary from a file.

    :param theme_name: Name of the theme. Is interpreted by name of the file.
    :returns dict: Returns the theme if it was found.
    :returns None: Returns None if the theme was not found.
    """

    if not theme_name.endswith(".json"):
        theme_name += ".json"

    path_to_theme = os.path.join(str(__file__).replace(r"\themes.py", ""), theme_name)

    if os.path.isfile(path_to_theme):

        # file exists
        try:
            with open(path_to_theme, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            _log.debug(f"Theme '{theme_name}' not found.")
            return None

        return data

    else:
        raise ValueError(f"Theme '{theme_name}' not found. CWD: {os.getcwd()}")


def create_custom_theme(theme_dict: dict, name: str) -> Theme:
    """
    Create a custom theme from a theme_dict.
    :param theme_dict: 
    :return Theme: the created theme.
    :raises ValueError: If the theme_dict is incorrect.
    """

    return Theme(theme_dict, name)


def get_theme(theme_name: str) -> Theme:
    """
    Gets a theme from the theme name.
    If the theme is not found, it returns the default theme.
    :param theme_name: Name of the theme. Not case-sensitive.
    """

    if not isinstance(theme_name, str):
        _log.error("Theme name is not a string. Defaulting to default theme.")
        return get_default_theme()

    theme_name = theme_name.lower()

    for theme in _all_themes:
        if theme.name == theme_name:
            return theme
    else:
        return get_default_theme()


def reload() -> None:
    """
    Initializes the theme objects.
    Called on import.
    """

    # ------------------------------------------
    themes = [
        "default",
        "default_light",
        "navy",
        "powder_blue"
    ]
    # ------------------------------------------

    _all_themes.clear()

    for theme in themes:
        _all_themes.append(Theme(_get_theme_from_file(theme), name=theme))

    _log.debug(f"Initialized {len(themes)} themes.")


def get_all_themes() -> list:
    """
    Gets all theme names.
    """

    return _all_themes


reload()
