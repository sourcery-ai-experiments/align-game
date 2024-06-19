import os

from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class ScoreManager:
    def __init__(self):
        self.score = 0
        self.score_rank = []

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
        # if self.overlay is None:
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

    def score_overlay_touch(self):
        self.root.remove_widget(self.overlay)
        self.overlay = None
        return True

    # def update_score_label(self, scorelb):
    #     scorelb.text = ' '.join(list(f'{self.score:04d}'))

    # def create_score_label(self):
    #     return Label(
    #         text=' '.join(list(f'{self.score:04d}')),
    #         pos_hint={'x': 0.61 + 0.005, 'y': 0.85},
    #         size_hint=(None, None),
    #         size=(200, 50),
    #         font_size=sp(54),
    #         halign='center',
    #     )
