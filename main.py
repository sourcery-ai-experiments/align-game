import time
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

print('start:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))


class MyPaintApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logical_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.selected_color = None
        self.selected_button = None
        self.grid_layout = None

    def on_button_press(self, tile, row, col):
        print(row, col)
        if tile.background_color != BLACK:
            self.selected_color = tile.background_color
            self.selected_button = (tile, row, col)
            print('colored')
        elif tile.background_color == BLACK and self.selected_color:
            # self.selected_color is not None
            tile.background_color = self.selected_color
            self.logical_grid[row][col] = 1
            start = (self.selected_button[1], self.selected_button[2])
            end = (row, col)
            print(
                'find path start:', time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime(),
                ),
            )
            self.find_path(start, end)
            print(
                'find path end:', time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime(),
                ),
            )
            self.selected_button[0].background_color = BLACK
            self.logical_grid[start[0]][start[1]] = 0
            self.selected_color = None
            self.selected_button = None
            print(start, end)
        print(self.logical_grid)
        print(
            'button press:', time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(),
            ),
        )

    def assign_random_colors_to_buttons(self, buttons, colors):
        for btn, color in zip(buttons, colors):
            btn.background_color = color

    def build_grid_layout(self):
        self.grid_layout = GridLayout(
            cols=9, rows=9,
            size_hint=(None, None),
            size=(450, 450), pos=(330, 20),
        )
        for row in range(9):
            for col in range(9):
                btn = Button(background_color=[1, 1, 1, 1])
                btn.bind(
                    on_press=lambda instance, x=row,
                    y=col: self.on_button_press(instance, x, y),
                )
                self.grid_layout.add_widget(btn)
        return self.grid_layout

    def update_logical_grid_based_on_buttons(self):
        print(
            'update logical grid:', time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(),
            ),
        )
        for index, btn in enumerate(reversed(self.grid_layout.children)):
            row = index // 9
            col = index % 9
            if btn.background_color != BLACK:
                self.logical_grid[row][col] = 1
            else:
                self.logical_grid[row][col] = 0

    def find_path(self, start, end):
        path = astar(self.logical_grid, start, end)
        if path:
            print('Path found:', path)
            for pos in path:
                row, col = pos
                button_index = (8 - row) * 9 + col
                self.grid_layout.children[button_index].background_color = [
                    1, 1, 1, 1,
                ]

    # def get_button_position(self, button):
    #     index = self.grid_layout.children.index(button)
    #     row = 8 - index // 9
    #     col = index % 9
    #     return row, col

    def future_grid(self):
        button_layout = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(100, 250), pos=(50, 150),
        )
        left_buttons = []
        for i in range(3):
            btn = Button(
                text=f'Button {i+1}',
                background_color=choice(COLOR_LIST),
            )
            button_layout.add_widget(btn)
            left_buttons.append(btn)
        return button_layout, left_buttons

    def build(self):
        parent = Widget()
        grid_layout = self.build_grid_layout()
        button_layout, left_buttons = self.future_grid()
        random_buttons = sample(grid_layout.children, 3)
        print(
            'Current time:', time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(),
            ),
        )
        self.assign_random_colors_to_buttons(
            random_buttons, [btn.background_color for btn in left_buttons],
        )
        print(
            'Current time:', time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(),
            ),
        )
        self.update_logical_grid_based_on_buttons()
        print(
            'Current time:', time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(),
            ),
        )
        parent.add_widget(grid_layout)
        print(
            'Current time:', time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(),
            ),
        )
        parent.add_widget(button_layout)
        print(
            'Current time:', time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(),
            ),
        )
        return parent


if __name__ == '__main__':
    MyPaintApp().run()
