import os
from random import choice
from random import randrange

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.metrics import dp
from kivy.metrics import sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from astar import astar
UNIQUE_BUTT = 'assets/unique.png'
BLACK = [0, 0, 0, 0]
BOARD = 'assets/board.jpg'
IMAGE_LIST = [
    'assets/pink.png',
    'assets/green.png',
    'assets/blue.png',
    'assets/yellow.png',
    'assets/turquoise.png',
    'assets/orange.png',
    'assets/purple.png',
]


class MyPaintApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logical_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.pos_set = {(row, col) for row in range(9) for col in range(9)}
        self.spawn = False
        self.selected_image = None
        self.selected_button = None
        self.grid_layout = None
        self.button_layout = None
        self.path = []
        self.path_index = 0
        self.last_position = None
        self.score = 0
        self.overlay = None
        self.text_input = None
        self.score_rank = []
        self.load_game_state()

    def unique_button(self):
        """
        is selected img is unique.png than check_lenght,
        if lenght of 4 or more is of same color,
        unique = this color
        than remove squares of that color

        unique image should spawn less?
        """
        pass

    def load_game_state(self):
        file_path = os.path.join(os.getcwd(), 'score.txt')
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path) as file:
                lines = file.readlines()
                self.score = int(lines[0].strip())
                self.pos_set = eval(lines[1].strip())
                self.logical_grid = eval(lines[2].strip())
                self.image_grid = eval(lines[3].strip())
                self.score_rank = eval(lines[4].strip())

    def build_grid_layout(self):
        self.grid_layout = GridLayout(
            cols=9, rows=9,
            size_hint=(None, None),
            size=(dp(200), dp(300)),
            pos_hint={'center_x': 0.37 - 0.001, 'center_y': 0.56 + 0.001},
            spacing=dp(12),
        )
        for row in range(9):
            for col in range(9):
                btn = self.create_grid_button(row, col)
                self.grid_layout.add_widget(btn)
        return self.grid_layout

    def create_grid_button(self, row, col):
        btn = Button(
            background_normal='', background_color=BLACK,
            size_hint=(None, None), size=(dp(50), dp(50)),
        )
        btn.background_disabled_normal = btn.background_normal
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

    def score_check_button(self):
        img_source = 'assets/unique.png'
        self.sc_button = Button(
            background_normal=img_source,
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={'x': 0.84, 'y': 0.91},
        )
        self.sc_button.bind(on_press=self.score_check)
        return self.sc_button

    def score_check(self, _):
        file_path = os.path.join(os.getcwd(), 'score.txt')
        scores = []
        if os.path.exists(file_path):
            with open(file_path) as file:
                lines = file.readlines()
                if len(lines) >= 5:
                    scores = [
                        int(score) for score in lines[4].strip().split(',')
                    ]
        if self.overlay is None:
            self.overlay = Widget()
            with self.overlay.canvas:
                Color(0, 0, 0, 0.5)
                self.background = Rectangle(
                    pos=self.root.pos,
                    size=self.root.size,
                )

            pos_text = '\n'.join(
                [
                    f'Position left: {len(self.pos_set)}',
                ],
            )
            pos_label = Label(
                text=pos_text,
                font_size=40,
                color=[1, 1, 1, 1],
                pos=(self.root.width * 0.4, self.root.height * 0.1),
            )
            score_text = '\n'.join(
                [
                    f'{i + 1}. {score}' for i,
                    score in enumerate(scores)
                ],
            )
            scores_label = Label(
                text=score_text,
                font_size=50,
                color=[1, 1, 1, 1],
                pos=(self.root.width * 0.4, self.root.height * 0.5),
            )
            self.overlay.add_widget(scores_label)
            self.overlay.add_widget(pos_label)
            self.root.add_widget(self.overlay)
            self.overlay.bind(on_touch_down=self.score_overlay_touch)

    def score_overlay_touch(self, instance, touch):
        self.root.remove_widget(self.overlay)
        self.overlay = None
        return True

    def saveexit_button(self):
        img_source = 'assets/unique.png'
        self.save_exit_button = Button(
            background_normal=img_source,
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={'x': 0.2, 'y': 0.91},
        )
        self.save_exit_button.bind(on_press=self.save_and_exit)
        return self.save_exit_button

    def save_and_exit(self, _):
        self.score_current = str(self.score)
        self.pos = str(self.pos_set)
        self.logrid = str(self.logical_grid)
        self.image_grid = [
            [
                self.get_button_at(
                    row, col,
                ).background_normal for col in range(9)
            ]
            for row in range(9)
        ]
        image_grid_str = str(self.image_grid)
        file_path = os.path.join(os.getcwd(), 'score.txt')
        existing_scores = []
        if os.path.exists(file_path):
            with open(file_path) as file:
                lines = file.readlines()
                if len(lines) >= 5:
                    existing_scores = [
                        int(score) for score in lines[4].strip().split(',')
                    ]
                else:
                    existing_scores = self.score_rank if self.score_rank else [
                        0,
                    ]
        else:
            lines = []
            existing_scores = self.score_rank if self.score_rank else [0]
        if not isinstance(self.score_rank, list):
            self.score_rank = []
        combined_scores = existing_scores + self.score_rank
        combined_scores = sorted(set(combined_scores), reverse=True)[:5]
        updated_lines = [
            self.score_current + '\n',
            self.pos + '\n',
            self.logrid + '\n',
            image_grid_str + '\n',
            f"{','.join(map(str, combined_scores))}\n",
        ]
        while len(lines) < 4:
            lines.append('\n')
        lines[:5] = updated_lines
        with open(file_path, 'w') as file:
            file.writelines(lines)
        self.stop()

    def reset_button(self):
        img_source = 'assets/unique.png'
        self.reset = Button(
            background_normal=img_source,
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={'x': 0.1, 'y': 0.91},
        )
        self.reset.bind(on_press=self.to_reset)
        return self.reset

    def to_reset(self, _):
        self.logical_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.pos_set = {(row, col) for row in range(9) for col in range(9)}
        self.clear_grid_layout()
        self.assign_random_images_to_buttons()
        self.update_button_layout_images()
        self.score = 0
        self.update_score_label()
        self.clear_selected_buttons()

    def clear_grid_layout(self):
        for child in self.grid_layout.children:
            child.background_normal = ''
            child.background_color = BLACK

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
            print('-----------')
        print(len(self.pos_set))

    def select_button(self, tile, row, col):
        self.selected_image = tile.background_normal
        self.selected_button = (tile, row, col)
        self.spawn = True
        if len(self.pos_set) == 0:
            self.gameover()

    def move_selected_button(self, tile, row, col):
        self.disable_grid_buttons()
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
            if self.spawn:
                self.assign_random_images_to_buttons()

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
        # self.selected_image = button.background_normal
        # # tried to keep img while moving but it dosnt work
        button.background_normal = self.selected_image
        button.background_color = [1, 1, 1, 1]

    def handle_reached_destination(self):
        start = self.selected_button[1], self.selected_button[2]
        self.update_logical_grid(self.path[-1][0], self.path[-1][1], start)
        adjacent_lines = self.find_adjacent_image(
            self.path[-1][0],
            self.path[-1][1],
        )
        if adjacent_lines:
            self.check_length_remove_square(adjacent_lines)
        self.enable_grid_buttons()

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
        # self.enable_grid_buttons()

    def assign_random_images_to_buttons(self):
        if len(self.pos_set) < 3:
            images = [img.source for img in self.button_layout.children]
            self.update_grid_with_new_images(
                self.get_unique_random_cords(len(self.pos_set)), images,
            )
        cords = self.get_unique_random_cords(3)
        images = [img.source for img in self.button_layout.children]
        self.update_button_layout_images()
        self.update_grid_with_new_images(cords, images)

    def gameover(self):
        print('Game Over')
        file_path = os.path.join(os.getcwd(), 'score.txt')
        scores = []
        if os.path.exists(file_path):
            with open(file_path) as file:
                lines = file.readlines()
                if len(lines) >= 5:
                    scores = [
                        int(score) for score in lines[4].strip().split(',')
                    ]
        if not isinstance(self.score_rank, list):
            self.score_rank = []
        self.score_rank.append(self.score)
        current_score = self.score
        if len(scores) < 5:
            scores.append(current_score)
        else:
            min_score = min(scores)
            if current_score > min_score:
                scores[scores.index(min_score)] = current_score
        scores = sorted(scores, reverse=True)[:5]
        if len(lines) >= 5:
            with open(file_path, 'w') as file:
                lines = lines[:4]
                lines.append(','.join(map(str, scores)) + '\n')
                file.writelines(lines)
        self.clear_selected_buttons()
        self.disable_grid_buttons()
        if self.overlay is None:
            self.overlay = Widget()
            with self.overlay.canvas:
                Color(0, 0, 0, 0.5)
                self.background = Rectangle(
                    pos=self.root.pos,
                    size=self.root.size,
                )
            self.root.add_widget(self.overlay)
            game_over_label = Label(
                text=f'Game Over\nScore: {self.score}',
                font_size=30,
                color=[1, 1, 1, 1],
                pos=(self.root.width * 0.5, self.root.height * 0.5),
            )
            self.overlay.add_widget(game_over_label)
            self.overlay.bind(on_touch_down=self.on_overlay_touch)

    def clear_selected_buttons(self):
        for child in self.grid_layout.children:
            if isinstance(child, Button) and child.state == 'down':
                child.state = 'normal'

    def disable_grid_buttons(self):
        for child in self.grid_layout.children:
            if isinstance(child, Button):
                child.disabled = True
                child.background_disabled_normal = child.background_normal

    def enable_grid_buttons(self):
        for child in self.grid_layout.children:
            if isinstance(child, Button):
                child.disabled = False
                child.background_disabled_normal = child.background_normal

    def on_overlay_touch(self, instance, touch):
        self.root.remove_widget(self.overlay)
        self.overlay = None
        self.clear_selected_buttons()
        self.enable_grid_buttons()
        self.to_reset(None)

    def get_unique_random_cords(self, count):
        pos_list = list(self.pos_set)
        cords = []
        while len(cords) < count and pos_list:
            index = randrange(len(pos_list))
            new_cord = pos_list[index]
            cords.append(new_cord)
            pos_list.pop(index)
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
            # if len(self.pos_set) <= 0:
            #     print('Game Over')
            #     break

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
        parent.add_widget(self.score_check_button())
        parent.add_widget(self.saveexit_button())
        parent.add_widget(self.reset_button())
        self.scorelb = self.create_score_label()
        parent.add_widget(self.scorelb)
        # self.assign_random_images_to_buttons()
        self.apply_game_state()
        return parent

    def apply_game_state(self):
        self.update_score_label()
        for row in range(9):
            for col in range(9):
                if self.logical_grid[row][col] == 1:
                    button = self.get_button_at(row, col)
                    button.background_normal = self.image_grid[row][col]
                    button.background_color = [1, 1, 1, 1]
                    self.pos_set.discard((row, col))

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
