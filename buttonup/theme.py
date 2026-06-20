"""
theme.py

Themes
Must be able to load from:
 - File path (.json)
 - Theme name (built-in)
 - Theme dict

"""
import copy
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from .buttonup_types import RGB
from .utils import ColorTools

FILE_PATH_BUILTIN_THEMES = Path(__file__).parent / "themes"
DEFAULT_THEME_NAME = "dark"


@dataclass(slots=True)
class LabelTheme:
    text_color: RGB

    def copy(self) -> "LabelTheme":
        return copy.copy(self)


@dataclass(slots=True)
class ButtonTheme:
    base_color: RGB
    base_color_pressed: RGB
    base_color_hovered: RGB
    base_color_disabled: RGB
    border_color: RGB
    border_color_pressed: RGB
    border_color_hovered: RGB
    border_color_disabled: RGB
    text_color: RGB
    text_color_pressed: RGB
    text_color_hovered: RGB
    text_color_disabled: RGB

    def copy(self) -> "ButtonTheme":
        return copy.copy(self)


@dataclass(slots=True)
class ColorTheme:
    background: RGB
    surface: RGB
    primary: RGB
    secondary: RGB
    text_surface: RGB
    text_background: RGB

    def copy(self) -> "ColorTheme":
        return copy.copy(self)


@dataclass(slots=True)
class CheckboxTheme:
    base_color: RGB
    base_color_pressed: RGB
    base_color_hovered: RGB
    base_color_disabled: RGB
    base_color_checked: RGB
    border_color: RGB
    border_color_pressed: RGB
    border_color_hovered: RGB
    border_color_disabled: RGB
    border_color_checked: RGB
    text_color: RGB
    text_color_pressed: RGB
    text_color_hovered: RGB
    text_color_disabled: RGB
    text_color_checked: RGB
    check_color: RGB
    check_color_pressed: RGB
    check_color_hovered: RGB
    check_color_disabled: RGB
    check_color_checked: RGB

    def copy(self) -> "CheckboxTheme":
        return copy.copy(self)


@dataclass(slots=True)
class TextInputTheme:
    base_color: RGB
    base_color_focused: RGB
    base_color_hovered: RGB
    base_color_disabled: RGB
    border_color: RGB
    border_color_focused: RGB
    border_color_hovered: RGB
    border_color_disabled: RGB
    text_color: RGB
    text_color_focused: RGB
    text_color_hovered: RGB
    text_color_disabled: RGB
    placeholder_color: RGB
    caret_color: RGB

    def copy(self) -> "TextInputTheme":
        return copy.copy(self)


@dataclass(slots=True)
class ContainerTheme:
    base_color: RGB
    border_color: RGB
    text_color: RGB

    def copy(self) -> "ContainerTheme":
        return copy.copy(self)


@dataclass(slots=True)
class SwitchTheme:
    base_color: RGB
    base_color_pressed: RGB
    base_color_hovered: RGB
    base_color_disabled: RGB
    base_color_dragging: RGB
    border_color: RGB
    border_color_pressed: RGB
    border_color_hovered: RGB
    border_color_disabled: RGB
    border_color_dragging: RGB
    text_color: RGB
    text_color_pressed: RGB
    text_color_hovered: RGB
    text_color_disabled: RGB
    text_color_dragging: RGB
    knob_color: RGB
    knob_color_pressed: RGB
    knob_color_hovered: RGB
    knob_color_disabled: RGB
    knob_color_dragging: RGB

    def copy(self) -> "SwitchTheme":
        return copy.copy(self)


@dataclass(slots=True)
class SliderTheme:
    base_color: RGB
    base_color_pressed: RGB
    base_color_hovered: RGB
    base_color_disabled: RGB
    border_color: RGB
    border_color_pressed: RGB
    border_color_hovered: RGB
    border_color_disabled: RGB
    knob_color: RGB
    knob_color_pressed: RGB
    knob_color_hovered: RGB
    knob_color_disabled: RGB

    def copy(self) -> "SliderTheme":
        return copy.copy(self)


