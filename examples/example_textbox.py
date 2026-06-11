import pygame
import buttonup
from base import ExampleBase
import time


class ExampleTextBox(ExampleBase):
    def __init__(self, WINDOW_WIDTH: int, WINDOW_HEIGHT: int) -> None:
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.theme = buttonup.theme.load_theme("dark")

        self._text_box = buttonup.TextBox(
            x=230,
            y=10,
            width=400,
            height=200,
            theme=self.theme,
            text="Wikipedia is a free online encyclopedia written and maintained by a community of volunteers, "
                 "known as Wikipedians, through open collaboration and the wiki software MediaWiki. Founded by Jimmy "
                 "Wales and Larry Sanger in 2001, Wikipedia has been hosted since 2003 by the Wikimedia Foundation, "
                 "an American nonprofit organization funded mainly by donations from readers. Wikipedia is the "
                 "largest and most read reference work in history.",
            wrap_behavior=buttonup.TextWrapBehavior.WORD,
            overflow_behavior=buttonup.TextOverflowBehavior.ELLIPSIS,
            border_radius=10,
            font="comic sans",
        )

        self._timer_label = buttonup.Label(
            x=0,
            y=0,
            text="Time: -",
            theme=self.theme,
        )

        self._profile_test_vbox = buttonup.VBox(
            x=10,
            y=10,
            width=200,
            height=200,
            elements=[
                self._timer_label,
                buttonup.TextButton(
                    x=0,
                    y=0,
                    width=180,
                    height=40,
                    text="Start Profile",
                    theme=self.theme,
                    on_click=self._test_profile_update_layout
                )
            ]
        )
        self._profile_test_vbox.apply()

    def _test_profile_update_layout(self) -> None:
        # Use a time module to profile the code
        start_time = time.perf_counter()

        self._text_box._update_layout()

        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        self._timer_label.text = f"Time: {self._format_time(elapsed_time)}"

    def _format_time(self, seconds: float) -> str:
        if seconds < 1e-3:
            return f"{seconds * 1e6:.2f} µs"
        elif seconds < 1:
            return f"{seconds * 1e3:.2f} ms"
        else:
            return f"{seconds:.2f} s"


    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self.theme.color.background)
        self._text_box.draw(surface)
        self._profile_test_vbox.draw(surface)

    def update(self, dt: float) -> None:
        self._text_box.update(dt)
        self._profile_test_vbox.update(dt)

    def handle_event(self, event: pygame.event.Event) -> None:
        self._text_box.handle_event(event)