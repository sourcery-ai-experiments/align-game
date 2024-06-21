from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.metrics import sp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class ScoreManager:
    def __init__(self, game):
        self.score = 0
        self.game = game
        self.score_file = 'score.txt'

    def score_check_button(self):
        # TODO: CHANGE TO STAR when Kati provides the img
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
        scores = []

        with open(self.score_file) as file:
            lines = file.readlines()
            if len(lines) >= 5:
                scores = [int(score) for score in lines[4].strip().split(',')]
        if scores[0] == 0:
            print('no score yet')
            # if no file is found maybe we should, no highscores yet, get to aligning!
        if self.game.overlay is None:
            self.game.overlay = Widget()
            with self.game.overlay.canvas:
                Color(0, 0, 0, 0.5)
                self.game.background = Rectangle(
                    pos=self.game.root.pos,
                    size=self.game.root.size,
                )
            pos_text = (f'Position left: {len(self.game.pos_set)}')
            pos_label = Label(
                text=pos_text,
                font_size=40,
                color=[1, 1, 1, 1],
                pos=(self.game.root.width * 0.4, self.game.root.height * 0.1),
            )
            score_text = '\n'.join(
                f'{i + 1}. {score}' for i,
                score in enumerate(scores)
            )
            scores_label = Label(
                text=score_text,
                font_size=50,
                color=[1, 1, 1, 1],
                pos=(self.game.root.width * 0.4, self.game.root.height * 0.5),
            )
            self.game.overlay.add_widget(scores_label)
            self.game.overlay.add_widget(pos_label)
            self.game.root.add_widget(self.game.overlay)
            self.game.overlay.bind(on_touch_down=self.score_overlay_touch)

    def score_overlay_touch(self, touch, instance):
        self.game.root.remove_widget(self.game.overlay)
        self.game.overlay = None
        return True

    def update_score_label(self):
        self.game.scorelb.text = ' '.join(list(f'{self.score:04d}'))

    def create_score_label(self):
        return Label(
            text=' '.join(list(f'{self.score:04d}')),
            pos_hint={'x': 0.61 + 0.005, 'y': 0.85},
            size_hint=(None, None),
            size=(200, 50),
            font_size=sp(54),
            halign='center',
        )