@dataclass(slots=True)
class TextBoxTheme:
    base_color: RGB
    border_color: RGB
    text_color: RGB

    def copy(self) -> "TextBoxTheme":
        return copy.copy(self)


class Theme:
    def __init__(self, theme_dict: Dict) -> None:
        self._name = self._parse_name(theme_dict)

        self._label_theme = self._parse_label_dict(theme_dict)
        self._button_theme = self._parse_button_dict(theme_dict)
        self._color_theme = self._parse_color_dict(theme_dict)
        self._checkbox_theme = self._parse_checkbox_dict(theme_dict)
        self._text_input_theme = self._parse_text_input_dict(theme_dict)
        self._container_theme = self._parse_container_dict(theme_dict)
        self._switch_theme = self._parse_switch_dict(theme_dict)
        self._slider_theme = self._parse_slider_dict(theme_dict)
        self._text_box_theme = self._parse_text_box_dict(theme_dict)

    def _parse_text_box_dict(self, theme_dict: Dict) -> TextBoxTheme:
        element_name = "text_box"
        element_dict = self._get_element_dict(theme_dict, element_name)

        return TextBoxTheme(
            base_color=self._parse_element_color(element_dict, element_name, "base_color"),
            border_color=self._parse_element_color(element_dict, element_name, "border_color"),
            text_color=self._parse_element_color(element_dict, element_name, "text_color"),
        )

    def _parse_slider_dict(self, theme_dict: Dict) -> SliderTheme:
        element_name = "slider"
        element_dict = self._get_element_dict(theme_dict, element_name)

        return SliderTheme(
            base_color=self._parse_element_color(element_dict, element_name, "base_color"),
            base_color_pressed=self._parse_element_color(element_dict, element_name, "base_color_pressed"),
            base_color_hovered=self._parse_element_color(element_dict, element_name, "base_color_hovered"),
            base_color_disabled=self._parse_element_color(element_dict, element_name, "base_color_disabled"),
            border_color=self._parse_element_color(element_dict, element_name, "border_color"),
            border_color_pressed=self._parse_element_color(element_dict, element_name, "border_color_pressed"),
            border_color_hovered=self._parse_element_color(element_dict, element_name, "border_color_hovered"),
            border_color_disabled=self._parse_element_color(element_dict, element_name, "border_color_disabled"),
            knob_color=self._parse_element_color(element_dict, element_name, "knob_color"),
            knob_color_pressed=self._parse_element_color(element_dict, element_name, "knob_color_pressed"),
            knob_color_hovered=self._parse_element_color(element_dict, element_name, "knob_color_hovered"),
            knob_color_disabled=self._parse_element_color(element_dict, element_name, "knob_color_disabled")
        )

    def _parse_switch_dict(self, theme_dict: Dict) -> SwitchTheme:
        element_name = "switch"
        element_dict = self._get_element_dict(theme_dict, element_name)

        return SwitchTheme(
            base_color=self._parse_element_color(element_dict, element_name, "base_color"),
            base_color_pressed=self._parse_element_color(element_dict, element_name, "base_color_pressed"),
            base_color_hovered=self._parse_element_color(element_dict, element_name, "base_color_hovered"),
            base_color_disabled=self._parse_element_color(element_dict, element_name, "base_color_disabled"),
            base_color_dragging=self._parse_element_color(element_dict, element_name, "base_color_dragging"),
            border_color=self._parse_element_color(element_dict, element_name, "border_color"),
            border_color_pressed=self._parse_element_color(element_dict, element_name, "border_color_pressed"),
            border_color_hovered=self._parse_element_color(element_dict, element_name, "border_color_hovered"),
            border_color_disabled=self._parse_element_color(element_dict, element_name, "border_color_disabled"),
            border_color_dragging=self._parse_element_color(element_dict, element_name, "border_color_dragging"),
            text_color=self._parse_element_color(element_dict, element_name, "text_color"),
            text_color_pressed=self._parse_element_color(element_dict, element_name, "text_color_pressed"),
            text_color_hovered=self._parse_element_color(element_dict, element_name, "text_color_hovered"),
            text_color_disabled=self._parse_element_color(element_dict, element_name, "text_color_disabled"),
            text_color_dragging=self._parse_element_color(element_dict, element_name, "text_color_dragging"),
            knob_color=self._parse_element_color(element_dict, element_name, "knob_color"),
            knob_color_pressed=self._parse_element_color(element_dict, element_name, "knob_color_pressed"),
            knob_color_hovered=self._parse_element_color(element_dict, element_name, "knob_color_hovered"),
            knob_color_disabled=self._parse_element_color(element_dict, element_name, "knob_color_disabled"),
            knob_color_dragging=self._parse_element_color(element_dict, element_name, "knob_color_dragging")
        )

    def _parse_container_dict(self, theme_dict: Dict) -> ContainerTheme:
        element_name = "container"
        element_dict = self._get_element_dict(theme_dict, element_name)

        return ContainerTheme(
            base_color=self._parse_element_color(element_dict, element_name, "base_color"),
            border_color=self._parse_element_color(element_dict, element_name, "border_color"),
            text_color=self._parse_element_color(element_dict, element_name, "text_color")
        )

    def _parse_text_input_dict(self, theme_dict: Dict) -> TextInputTheme:
        element_name = "text_input"
        element_dict = self._get_element_dict(theme_dict, element_name)

        return TextInputTheme(
            base_color=self._parse_element_color(element_dict, element_name, "base_color"),
            base_color_focused=self._parse_element_color(element_dict, element_name, "base_color_focused"),
            base_color_hovered=self._parse_element_color(element_dict, element_name, "base_color_hovered"),
            base_color_disabled=self._parse_element_color(element_dict, element_name, "base_color_disabled"),
            border_color=self._parse_element_color(element_dict, element_name, "border_color"),
            border_color_focused=self._parse_element_color(element_dict, element_name, "border_color_focused"),
            border_color_hovered=self._parse_element_color(element_dict, element_name, "border_color_hovered"),
            border_color_disabled=self._parse_element_color(element_dict, element_name, "border_color_disabled"),
            text_color=self._parse_element_color(element_dict, element_name, "text_color"),
            text_color_focused=self._parse_element_color(element_dict, element_name, "text_color_focused"),
            text_color_hovered=self._parse_element_color(element_dict, element_name, "text_color_hovered"),
            text_color_disabled=self._parse_element_color(element_dict, element_name, "text_color_disabled"),
            placeholder_color=self._parse_element_color(element_dict, element_name, "placeholder_color"),
            caret_color=self._parse_element_color(element_dict, element_name, "caret_color")
        )

    def _parse_checkbox_dict(self, theme_dict: Dict) -> CheckboxTheme:
        element_name = "checkbox"
        element_dict = self._get_element_dict(theme_dict, element_name)

        return CheckboxTheme(
            base_color=self._parse_element_color(element_dict, element_name, "base_color"),
            base_color_pressed=self._parse_element_color(element_dict, element_name, "base_color_pressed"),
            base_color_hovered=self._parse_element_color(element_dict, element_name, "base_color_hovered"),
            base_color_disabled=self._parse_element_color(element_dict, element_name, "base_color_disabled"),
            base_color_checked=self._parse_element_color(element_dict, element_name, "base_color_checked"),
            border_color=self._parse_element_color(element_dict, element_name, "border_color"),
            border_color_pressed=self._parse_element_color(element_dict, element_name, "border_color_pressed"),
            border_color_hovered=self._parse_element_color(element_dict, element_name, "border_color_hovered"),
            border_color_disabled=self._parse_element_color(element_dict, element_name, "border_color_disabled"),
            border_color_checked=self._parse_element_color(element_dict, element_name, "border_color_checked"),
            text_color=self._parse_element_color(element_dict, element_name, "text_color"),
            text_color_pressed=self._parse_element_color(element_dict, element_name, "text_color_pressed"),
            text_color_hovered=self._parse_element_color(element_dict, element_name, "text_color_hovered"),
            text_color_disabled=self._parse_element_color(element_dict, element_name, "text_color_disabled"),
            text_color_checked=self._parse_element_color(element_dict, element_name, "text_color_checked"),
            check_color=self._parse_element_color(element_dict, element_name, "check_color"),
            check_color_pressed=self._parse_element_color(element_dict, element_name, "check_color_pressed"),
            check_color_hovered=self._parse_element_color(element_dict, element_name, "check_color_hovered"),
            check_color_disabled=self._parse_element_color(element_dict, element_name, "check_color_disabled"),
            check_color_checked=self._parse_element_color(element_dict, element_name, "check_color_checked")
        )

    def _parse_color_dict(self, theme_dict: Dict) -> ColorTheme:
        color_dict = theme_dict.get("colors")

        if color_dict is None:
            raise ValueError(f"Theme dict missing required key 'colors'.")
        if not isinstance(color_dict, dict):
            raise ValueError(f"Theme dict key 'colors' must be of type 'dict'.")

        return ColorTheme(
            background=self._parse_element_color(color_dict, "colors", "background"),
            surface=self._parse_element_color(color_dict, "colors", "surface"),
            primary=self._parse_element_color(color_dict, "colors", "primary"),
            secondary=self._parse_element_color(color_dict, "colors", "secondary"),
            text_surface=self._parse_element_color(color_dict, "colors", "text_surface"),
            text_background=self._parse_element_color(color_dict, "colors", "text_background")
        )

    def _parse_button_dict(self, theme_dict: Dict) -> ButtonTheme:
        element_name = "button"
        element_dict = self._get_element_dict(theme_dict, element_name)

        return ButtonTheme(
            base_color=self._parse_element_color(element_dict, element_name, "base_color"),
            base_color_pressed=self._parse_element_color(element_dict, element_name, "base_color_pressed"),
            base_color_hovered=self._parse_element_color(element_dict, element_name, "base_color_hovered"),
            base_color_disabled=self._parse_element_color(element_dict, element_name, "base_color_disabled"),
            border_color=self._parse_element_color(element_dict, element_name, "border_color"),
            border_color_pressed=self._parse_element_color(element_dict, element_name, "border_color_pressed"),
            border_color_hovered=self._parse_element_color(element_dict, element_name, "border_color_hovered"),
            border_color_disabled=self._parse_element_color(element_dict, element_name, "border_color_disabled"),
            text_color=self._parse_element_color(element_dict, element_name, "text_color"),
            text_color_pressed=self._parse_element_color(element_dict, element_name, "text_color_pressed"),
            text_color_hovered=self._parse_element_color(element_dict, element_name, "text_color_hovered"),
            text_color_disabled=self._parse_element_color(element_dict, element_name, "text_color_disabled")
        )

    def _parse_label_dict(self, theme_dict: Dict) -> LabelTheme:
        element_name = "label"
        element_dict = self._get_element_dict(theme_dict, element_name)

        return LabelTheme(
            text_color=self._parse_element_color(element_dict, element_name, "text_color")
        )

    @staticmethod
    def _get_element_dict(theme_dict: Dict, element_name: str) -> Dict:
        elements_dict: Optional[Dict] = theme_dict.get("elements")

        if elements_dict is None:
            raise ValueError(f"Theme dict missing required key 'elements'.")
        if not isinstance(elements_dict, dict):
            raise ValueError(f"Theme dict key 'elements' must be of type 'dict'.")

        element_dict = elements_dict.get(element_name)

        if element_dict is None:
            raise ValueError(f"Theme dict missing required key '{element_name}' in 'elements' dict.")
        if not isinstance(element_dict, dict):
            raise ValueError(f"Theme dict key '{element_name}' must be of type 'dict'.")

        return element_dict

    @staticmethod
    def _parse_element_color(element_dict: dict, element_name: str, color_key: str) -> RGB:
        raw_color = element_dict.get(color_key)

        if raw_color is None:
            raise ValueError(f"Theme dict missing required key '{color_key}' in '{element_name}' element dict.")

        if ColorTools.is_color(raw_color):
            return ColorTools.to_rgb(raw_color)
        else:
            raise ValueError(f"Color value for '{color_key}' in '{element_name}' element dict must be of type 'str', "
                             f"or RGB tuple, not '{type(raw_color)}'.")

    @staticmethod
    def _parse_name(theme_dict: Dict) -> str:
        name = theme_dict.get("name")
        if name is None:
            raise ValueError(f"Theme dict must have a 'name' key.")
        if not isinstance(name, str):
            raise ValueError(f"Key 'name' in theme dict must be of type 'str'.")
        return name

    @property
    def name(self) -> str:
        return self._name

    @property
    def label_theme(self) -> LabelTheme:
        return self._label_theme

    @property
    def button_theme(self) -> ButtonTheme:
        return self._button_theme

    @property
    def color(self) -> ColorTheme:
        return self._color_theme

    @property
    def checkbox_theme(self) -> CheckboxTheme:
        return self._checkbox_theme

    @property
    def text_input_theme(self) -> TextInputTheme:
        return self._text_input_theme

    @property
    def container_theme(self) -> ContainerTheme:
        return self._container_theme

    @property
    def switch_theme(self) -> SwitchTheme:
        return self._switch_theme

    @property
    def slider_theme(self) -> SliderTheme:
        return self._slider_theme

    @property
    def text_box_theme(self) -> TextBoxTheme:
        return self._text_box_theme


