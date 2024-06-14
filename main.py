from random import choice

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
            cols=9, rows=9,
            size_hint=(None, None),
            size=(555, 555), pos=(191, 49),
        )
        for row in range(9):
            for col in range(9):
                btn = self.create_grid_button(row, col)
                self.grid_layout.add_widget(btn)
        return self.grid_layout

    def create_grid_button(self, row, col):
        btn = Button(background_normal='', background_color=BLACK)
        btn.bind(
            on_press=lambda tile,
            x=row, y=col: self.on_button_press(tile, x, y),
        )
        return btn

    def build_predicted_layout(self):
        self.button_layout = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(70, 300),
            pos=(55, 207),
            spacing=44,
        )
        for _ in range(3):
            img = self.create_image_widget()
            self.button_layout.add_widget(img)
        return self.button_layout

    def create_image_widget(self):
        img = Image(source=choice(IMAGE_LIST))
        img.bind(
            on_touch_down=lambda instance,
            touch: self.select_image(instance, touch),
        )
        return img

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
            self.move_along_path()
        else:
            Clock.unschedule(self.update)
            self.handle_reached_destination()

    def move_along_path(self):
        if self.path_index > 0:
            self.clear_last_button()
        current_pos = self.path[self.path_index]
        self.update_current_button(current_pos)
        self.path_index += 1

    def clear_last_button(self):
        last_row, last_col = self.path[self.path_index - 1]
        last_button = self.get_button_at(last_row, last_col)
        last_button.background_normal = ''
        last_button.background_color = BLACK

    def update_current_button(self, current_pos):
        row, col = current_pos
        button = self.get_button_at(row, col)
        button.background_normal = self.selected_image
        button.background_color = [1, 1, 1, 1]

    def handle_reached_destination(self):
        start = self.selected_button[1], self.selected_button[2]
        self.update_logical_grid(self.path[-1][0], self.path[-1][1], start)
        if self.spawn:
            self.assign_random_images_to_buttons()
            adjacent_lines = self.find_adjacent_image(
                self.path[-1][0],
                self.path[-1][1],
            )
            if not adjacent_lines:
                self.assign_random_images_to_buttons()
            elif adjacent_lines:
                self.check_length_remove_square(adjacent_lines)

    def get_button_at(self, row, col):
        return self.grid_layout.children[9 * (8 - row) + (8 - col)]

    def update_logical_grid(self, row, col, start):
        self.logical_grid[row][col] = 1
        self.pos_set.remove((row, col))
        self.clear_selected_button(start)
        self.selected_image = None
        self.selected_button = None

    def clear_selected_button(self, start):
        self.selected_button[0].background_normal = ''
        self.selected_button[0].background_color = BLACK
        self.logical_grid[start[0]][start[1]] = 0
        self.pos_set.add((start[0], start[1]))

    def assign_random_images_to_buttons(self):
        if len(self.pos_set) < 3 or not self.spawn:
            return
        cords = self.get_unique_random_cords(3)
        images = [img.source for img in self.button_layout.children]
        self.update_button_layout_images()
        self.update_grid_with_new_images(cords, images)

    def get_unique_random_cords(self, count):
        cords = []
        while len(cords) < count:
            new_cord = choice(list(self.pos_set))
            if new_cord not in cords:
                cords.append(new_cord)
        return cords

    def update_button_layout_images(self):
        for img in self.button_layout.children:
            img.source = choice(IMAGE_LIST)

    def update_grid_with_new_images(self, cords, images):
        for cord, image in zip(cords, images):
            row, col = cord
            button = self.get_button_at(row, col)
            button.background_normal = image
            button.background_color = [1, 1, 1, 1]
            self.pos_set.remove(cord)
            self.logical_grid[cord[0]][cord[1]] = 1
            self.check_length_remove_square(
                self.find_adjacent_image(row, col),
            )
            if len(self.pos_set) <= 0:
                print('Game Over')
                break

    def find_adjacent_image(self, row, col):
        directions = [
            (1, 0), (0, 1), (1, 1), (1, -1),
            (-1, 0), (0, -1), (-1, -1), (-1, 1),
        ]
        adjacent_lines = {i: [(row, col)] for i in range(4)}
        current_image = self.get_button_at(row, col).background_normal
        for i, direction in enumerate(directions):
            self.find_line_in_direction(
                adjacent_lines, i,
                direction, row, col,
                current_image,
            )
        return adjacent_lines

    def find_line_in_direction(
            self, adjacent_lines, i,
            direction, row, col, current_image,
    ):
        x, y = row, col
        dir_x, dir_y = direction
        while True:
            x += dir_x
            y += dir_y
            if not self.is_within_bounds(x, y):
                break
            adjacent_button = self.get_button_at(x, y)
            adjacent_image = adjacent_button.background_normal
            if adjacent_image == current_image:
                adjacent_lines[i % 4].append((x, y))
            else:
                break

    def is_within_bounds(self, x, y):
        return 0 <= x < 9 and 0 <= y < 9

    def check_length_remove_square(self, lines):
        variable = len(self.pos_set)
        for line in lines.values():
            if len(line) >= 5:
                self.spawn = False
                self.remove_line(line)
        # self.spawn = True

        self.score += (len(self.pos_set) - variable)
        self.update_score_label()

    def remove_line(self, line):
        for x, y in line:
            if self.is_within_bounds(x, y):
                button_index = 9 * (8 - x) + (8 - y)
                if button_index < len(self.grid_layout.children):
                    self.clear_button(x, y)
                else:
                    print(f'Out of bounds ({x}, {y}) in grid_layout')
            else:
                print(f'Out of bounds ({x}, {y})')

    def clear_button(self, x, y):
        self.grid_layout.children[
            9 * (8 - x) + (8 - y)
        ].background_normal = ''
        self.grid_layout.children[
            9 * (8 - x) + (8 - y)
        ].background_color = BLACK
        self.logical_grid[x][y] = 0
        self.pos_set.add((x, y))

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
        parent.add_widget(self.create_background())
        parent.add_widget(self.build_grid_layout())
        parent.add_widget(self.build_predicted_layout())
        self.scorelb = self.create_score_label()
        parent.add_widget(self.scorelb)
        self.assign_random_images_to_buttons()
        return parent

    def create_background(self):
        return Image(source=BOARD, allow_stretch=True, keep_ratio=True)

    def create_score_label(self):
        return Label(
            text=' '.join(list(f'{self.score:04d}')),
            pos_hint={'x': 0.61 + 0.005, 'y': 0.85},
            size_hint=(None, None),
            size=(200, 50),
            font_size=sp(54),
            halign='center',
        )


if __name__ == '__main__':
    MyPaintApp().run()
