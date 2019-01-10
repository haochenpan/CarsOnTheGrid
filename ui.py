from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty
import proto
import config


class Grid(GridLayout):
    def __init__(self):
        super().__init__()
        self.gen = proto.grid_generator()
        self.rows = config.NUM_OF_ROWS
        self.cols = config.NUM_OF_COLS

    def on_click(self, instance):
        self.children = []
        self.add_widgets()

    def add_widgets(self):
        try:
            grid = next(self.gen)
        except StopIteration:
            exit(0)
        for r in range(config.FIRST_ROW_INDEX, config.FIRST_ROW_INDEX + config.NUM_OF_ROWS):
            for c in range(config.FIRST_COL_INDEX, config.FIRST_COL_INDEX + config.NUM_OF_COLS):
                btn = Button(text=f'{(r, c)}\n    {len(grid[(r, c)])}')
                btn.background_color = [1, 50, 0, 150]  # green
                for car in grid[(r, c)]:

                    # for ! become source
                    # if car["when"] == 0:
                    #     btn.background_color = [50, 1, 0, 150]  # red
                    #     break
                    # if car["when"] > 0:
                    #     btn.background_color = [5, 50, 0, 150]  # yellow

                    # for can become source
                    if car["when"] >= 0:
                        btn.background_color = [50, 1, 0, 150]  # red
                btn.bind(on_press=self.on_click)
                self.add_widget(btn)




class GridApp(App):

    def build(self):
        layout = Grid()
        layout.add_widgets()
        return layout


if __name__ == '__main__':
    g = GridApp()
    g.run()
