from __future__ import annotations

import random
import sys
from time import sleep

import pygame

from astar import astar
from coloredRect import ColoredRect


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
        self.main()

    def setup_game(self, next_colors):
        global SCREEN, CLOCK   # makes them global
        pygame.init()             # initialise pygame
        # pygame.mixer.music.pause()
        SCREEN = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
        )  # declare space
        CLOCK = pygame.time.Clock()           # framerate
        SCREEN.fill(BLACK)  # background
        self.draw_future_grid(next_colors)       # 3 future colors
        self.draw_grid(True)                      # draws grid

    def main(self):
        next_colors = [
            rand_color()
            for _ in range(3)
        ]   # generates future blocks
        self.setup_game(next_colors)      # calls function
        move_made = True
        selected_square = None
        grow = True

        while True:
            self.draw_grid(False)
            if move_made:
                self.draw_predicted(next_colors)
                # generates 3 new futureblocks
                next_colors = [rand_color() for _ in range(3)]
                self.draw_future_grid(next_colors)
                move_made = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if x < 150 or y < 150:
                        break
                    x, y = normalize_cords(x, y)
                    x_grid = int((x / 50) - 3)
                    y_grid = int((y / 50) - 3)
                    if selected_square and self.space[x_grid][y_grid] == 0:
                        start = (
                            selected_square.grid_x,
                            selected_square.grid_y,
                        )
                        end = (x_grid, y_grid)
                        path = astar(self.space, start, end)
                        if path == 0:
                            break
                        first = path[0]
                        last = path[-1]
                        color = self.sqr_grid[first[0]][first[1]].color
                        self.sqr_grid[last[0]][last[1]].color = color
                        self.space[last[0]][last[1]] = 1
                        self.sqr_grid[first[0]][first[1]].color = BLACK
                        self.space[first[0]][first[1]] = 0
                        self.move_square(path, color)
                        lines = self.sqr_grid[last[0]][last[1]]
                        print(lines)
                        move_made = True
                        selected_square = None
                        break
                    if self.space[x_grid][y_grid] == 0:
                        break
                    selected_square = self.sqr_grid[x_grid][y_grid]
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if selected_square:
                if grow:
                    inf_val = 2
                    grow = False
                    color = selected_square.color
                    sleep(.2)
                else:
                    inf_val = -2
                    grow = True
                    color = BLACK
                    sleep(.5)
                selected_square.inflate_ip(inf_val, inf_val)
                selected_square.draw_colored_rect(color, 2, False)
            pygame.display.update()

    def move_square(self, path, color):
        prev_x = 0
        prev_y = 0
        for cords in path:
            self.sqr_grid[prev_x][prev_y].draw_colored_rect(BLACK)
            grid_x = cords[0]
            grid_y = cords[1]
            self.sqr_grid[grid_x][grid_y].draw_colored_rect(color)
            prev_x = grid_x
            prev_y = grid_y

    def draw_grid(self, new):
        if new:
            row = 0
            for x in range(OFFSET, WINDOW_WIDTH, BLOCKSIZE):
                col = 0
                for y in range(OFFSET, WINDOW_HEIGHT, BLOCKSIZE):
                    rect = ColoredRect(WHITE, x, y)
                    self.sqr_grid[row][col] = rect.draw_colored_rect(
                        WHITE, 1, False,
                    )
                    col += 1
                row += 1
        else:
            for row in self.sqr_grid:
                for rect in row:
                    rect.draw_colored_rect(WHITE, 1, False)

    def draw_future_grid(self, colors):
        self.next_sqrs.clear()
        for i, color in enumerate(colors):
            rect = ColoredRect(
                color,
                BLOCKSIZE,
                ((i + 5) * BLOCKSIZE) + (i * 25),
            )
            self.next_sqrs.append(rect)  # pass it as single color block

    def draw_predicted(self, next_colors):
        placed = 0
        while True:
            if placed == 3:
                break
            x = random.randint(150, 600)
            y = random.randint(150, 600)

            x, y = normalize_cords(x, y)
            x_grid = int((x / 50) - 3)
            y_grid = int((y / 50) - 3)

            x_grid_fd = (x_grid >= 0) < len(self.space)
            y_grid_fd = 0 <= y_grid < len(self.space[0])  # boundary checks
            if x_grid_fd and y_grid_fd and self.space[x_grid][y_grid] == 0:
                color = next_colors.pop()
                self.sqr_grid[x_grid][y_grid] = ColoredRect(
                    color,
                    x,
                    y,
                ).draw_colored_rect(color)
                self.space[x_grid][y_grid] = 1
                placed += 1


if __name__ == '__main__':
    AlignIt()
