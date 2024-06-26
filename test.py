from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout

BOARD = 'assets/board.jpg'


class MyPaintApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logical_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.pos_set = {(row, col) for row in range(9) for col in range(9)}
        self.selected_button = None
        self.grid_layout = None
        self.button_layout = None

    def build_grid_layout(self):
        self.grid_layout = GridLayout(
            cols=9, rows=9,
            size_hint=(1.0, 1.0),
            spacing=12,
        )
        for row in range(9):
            for col in range(9):
                btn = self.create_grid_button(row, col)
                self.grid_layout.add_widget(btn)
        return self.grid_layout

    def create_grid_button(self, row, col):
        btn = Button(
            background_normal='', background_color=[1, 1, 1, 1],
            size_hint=(50.0, 50.0),
        )
        btn.background_disabled_normal = btn.background_normal
        btn.bind(
            on_press=lambda tile, x=row, y=col: self.on_button_press(
                tile, x, y,
            ),
        )
        return btn

    def build_predicted_layout(self):
        self.button_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.37, 1.0),
        )
        for _ in range(3):
            btn = Button(
                text='Predicted',
                size_hint=(1, 0.3),
                # Green background for visualization
                background_color=[0, 1, 0, 0.3],
            )
            self.button_layout.add_widget(btn)
        return self.button_layout

    def build_right_layout(self):
        self.button_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.12, 1.0),
        )
        for _ in range(1):
            btn = Button(
                text='Right',
                size_hint=(1, 0.1),
                # Blue background for visualization
                background_color=[0, 0, 1, 0.3],
            )
            self.button_layout.add_widget(btn)
        return self.button_layout

    def build_top_layout(self):
        self.button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1.0, 0.38),
        )
        for _ in range(1):
            btn = Button(
                text='Top',
                size_hint=(0.3, 1),
                # Yellow background for visualization
                background_color=[1, 1, 0, 0.3],
            )
            self.button_layout.add_widget(btn)
        return self.button_layout

    def build_bottom_layout(self):
        self.button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1.0, 0.11),
        )
        for _ in range(1):
            btn = Button(
                text='Bottom',
                size_hint=(0.3, 1),
                # Magenta background for visualization
                background_color=[1, 0, 1, 0.5],
            )
            self.button_layout.add_widget(btn)
        return self.button_layout

    def on_button_press(self, tile, x, y):
        print(f'Button at ({x}, {y}) pressed')

    def build(self):
        parent = RelativeLayout()

        parent.add_widget(Image(source=BOARD, fit_mode='contain'))

        # Create a main BoxLayout to hold all other layouts
        main_layout = BoxLayout(orientation='vertical')

        # Add top layout
        top_layout = self.build_top_layout()
        main_layout.add_widget(top_layout)

        # Create a middle BoxLayout to hold grid and side layouts
        middle_layout = BoxLayout(orientation='horizontal')

        # Add predicted layout
        predicted_layout = self.build_predicted_layout()
        middle_layout.add_widget(predicted_layout)

        # Add grid layout
        grid_layout = self.build_grid_layout()
        middle_layout.add_widget(grid_layout)

        # Add right layout
        right_layout = self.build_right_layout()
        middle_layout.add_widget(right_layout)

        # Add middle layout to main layout
        main_layout.add_widget(middle_layout)

        # Add bottom layout
        bottom_layout = self.build_bottom_layout()
        main_layout.add_widget(bottom_layout)

        # Add main layout to parent
        parent.add_widget(main_layout)

        return parent


if __name__ == '__main__':
    MyPaintApp().run()
