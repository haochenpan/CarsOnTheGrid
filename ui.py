from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config
import proto
import config
import help_lib

Config.set('input', 'mouse', 'mouse, disable_multitouch')


def _decorate_button(button: Button, pos: tuple, cars: list):
    button.text = f'{pos}\n    {len(cars)}'
    button.background_color = config.GREEN
    for car in cars:
        if config.CONSTANT_SOURCE_THROUGHOUT:
            if car["when"] > 0:
                button.background_color = config.BLUE
            elif car["when"] == 0:
                button.background_color = config.RED
                break
        else:
            if car["when"] >= 0:
                button.background_color = config.RED
                break


class Grid(GridLayout, App):
    def __init__(self):
        super().__init__()
        self.rows = config.NUM_OF_ROWS
        self.cols = config.NUM_OF_COLS
        self.phrases = proto.grid_get_states()
        self.phrase_ctr = -1

    def build(self):
        self.add_widgets()
        return self

    def add_widgets(self):
        phrase = self._get_phrase()
        for r in range(config.FIRST_ROW_INDEX, config.FIRST_ROW_INDEX + self.rows):
            for c in range(config.FIRST_COL_INDEX, config.FIRST_COL_INDEX + self.cols):
                button = Button()
                _decorate_button(button, (r, c), phrase[(r, c)])
                if (r, c) == (config.FIRST_ROW_INDEX, config.FIRST_COL_INDEX):
                    button.bind(on_touch_down=self._on_click)
                self.add_widget(button)

    def _get_phrase(self, cmd="next"):
        if cmd == "next":
            self.phrase_ctr += 1
        else:
            self.phrase_ctr -= 1
        self.phrase_ctr = self.phrase_ctr % len(self.phrases)
        phrase = self.phrases[self.phrase_ctr]
        # help_lib.print_grid(phrase)
        print("self.phrase_ctr", self.phrase_ctr)
        return phrase

    def _on_click(self, instance, touch):
        if touch.button == 'left':
            phrase = self._get_phrase("next")
        else:
            phrase = self._get_phrase("prev")

        widget_ctr = -1
        for r in range(config.FIRST_ROW_INDEX, config.FIRST_ROW_INDEX + self.rows):
            for c in range(config.FIRST_COL_INDEX, config.FIRST_COL_INDEX + self.cols):
                button = self.children[widget_ctr]
                widget_ctr -= 1
                _decorate_button(button, (r, c), phrase[(r, c)])


if __name__ == '__main__':
    g = Grid()
    g.run()
