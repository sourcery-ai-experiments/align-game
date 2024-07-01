import os
from random import choice
from random import randrange

from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget

from astar import astar
from save_load_exit import FuncManager
from score_manager import ScoreManager
UNIQUE_BUTT = 'assets/crown.png'
BLACK = [0, 0, 0, 0]
BOARD = 'assets/board.jpg'
IMAGE_LIST = [
    'assets/pink.png',
    'assets/green.png',
    # 'assets/blue.png',
    # 'assets/yellow.png',
    # 'assets/turquoise.png',
    # 'assets/orange.png',
    # 'assets/purple.png',
    UNIQUE_BUTT,
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
        self.overlay = None
        self.text_input = None
        self.scorelb = None
        self.score_top_five = []
        self.score_manager = ScoreManager(self)
        self.func_manager = FuncManager(self)
        self.func_manager.load_game_state()
        self.no_path_sound = SoundLoader.load('assets/no path.wav')
        self.is_moving = False

        self.right_wide = 0.11
        self.left_wide = 0.36
        self.top_height = 0.77
        self.bottom_height = 0.50

        # scaling for tablet 1200x2000
        # self.right_wide = 0.11
        # self.left_wide = 0.36
        # self.top_height = 0.83
        # self.bottom_height = 0.55

        # phone scaling
        # self.right_wide = 0.11
        # self.left_wide = 0.36
        # self.top_height = 1.267
        # self.bottom_height = 1.0

    # algorytm for dynamic scaling
    # def window_size(self, instance, width, height):
    #     if width > height:
    #         diff = width - height
    #         self.right_wide += diff / 1000
    #         self.left_wide += diff / 1000
    #     if height > width:
    #         diff = height - width
    #         self.top_height += diff / 1000
    #         self.bottom_height += diff / 1000

    def build_grid_layout(self):
        self.grid_layout = GridLayout(
            cols=9, rows=9,
            size_hint=(1.0, 1.0),
            spacing=16,
        )
        for row in range(9):
            for col in range(9):
                btn = self.create_grid_button(row, col)
                self.grid_layout.add_widget(btn)
        return self.grid_layout

    def create_grid_button(self, row, col):
        btn = Button(
            background_normal='', background_color=BLACK,
            size_hint=(45.0, 45.0),
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
            size_hint=(self.left_wide, 1.0),
            spacing=95,
            padding=(50, 238),
        )
        for _ in range(3):
            img = self.create_image_widget()
            self.button_layout.add_widget(img)
        return self.button_layout

    def build_placeholder_layout(self, orientation, size_hint):
        return BoxLayout(
            orientation=orientation,
            size_hint=size_hint,
        )

    def clear_grid_layout(self):
        for child in self.grid_layout.children:
            child.background_normal = ''
            child.background_color = BLACK

    def create_image_widget(self):
        img = Image(
            source=choice(IMAGE_LIST),
            size_hint=(None, None),
            size=(80, 80),
        )
        img.pos_hint = {'center_x': 0.44, 'y': 0.99}
        img.allow_stretch = True
        img.keep_ratio = False
        img.bind(
            on_touch_down=lambda instance,
            touch: self.select_image(instance, touch),
        )
        return img

    def on_button_press(self, tile, row, col):
        if self.is_moving:
            return
        if tile.background_normal:
            self.select_button(tile, row, col)
            tile.background_color = [1, 1, 1, 1]
        elif not tile.background_normal and self.selected_image:
            self.move_selected_button(tile, row, col)

    def select_button(self, tile, row, col):
        self.selected_image = tile.background_normal
        self.selected_button = (tile, row, col)
        self.spawn = True

    def move_selected_button(self, tile, row, col):
        if self.selected_button is None:
            return
        self.is_moving = True
        start = (self.selected_button[1], self.selected_button[2])
        end = (row, col)
        path = astar(self.logical_grid, start, end)
        if not path:
            self.show_no_path_overlay()
            print('no path')
            self.is_moving = False
            return
        self.path = path
        self.path_index = 0
        self.last_position = start
        Clock.schedule_interval(self.update, 0.1)

    def show_no_path_overlay(self):
        self.overlay = Widget()
        with self.overlay.canvas:
            Color(0, 0, 0, 0)
            self.background = Rectangle(
                pos=self.root.pos,
                size=self.root.size,
            )
        self.root.add_widget(self.overlay)
        no_path_label = Label(
            text='No Path Found',
            font_size=35,
            color=[1, 1, 1, 1],
            pos=(self.root.width * 0.5, self.root.height * 0.75),
            halign='center',
            valign='middle',
        )
        no_path_label.bind(size=no_path_label.setter('text_size'))
        self.overlay.add_widget(no_path_label)
        if self.no_path_sound:
            self.no_path_sound.play()
        self.overlay.bind(
            on_touch_down=lambda instance,
            touch: self.remove_overlay(instance, touch),
        )

    def remove_overlay(self, instance, touch):
        if self.overlay:
            self.root.remove_widget(self.overlay)
            self.overlay = None
            self.enable_grid_buttons()

    def update(self, dt):
        if self.path_index < len(self.path):
            self.move_along_path()
        else:
            Clock.unschedule(self.update)
            self.handle_reached_destination()
            if self.spawn:
                self.assign_random_images_to_buttons()
                if len(self.pos_set) == 0:
                    self.gameover()

    def move_along_path(self):
        if self.path_index > 0:
            self.clear_last_button()
        current_pos = self.path[self.path_index]
        self.update_current_button(current_pos)
        self.path_index += 1

    def update_current_button(self, current_pos):
        row, col = current_pos
        button = self.get_button_at(row, col)
        button.background_normal = self.selected_image
        button.background_color = [1, 1, 1, 1]

    def clear_last_button(self):
        last_row, last_col = self.path[self.path_index - 1]
        last_button = self.get_button_at(last_row, last_col)
        last_button.background_normal = ''
        last_button.background_color = BLACK

    def handle_reached_destination(self):
        start = self.selected_button[1], self.selected_button[2]
        self.update_logical_grid(self.path[-1][0], self.path[-1][1], start)
        adjacent_lines = self.find_adjacent_lines(
            self.path[-1][0],
            self.path[-1][1],
        )
        if adjacent_lines:
            self.check_length_remove_square(adjacent_lines)
        self.enable_grid_buttons()
        self.is_moving = False

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
        if not isinstance(self.score_top_five, list):
            self.score_top_five = []
        self.score_top_five.append(self.score_manager.score)
        current_score = self.score_manager.score
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
                text=f'Game Over\nScore: {self.score_manager.score}',
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
        self.func_manager.to_reset(None)

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
                self.find_adjacent_lines(row, col),
            )

    def find_adjacent_lines(self, row, col):
        directions = [
            (1, 0), (0, 1), (1, 1), (1, -1),
            (-1, 0), (0, -1), (-1, -1), (-1, 1),
        ]
        current_image = self.get_button_at(row, col).background_normal
        adjacent_lines = {i: {(row, col)} for i in range(4)}
        for i, direction in enumerate(directions):
            self.find_line_in_direction(
                adjacent_lines[i % 4],
                direction, row, col,
                current_image,
            )
        return adjacent_lines

    def find_line_in_direction(
            self,
            current_line,
            direction,
            row, col,
            current_image,
    ):
        x, y = row, col
        dir_x, dir_y = direction
        previous_image = None
        while True:
            x += dir_x
            y += dir_y
            if not self.is_within_bounds(x, y):
                break
            adjacent_button = self.get_button_at(x, y)
            adjacent_image = adjacent_button.background_normal
            if adjacent_image == '':
                break
            # every line has one color, that is the first not unique
            if not previous_image and adjacent_image != UNIQUE_BUTT:
                previous_image = adjacent_image

            if previous_image and adjacent_image not in (previous_image, UNIQUE_BUTT):
                break
            # if the color is the same as the one we are looking for
            if adjacent_image in (current_image, UNIQUE_BUTT):
                current_line.add((x, y))
                print('only color and unique or one color on line')
            # if the color is unique but the adjacent is not
            elif current_image == UNIQUE_BUTT and adjacent_image == 'assets/green.png':
                current_line.add((x, y))  # problem potentioly here
                print('bbut is unique  but adjacent is not')

    def is_within_bounds(self, x, y):
        return 0 <= x < 9 and 0 <= y < 9

    def check_length_remove_square(self, lines):
        variable = len(self.pos_set)
        for line in lines.values():
            if len(line) >= 5:
                self.spawn = False
                self.remove_line(line)
        self.score_manager.score += (len(self.pos_set) - variable)
        self.score_manager.update_score_label()

    def remove_line(self, line):
        for x, y in line:
            if self.is_within_bounds(x, y):
                button_index = 9 * (8 - x) + (8 - y)
                if button_index < len(self.grid_layout.children):
                    self.clear_button(x, y)

    def clear_button(self, x, y):
        self.get_button_at(x, y).background_normal = ''
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

    def build(self):
        Window.size = (1200, 1850)
        parent = RelativeLayout()
        parent.add_widget(Image(source=BOARD, fit_mode='contain'))

        main_layout = BoxLayout(orientation='vertical')

        top_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1.0, self.top_height),
            padding=(5, 5),
            spacing=40,
        )

        reset_button = self.func_manager.reset_button()
        save_exit_button = self.func_manager.create_save_exit_button()
        score_check_button = self.score_manager.score_check_button()
        self.scorelb = self.score_manager.create_score_label()

        reset_button.size_hint = (None, None)
        reset_button.size = (80, 80)
        reset_button.pos_hint = {'center_y': 0.36}

        save_exit_button.size_hint = (None, None)
        save_exit_button.size = (80, 80)
        save_exit_button.pos_hint = {'center_y': 0.36}

        self.scorelb.size_hint = (None, None)
        self.scorelb.size = (100, 100)
        self.scorelb.pos_hint = {'center_y': 0.25}

        score_check_button.size_hint = (None, None)
        score_check_button.size = (80, 80)
        score_check_button.pos_hint = {'center_y': 0.36}

        top_layout.add_widget(
            Widget(size_hint=(None, None), size=(Window.width * 0.02, 1)),
        )
        top_layout.add_widget(reset_button)
        top_layout.add_widget(save_exit_button)
        top_layout.add_widget(
            Widget(size_hint=(None, None), size=(Window.width * 0.405, 1)),
        )
        top_layout.add_widget(self.scorelb)
        top_layout.add_widget(
            Widget(size_hint=(None, None), size=(Window.width * 0.0, 1)),
        )
        top_layout.add_widget(score_check_button)

        main_layout.add_widget(top_layout)

        middle_layout = BoxLayout(orientation='horizontal')
        predicted_layout = self.build_predicted_layout()
        middle_layout.add_widget(predicted_layout)
        grid_layout = self.build_grid_layout()
        middle_layout.add_widget(grid_layout)
        right_layout = self.build_placeholder_layout(
            'horizontal', (self.right_wide, 1.0),
        )
        middle_layout.add_widget(right_layout)

        main_layout.add_widget(middle_layout)

        bottom_layout = self.build_placeholder_layout(
            'horizontal', (1.0, self.bottom_height),
        )
        main_layout.add_widget(bottom_layout)

        parent.add_widget(main_layout)

        self.func_manager.apply_game_state()
        if self.logical_grid == [[0 for _ in range(9)] for _ in range(9)]:
            self.assign_random_images_to_buttons()
        return parent


if __name__ == '__main__':
    MyPaintApp().run()