ThemeLike = Theme | Dict | str | Path


def _get_file_name(theme_name: str) -> Path:
    return FILE_PATH_BUILTIN_THEMES / f"{theme_name}.json"


def _is_builtin_theme(theme_name: str) -> bool:
    """
    Check if the theme_name is in the themes directory.
    """
    file_name = _get_file_name(theme_name)

    return file_name.exists()


def _load_builtin_theme_dict(theme_name: str) -> Dict:
    file_name = _get_file_name(theme_name)

    if not file_name.exists():
        raise ValueError(f"Theme '{theme_name}' not found in built-in themes.")

    with open(file_name, "r") as f:
        theme_dict = json.load(f)

    return theme_dict


_theme_cache: Dict[str, Theme] = {}


def load_theme(theme: ThemeLike) -> Theme:
    if isinstance(theme, Theme):
        return theme

    elif isinstance(theme, dict):
        return Theme(theme)

    elif isinstance(theme, str):
        if theme in _theme_cache:
            return _theme_cache[theme]

        if _is_builtin_theme(theme):
            theme_object = Theme(_load_builtin_theme_dict(theme))

            _theme_cache[theme] = theme_object

            return theme_object
        else:
            raise ValueError(f"Theme '{theme}' not found in built-in themes.")

    elif isinstance(theme, Path):
        if not theme.exists():
            raise ValueError(f"Theme file '{theme}' does not exist.")

        if not theme.is_file():
            raise ValueError(f"Theme file '{theme}' is not a file.")

        if not theme.suffix == ".json":
            raise ValueError(f"Theme file '{theme}' must have a .json extension.")

        with open(theme, "r") as f:
            theme_dict = json.load(f)

        return Theme(theme_dict)

    else:
        raise TypeError(f"Theme '{theme}' is not a valid Theme, Path, dict, or built-in theme name.")


# TODO: make loading default theme come from cache and not from file every time
def load_default_theme() -> Theme:
    return Theme(_load_builtin_theme_dict(DEFAULT_THEME_NAME))
