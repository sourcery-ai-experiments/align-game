from random import choice
from random import sample

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget

from astar import astar

BLACK = [1, 1, 1, 0]
COLOR_LIST = [
    [1, 0, 0, 1],     # Red
    [0, 1, 0, 1],     # Green
    # [0, 0, 1, 1],     # Blue
    # [1, 1, 0, 1],     # Yellow
    # [1, 0, 1, 1],     # Magenta
    # [0, 1, 1, 1],     # Cyan
    # [1, 0.5, 0, 1],   # Orange
    # [0.5, 0, 0.5, 1],  # Purple
]
IMAGE_LIST = [
    'assets/red.png',
    'assets/green.png',
    'assets/blue.png',
    'assets/yellow.png',
    'assets/magenta.png',
    'assets/cyan.png',
    'assets/orange.png',
    'assets/purple.png',
]


class MyPaintApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logical_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.pos_set = {(row, col) for row in range(9) for col in range(9)}
        self.spawn = True
        self.selected_color = None
        self.selected_button = None
        self.grid_layout = None
        self.button_layout = None
        self.path = []
        self.path_index = 0
        self.last_position = None

    def build_grid_layout(self):
        self.grid_layout = GridLayout(
            cols=9, rows=9, size_hint=(
                None, None,
            ), size=(555, 555), pos=(191, 48),
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
            orientation='vertical',
            size_hint=(None, None),
            size=(70, 305),  # Fixed size for the BoxLayout
            pos=(53, 206),
            spacing=44,  # Adjust spacing between widgets
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
        self.path = path
        self.path_index = 0
        self.last_position = start
        Clock.schedule_interval(self.update, 0.1)

    def update(self, dt):
        if self.path_index < len(self.path):
            if self.path_index > 0:
                last_row, last_col = self.path[self.path_index - 1]
                last_button = self.grid_layout.children[
                    9 * (8 - last_row) + (8 - last_col)
                ]
                last_button.background_color = BLACK
            current_pos = self.path[self.path_index]
            row, col = current_pos
            button = self.grid_layout.children[
                9 * (8 - row) + (8 - col)
            ]
            button.background_color = self.selected_color
            self.path_index += 1
        else:
            Clock.unschedule(self.update)
            start = self.selected_button[1], self.selected_button[2]
            self.update_logical_grid(
                self.path[-1][0], self.path[-1][1], start,
            )
            if self.spawn:
                self.assign_random_colors_to_buttons()
                adjacent_lines = self.find_adjacent_color(
                    self.path[-1][0], self.path[-1][1],
                )
                if adjacent_lines:
                    self.check_length_remove_square(adjacent_lines)

    def update_logical_grid(self, row, col, start):
        self.logical_grid[row][col] = 1
        self.pos_set.remove((row, col))
        self.selected_button[0].background_color = BLACK
        self.logical_grid[start[0]][start[1]] = 0
        self.pos_set.add((start[0], start[1]))
        self.selected_color = None
        self.selected_button = None

    def assign_random_colors_to_buttons(self):
        if len(self.pos_set) < 3 or not self.spawn:
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
        adjacent_lines = {
            0: [(row, col)],
            1: [(row, col)],
            2: [(row, col)],
            3: [(row, col)],
        }
        current_color = self.grid_layout.children[
            9 * (8 - row) + (8 - col)
        ].background_color
        for i, direction in enumerate(directions):
            x, y = row, col
            dir_x, dir_y = direction
            while True:
                x += dir_x
                y += dir_y
                try:
                    adjacent_button = self.grid_layout.children[
                        9 * (
                            8 - x
                        ) + (8 - y)
                    ]
                    adjacent_color = adjacent_button.background_color
                    if adjacent_color == current_color:
                        adjacent_lines[i % 4].append((x, y))
                    else:
                        break
                except IndexError:
                    break
        # print(adjacent_lines)
        return adjacent_lines

    def check_length_remove_square(self, lines):
        for line in lines.values():
            if len(line) >= 5:
                self.spawn = False
                print('Spawn Flag Set to False')
                for x, y in line:
                    if 0 <= x < 9 and 0 <= y < 9:
                        self.grid_layout.children[
                            9 * (8 - x) + (8 - y)
                        ].background_color = BLACK
                        self.logical_grid[x][y] = 0
                        self.pos_set.add((x, y))
                    else:
                        print(f'losho, out of bounds ({x}, {y})')
                self.spawn = True

    def build(self):
        Window.size = (800, 800)
        Window.minimum_size = (400, 300)
        Window.maximum_size = (1000, 800)
        parent = BoxLayout(orientation='vertical')
        parent = Widget()
        parent = FloatLayout()
        background = Image(
            source='assets/board.jpg',
            allow_stretch=True, keep_ratio=True,
        )
        parent.add_widget(background)
        parent.add_widget(self.build_grid_layout())
        parent.add_widget(self.build_predicted_layout())
        self.assign_random_colors_to_buttons()
        return parent


if __name__ == '__main__':
    MyPaintApp().run()
