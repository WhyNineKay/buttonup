from dataclasses import dataclass
from typing import Type, Tuple
import buttonup
from itertools import count

@dataclass(frozen=True)
class WillRaise:
    exception_type: Type[Exception]


def generate_testing_theme_dict() -> dict:
    template = buttonup.theme._load_builtin_theme_dict("dark")
    template = _crawl_and_fill(template, 0)
    template["name"] = "test_theme"
    return template


def _color_from_number(number: int) -> Tuple[int, int, int]:
    r = (number >> 16) & 0xFF
    g = (number >> 8) & 0xFF
    b = number & 0xFF
    return r, g, b


def _crawl_and_fill(d: dict, number: int) -> dict:
    """
    Recursively fill dictionary leaf values with RGB tuples derived from sequential numbers.
    Each non-dict leaf receives a color from _color_from_number, and the counter increments
    for every element across the whole structure (including siblings and nested elements).

    Args:
        d: Nested dictionary template to fill.
        number: Starting integer used to generate the first color.

    Returns:
        The same dictionary `d` with leaf values replaced by `(r, g, b)` tuples.
    """
    counter = count(start=number)

    def _fill(node: dict) -> dict:
        for key, value in node.items():
            if isinstance(value, dict):
                node[key] = _fill(value)
            else:
                node[key] = _color_from_number(next(counter))
        return node

    return _fill(d)