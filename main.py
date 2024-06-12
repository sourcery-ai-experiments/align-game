from random import choice
from random import sample

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

from astar import astar
BLACK = [1, 1, 1, 1]
COLOR_LIST = [
    [1, 0, 0, 1],     # Red
    [0, 1, 0, 1],     # Green
    [0, 0, 1, 1],     # Blue
    [1, 1, 0, 1],     # Yellow
    [1, 0, 1, 1],     # Magenta
    [0, 1, 1, 1],     # Cyan
    [1, 0.5, 0, 1],   # Orange
    [0.5, 0, 0.5, 1],  # Purple
]


class MyPaintApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logical_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.pos_set = {(row, col) for row in range(9) for col in range(9)}
        self.selected_color = None
        self.selected_button = None
        self.grid_layout = None
        self.button_layout = None

    def on_button_press(self, tile, row, col):
        print(row, col)
        if tile.background_color != BLACK:
            self.selected_color = tile.background_color
            self.selected_button = (tile, row, col)
        elif tile.background_color == BLACK and self.selected_color:
            start = (self.selected_button[1], self.selected_button[2])
            end = (row, col)
            path = astar(self.logical_grid, start, end)
            if not path:
                return
            tile.background_color = self.selected_color
            self.logical_grid[row][col] = 1
            self.selected_button[0].background_color = BLACK
            self.logical_grid[start[0]][start[1]] = 0
            self.selected_color = None
            self.selected_button = None
            self.assign_random_colors_to_buttons()
        print('-----------------------')
        for inner_list in self.logical_grid:
            print(inner_list)

    def assign_random_colors_to_buttons(self):
        cords = sample(self.pos_set, 3)
        colors = []
        for btn in self.button_layout.children:
            colors.append(btn.background_color)
            btn.background_color = choice(COLOR_LIST)
        for cord, color in zip(cords, colors):
            row, col = cord
            # print(row, col)
            # print(self.pos_set)
            button = self.grid_layout.children[9 * (8 - row) + (8 - col)]
            button.background_color = color
            self.pos_set.remove(cord)
            self.logical_grid[cord[0]][cord[1]] = 1
        # print(len(self.pos_set))

    def build_grid_layout(self):
        self.grid_layout = GridLayout(
            cols=9, rows=9,
            size_hint=(None, None),
            size=(450, 450), pos=(330, 20),
        )
        for row in range(9):
            for col in range(9):
                btn = Button(background_color=BLACK)
                btn.bind(
                    on_press=lambda tile, x=row,
                    y=col: self.on_button_press(tile, x, y),
                )
                self.grid_layout.add_widget(btn)
        return self.grid_layout

    def future_grid(self):
        self.button_layout = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(100, 250), pos=(50, 150),
        )
        for i in range(3):
            btn = Button(
                text=f'Button {i+1}',
                background_color=choice(COLOR_LIST),
            )
            self.button_layout.add_widget(btn)

    def build(self):
        parent = Widget()
        grid_layout = self.build_grid_layout()
        self.future_grid()
        self.assign_random_colors_to_buttons()
        parent.add_widget(grid_layout)
        parent.add_widget(self.button_layout)
        return parent


if __name__ == '__main__':
    MyPaintApp().run()
