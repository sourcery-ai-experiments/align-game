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

    def on_button_press(self, instance, row, col):
        print(row, col)
        if instance.background_color != [1, 1, 1, 1]:
            print('colored')

    def assign_random_colors_to_buttons(self, buttons, colors):
        for btn, color in zip(buttons, colors):
            btn.background_color = color

    def build_grid_layout(self):
        grid_layout = GridLayout(
            cols=9, rows=9,
            size_hint=(None, None),
            size=(450, 450), pos=(330, 20),
        )
        for row in range(9):
            for col in range(9):
                btn = Button()
                btn.bind(
                    on_press=lambda instance, x=row,
                    y=col: self.on_button_press(instance, x, y),
                )
                grid_layout.add_widget(btn)
        return grid_layout

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
