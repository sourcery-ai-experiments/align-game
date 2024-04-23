from __future__ import annotations

import random

import pygame


WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
OFFSET = 150
BLOCKSIZE = 50
BLACK = (0, 0, 0)
GREY = (160, 160, 160)
WHITE = (200, 200, 200)
GREEN = '#00A14B'
RED = '#ED1C24'
BLUE = '#21409A'
YELLOW = '#FFDE17'
PURPLE = '#7F3F98'
CYAN = '#009599'
PINK = (255, 153, 255)
BROWN = (255, 128, 0)
ORANGE = '#F26522'
colors = [GREEN, RED, BLUE, YELLOW, PURPLE, CYAN, ORANGE, BROWN]


def rand_color():
    return random.choice(colors)


def normalize_cords(x, y):
    x = x - (x % 50)
    y = y - (y % 50)
    return (x, y)


class AlignIt:
    def __init__(self):
        self.sqr_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.space = [[0 for _ in range(9)] for _ in range(9)]
        self.next_sqrs = []
        self.score = 0
        self.setup_game()
        self.main()

    def setup_game(self):
        global SCREEN, CLOCK
        SCREEN = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.NOFRAME,
        )

        CLOCK = pygame.time.Clock()
        SCREEN.fill(BLACK)
        self.draw_grid(True)
        self.draw_mini_grid(True)

    def draw_grid(self, new):
        if new:
            blocksize = BLOCKSIZE
            for row in range(9):
                for col in range(9):
                    rect = pygame.Rect(
                        col * blocksize + OFFSET,
                        row * blocksize + OFFSET,
                        blocksize,
                        blocksize,
                    )
                    pygame.draw.rect(SCREEN, WHITE, rect, 1)

    def draw_mini_grid(self, new):
        if new:
            blocksize = BLOCKSIZE
            for row in range(3):
                for col in range(1):
                    rect = pygame.Rect(
                        col * blocksize + 25,
                        row * blocksize + OFFSET,
                        blocksize,
                        blocksize,
                    )
                    pygame.draw.rect(SCREEN, WHITE, rect, 1)

    def main(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()
            CLOCK.tick(60)


if __name__ == '__main__':
    pygame.init()
    game = AlignIt()
