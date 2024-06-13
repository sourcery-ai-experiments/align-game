from random import choice
from random import choices

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

from astar import astar
BLACK = [0, 0, 0, 0]
BOARD = 'assets/board.jpg'
TRANS = 'assets/trans.png'
IMAGE_LIST = [
    'assets/pink.png',
    # 'assets/green.png',
    # 'assets/blue.png',
    # 'assets/yellow.png',
    # 'assets/turquoise.png',
    # 'assets/orange.png',
    # 'assets/purple.png',
]


class MyPaintApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logical_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.pos_set = {(row, col) for row in range(9) for col in range(9)}
        self.spawn = True
        self.selected_image = None
        self.selected_button = None
        self.grid_layout = None
        self.button_layout = None
        self.path = []
        self.path_index = 0
        self.last_position = None
        self.score = 0

    def build_grid_layout(self):
        self.grid_layout = GridLayout(
            cols=9, rows=9, size_hint=(
                None, None,
            ), size=(555, 555), pos=(191, 48),
        )
        for row in range(9):
            for col in range(9):
                btn = Button(
                    background_normal='', background_color=BLACK,
                )
                btn.bind(
                    on_press=lambda tile,
                    x=row, y=col: self.on_button_press(tile, x, y),
                )
                self.grid_layout.add_widget(btn)
        return self.grid_layout

    def build_predicted_layout(self):
        self.button_layout = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(70, 300),
            pos=(55, 207),
            spacing=44,
        )
        for _ in range(3):
            img = Image(source=choice(IMAGE_LIST))
            img.bind(
                on_touch_down=lambda instance, touch:
                self.select_image(instance, touch),
            )
            self.button_layout.add_widget(img)
        return self.button_layout

    def on_button_press(self, tile, row, col):
        if tile.background_normal:
            self.select_button(tile, row, col)
            tile.background_color = [1, 1, 1, 1]
        elif not tile.background_normal and self.selected_image:
            self.move_selected_button(tile, row, col)

    def select_button(self, tile, row, col):
        self.selected_image = tile.background_normal
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
                last_button.background_normal = ''
                last_button.background_color = BLACK
            current_pos = self.path[self.path_index]
            row, col = current_pos
            button = self.grid_layout.children[
                9 * (8 - row) + (8 - col)
            ]
            button.background_normal = self.selected_image
            button.background_color = [1, 1, 1, 1]
            self.path_index += 1
        else:
            Clock.unschedule(self.update)
            start = self.selected_button[1], self.selected_button[2]
            self.update_logical_grid(self.path[-1][0], self.path[-1][1], start)
            if self.spawn:
                self.assign_random_images_to_buttons()
                adjacent_lines = self.find_adjacent_image(
                    self.path[-1][0], self.path[-1][1],
                )
                if adjacent_lines:
                    self.check_length_remove_square(adjacent_lines)

    def update_logical_grid(self, row, col, start):
        self.logical_grid[row][col] = 1
        self.pos_set.remove((row, col))
        self.selected_button[0].background_normal = ''
        self.selected_button[0].background_color = BLACK
        self.logical_grid[start[0]][start[1]] = 0
        self.pos_set.add((start[0], start[1]))
        self.selected_image = None
        self.selected_button = None

    def assign_random_images_to_buttons(self):
        if len(self.pos_set) < 3 or not self.spawn:
            return
        cords = choices(list(self.pos_set), k=3)
        images = [img.source for img in self.button_layout.children]
        for img in self.button_layout.children:
            img.source = choice(IMAGE_LIST)
        self.update_grid_with_new_images(cords, images)

    def update_grid_with_new_images(self, cords, images):
        for cord, image in zip(cords, images):
            row, col = cord
            button = self.grid_layout.children[9 * (8 - row) + (8 - col)]
            button.background_normal = image
            button.background_color = [1, 1, 1, 1]
            self.pos_set.remove(cord)
            self.logical_grid[cord[0]][cord[1]] = 1
            self.check_length_remove_square(self.find_adjacent_image(row, col))
            if len(self.pos_set) <= 0:
                print('Game Over')
                break

    def find_adjacent_image(self, row, col):
        directions = [
            (1, 0), (0, 1), (1, 1), (1, -1),
            (-1, 0), (0, -1), (-1, -1), (-1, 1),
        ]
        adjacent_lines = {
            0: [(row, col)],
            1: [(row, col)],
            2: [(row, col)],
            3: [(row, col)],
        }
        current_image = self.grid_layout.children[
            9 * (8 - row) + (8 - col)
        ].background_normal
        for i, direction in enumerate(directions):
            x, y = row, col
            dir_x, dir_y = direction
            while True:
                x += dir_x
                y += dir_y
                if 0 <= x < 9 and 0 <= y < 9:
                    adjacent_button = self.grid_layout.children[
                        9 * (8 - x) + (8 - y)
                    ]
                    adjacent_image = adjacent_button.background_normal
                    if adjacent_image == current_image:
                        adjacent_lines[i % 4].append((x, y))
                    else:
                        break
                else:
                    break
        return adjacent_lines

    def check_length_remove_square(self, lines):
        for line in lines.values():
            if len(line) >= 5:
                self.spawn = False
                line_score = len(line)
                self.score += line_score
                self.update_score_label()
                print('Spawn Flag Set to False')
                for x, y in line:
                    if 0 <= x < 9 and 0 <= y < 9:
                        button_index = 9 * (8 - x) + (8 - y)
                        if button_index < len(self.grid_layout.children):
                            self.grid_layout.children[
                                button_index
                            ].background_normal = ''
                            self.grid_layout.children[
                                button_index
                            ].background_color = BLACK
                            self.logical_grid[x][y] = 0
                            self.pos_set.add((x, y))
                        else:
                            print(f'Out of bounds ({x}, {y}) in grid_layout')
                    else:
                        print(f'Out of bounds ({x}, {y})')
                self.spawn = True
        print(f'score: {self.score}')

    def select_image(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.selected_image = instance.source
            return True
        return False

    def update_score_label(self):
        self.scorelb.text = ' '.join(list(f'{self.score:04d}'))

    def build(self):
        Window.size = (800, 800)
        Window.minimum_size = (400, 300)
        Window.maximum_size = (1000, 800)
        parent = FloatLayout()
        background = Image(
            source=BOARD, allow_stretch=True, keep_ratio=True,
        )
        parent.add_widget(background)
        parent.add_widget(self.build_grid_layout())
        parent.add_widget(self.build_predicted_layout())
        self.assign_random_images_to_buttons()
        self.scorelb = Label(
            text=' '.join(list(f'{self.score:04d}')),
            pos_hint={'x': 0.62, 'y': 0.85},
            size_hint=(None, None),
            size=(200, 50),
            font_size=sp(55),
            halign='center',
        )
        parent.add_widget(self.scorelb)
        return parent


if __name__ == '__main__':
    MyPaintApp().run()
