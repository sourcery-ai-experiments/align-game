from random import choice
from random import sample

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

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
        self.selected_color = None
        self.selected_button = None
        self.grid_layout = None

    def on_button_press(self, tile, row, col):
        print(row, col)
        if tile.background_color != [1, 1, 1, 1]:
            self.selected_color = tile.background_color
            self.selected_button = tile
            self.update_logical_grid(row, col, 0)
            print('colored')

        elif tile.background_color == [
            1, 1, 1, 1,
        ] and self.selected_color is not None:
            tile.background_color = self.selected_color
            self.update_logical_grid(row, col, 1)
            self.selected_button.background_color = [1, 1, 1, 1]
            self.selected_color = None
            self.selected_button = None
        print(self.logical_grid[0])

    def update_logical_grid(self, row, col, value):
        self.logical_grid[row][col] = value

    def assign_random_colors_to_buttons(self, buttons, colors):
        for btn, color in zip(buttons, colors):
            btn.background_color = color
            btn.logical_color = 1

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
        self.assign_random_colors_to_buttons(
            random_buttons, [btn.background_color for btn in left_buttons],
        )
        parent.add_widget(grid_layout)
        parent.add_widget(button_layout)
        return parent


if __name__ == '__main__':
    MyPaintApp().run()
