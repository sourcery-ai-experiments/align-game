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

    def build_grid_layout(self):
        self.grid_layout = GridLayout(
            cols=9, rows=9, size_hint=(
                None, None,
            ), size=(450, 450), pos=(330, 20),
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

    def build_predicted_layout(self):
        self.button_layout = BoxLayout(
            orientation='vertical', size_hint=(
                None, None,
            ), size=(100, 250), pos=(50, 150),
        )
        for i in range(3):
            btn = Button(
                text=f'Button {i+1}',
                background_color=choice(COLOR_LIST),
            )
            self.button_layout.add_widget(btn)
        return self.button_layout

    def on_button_press(self, tile, row, col):
        # print(row, col)
        if tile.background_color != BLACK:
            self.select_button(tile, row, col)
        elif tile.background_color == BLACK and self.selected_color:
            self.move_selected_button(tile, row, col)
        print('---------------------')
        for cord in self.logical_grid:
            print(cord)

    def select_button(self, tile, row, col):
        self.selected_color = tile.background_color
        self.selected_button = (tile, row, col)

    def move_selected_button(self, tile, row, col):
        start = (self.selected_button[1], self.selected_button[2])
        end = (row, col)
        path = astar(self.logical_grid, start, end)
        if not path:
            return
        tile.background_color = self.selected_color
        self.update_logical_grid(row, col, start)
        self.assign_random_colors_to_buttons()
        self.find_adjacent_color(row, col)

    def update_logical_grid(self, row, col, start):
        self.logical_grid[row][col] = 1
        self.pos_set.remove((row, col))
        self.selected_button[0].background_color = BLACK
        self.logical_grid[start[0]][start[1]] = 0
        self.pos_set.add((start[0], start[1]))
        self.selected_color = None
        self.selected_button = None

    def assign_random_colors_to_buttons(self):
        if len(self.pos_set) < 3:
            return
        cords = sample(self.pos_set, 3)
        colors = [btn.background_color for btn in self.button_layout.children]
        for btn in self.button_layout.children:
            btn.background_color = choice(COLOR_LIST)
        self.update_grid_with_new_colors(cords, colors)

    def update_grid_with_new_colors(self, cords, colors):
        for cord, color in zip(cords, colors):
            row, col = cord
            button = self.grid_layout.children[9 * (8 - row) + (8 - col)]
            button.background_color = color
            self.pos_set.remove(cord)
            self.logical_grid[cord[0]][cord[1]] = 1
            if len(self.pos_set) <= 0:
                print('Game Over')
                break

    def find_adjacent_color(self, row, col):
        directions = [
            (1, 0),  (0, 1), (1, 1), (1, -1),
            (-1, 0),  (0, -1), (-1, -1), (-1, 1),
        ]
# it needs to store cords in dictionarys so to have key:vlue and no duplictes
        adjacent_buttons = []
        current_color = self.grid_layout.children[
            9 * (8 - row) + (8 - col)
        ].background_color
        for direction in directions:
            dir_x, dir_y = direction
            adjacent_row, adjacent_col = row + dir_x, col + dir_y
            if 0 <= adjacent_row < 9 and 0 <= adjacent_col < 9:
                adjacent_button = self.grid_layout.children[
                    9 * (8 - adjacent_row) + (8 - adjacent_col)
                ]
                if adjacent_button.background_color == current_color:
                    adjacent_buttons.append((adjacent_row, adjacent_col))
        print(adjacent_buttons)
        return adjacent_buttons

    def build(self):
        parent = Widget()
        parent.add_widget(self.build_grid_layout())
        parent.add_widget(self.build_predicted_layout())
        self.assign_random_colors_to_buttons()
        return parent


if __name__ == '__main__':
    MyPaintApp().run()
