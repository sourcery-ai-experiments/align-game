import os

from kivy.uix.button import Button


class FuncManager:
    def __init__(self, game) -> None:
        self.game = game
        self.score_file = 'score.txt'

    def load_game_state(self):
        if os.path.exists('score.txt'):
            with open('score.txt') as file:
                lines = file.readlines()
                self.game.score_manager.score = int(lines[0].strip())
                self.game.pos_set = eval(lines[1].strip())
                self.game.logical_grid = eval(lines[2].strip())
                self.game.image_grid = eval(lines[3].strip())
                self.game.score_rank = eval(lines[4].strip())

    def apply_game_state(self):
        self.game.score_manager.update_score_label()
        for row in range(9):
            for col in range(9):
                if self.game.logical_grid[row][col] == 1:
                    button = self.game.get_button_at(row, col)
                    button.background_normal = self.game.image_grid[row][col]
                    button.background_color = [1, 1, 1, 1]
                    self.game.pos_set.discard((row, col))

    def create_save_exit_button(self):
        # TODO: change to img when Kati gives it.
        img_source = 'assets/unique.png'
        save_exit_button = Button(
            background_normal=img_source,
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={'x': 0.2, 'y': 0.91},
        )
        save_exit_button.bind(on_press=self.save_and_exit)
        return save_exit_button

    def save_and_exit(self, _):
        score_current = str(self.game.score_manager.score)
        pos = str(self.game.pos_set)
        logrid = str(self.game.logical_grid)
        image_grid = [
            [
                self.game.get_button_at(
                    row, col,
                ).background_normal for col in range(9)
            ]
            for row in range(9)
        ]
        image_grid_str = str(image_grid)
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
                    # TODO: figureout a better name for score_rank and where it should be
                    existing_scores = self.game.score_rank if self.game.score_rank else [
                        0,
                    ]
        else:
            lines = []
            existing_scores = self.game.score_rank if self.game.score_rank else [
                0,
            ]
        if not isinstance(self.game.score_rank, list):
            self.game.score_rank = []
        combined_scores = existing_scores + self.game.score_rank
        combined_scores = sorted(set(combined_scores), reverse=True)[:5]
        updated_lines = [
            score_current + '\n',
            pos + '\n',
            logrid + '\n',
            image_grid_str + '\n',
            f"{','.join(map(str, combined_scores))}\n",
        ]
        while len(lines) < 4:
            lines.append('\n')
        lines[:5] = updated_lines
        with open(file_path, 'w') as file:
            file.writelines(lines)
        self.game.stop()

    def reset_button(self):
        # TODO: set the proper image as the rest
        img_source = 'assets/unique.png'
        reset = Button(
            background_normal=img_source,
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={'x': 0.1, 'y': 0.91},
        )
        reset.bind(on_press=self.to_reset)
        return reset

    def to_reset(self, _):
        self.game.logical_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.game.pos_set = {(row, col) for row in range(9)
                             for col in range(9)}
        self.game.clear_grid_layout()
        self.game.assign_random_images_to_buttons()
        self.game.update_button_layout_images()
        self.game.score_manager.score = 0
        self.game.score_manager.update_score_label()
        self.game.clear_selected_buttons()
