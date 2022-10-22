import buttonup
import pygame
import time


class Test:
    """Class to test the pygame window."""

    def __init__(self) -> None:
        """Initialize the pygame window."""
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0.0

        buttonup.globs.project_theme = "navy"

        self.button_1 = buttonup.button.DefaultButton(100, 100, width=130, height=80, text="add 0.1",
                                                      on_click_function=self.increase_slider_pos)
        self.button_2 = buttonup.button.DefaultButton(100, 200, width=130, height=40, text="2")
        self.button_2.state = "disabled"
        self.button_3 = buttonup.button.DefaultButton(100, 300, width=150, height=150, text="3", text_align_x="left",
                                                      text_align_y="top")
        self.button_4 = buttonup.button.DefaultButton(300, 100, width=40, height=130, text="4")
        self.button_5 = buttonup.button.DefaultButton(400, 100, width=130, height=40, text="swap",
                                                      on_click_function=self.swap_sld1_sld2)
        self.button_6 = buttonup.button.DefaultButton(400, 150, width=130, height=40, text="cycle",
                                                      on_click_function=self.cycle_themes)
        self.button_7 = buttonup.button.DefaultButton(400, 200, width=130, height=40, text="7",
                                                      rounded_corners_amount=0,
                                                      on_click_function=self.set_colored_label_text)

        self.slider_1 = buttonup.slider.DefaultSlider(300, 300)
        self.slider_2 = buttonup.slider.DefaultSlider(300, 340)
        self.label_1 = buttonup.label.DefaultLabel(215, 297, text="0.0", text_size=15)
        self.label_2 = buttonup.label.DefaultLabel(215, 337, text="0.0", text_size=15)

        self.textbox_1 = buttonup.textbox.DefaultTextBox(700, 100, width=450, height=300, text_size=20,
                                                         text=buttonup.Utility.testvars.text_large_sentences,
                                                         rounded_corners_amount=18)

        color_palette = buttonup.Tools.colors.ColorPalette()
        color_palette.add_reset("$reset$")
        color_palette.add_color("$red$", (255, 0, 0))
        color_palette.add_color("$green$", (0, 255, 0))
        color_palette.add_color("$white$", (255, 255, 255))

        self.colored_label_1 = buttonup.label.ColoredLabel(100, 600, "dfsadfa $red$HELLO $green$WORLD TEST "
                                                                     "$reset$resetted",
                                                           color_palette=color_palette, text_size=20,
                                                           font="consolas")

        self.elements = [self.button_1, self.button_2, self.button_3, self.button_4,
                         self.button_5, self.button_6, self.button_7, self.slider_1,
                         self.label_1, self.slider_2, self.label_2, self.textbox_1,
                         self.colored_label_1]

    def update(self) -> None:
        for e in self.elements:
            e.update(self.dt)

        self.button_3.text = self.button_3.state
        self.label_1.text = "{:10.3f}".format(self.slider_1.value)
        self.label_2.text = "{:10.3f}".format(self.slider_2.value)

    def events(self) -> None:
        """Handle events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            for e in self.elements:
                e.event(event)

    def draw(self) -> None:
        """Draw the pygame window."""
        self.screen.fill(buttonup.globs.project_theme.background)
        for e in self.elements:
            e.render(self.screen)

        pygame.display.flip()

    def run(self) -> float:
        """Run the pygame window.
        :return: Runtime in seconds.
        """

        time_start = time.time()
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(60)

        time_end = time.time()

        return time_end - time_start

    def increase_slider_pos(self) -> None:
        self.slider_1.value += 0.1

    def swap_sld1_sld2(self) -> None:
        self.slider_1.value, self.slider_2.value = self.slider_2.value, self.slider_1.value

    def cycle_themes(self) -> None:
        all_themes = buttonup.themes.get_all_themes()

        current_idx = all_themes.index(buttonup.globs.project_theme)

        try:
            theme = all_themes[current_idx + 1]
        except IndexError:
            theme = all_themes[0]

        buttonup.globs.project_theme = theme

        for element in self.elements:
            element.theme = theme

    def set_colored_label_text(self) -> None:
        new_text = input("Enter new text > ")
        self.colored_label_1.text = new_text
        self.colored_label_1.text_size += 3


if __name__ == "__main__":
    test = Test()
    time_run = test.run()
    print(f"Ran for {round(time_run, 3)}s.")
