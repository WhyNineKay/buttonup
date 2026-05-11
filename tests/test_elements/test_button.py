import unittest
import buttonup
from ..testing_tools import WillRaise, generate_testing_theme_dict


class TestBaseButton(unittest.TestCase):
    def test_init_no_args(self):
        button = buttonup.elements.button.BaseButton(0, 0)

