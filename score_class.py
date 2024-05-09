import datetime

import pygame

WHITE = (200, 200, 200)
BLACK = (0, 0, 0)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class SCORE:

    def save_score(
            self, name,
            moves_made,
            scoreall,
            space,
            sqr_grid,
            future_sqr_cord_color,
    ):
        t = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        current_time = t
        with open('score.txt', 'a') as file:
            file.write('------------------------------ \n')
            file.write(f'your name: {name} \n')
            file.write(f'moves made: {moves_made} \n')
            file.write(f'date: {current_time} \n')
            file.write(f'{str(scoreall)} \n')
            file.write(str(space) + '\n')
            file.write(str(sqr_grid) + '\n')
            file.write(f'{str(future_sqr_cord_color),} \n')

    def score(self):
        img = self.text_font.render(f'score: {self.scoreall}', True, WHITE)
        SCREEN.fill(BLACK, (470, 10, 130, 30))
        SCREEN.blit(img, (470, 10))
