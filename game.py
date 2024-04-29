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
colors = [
    GREEN, RED, BLUE, YELLOW, PURPLE, CYAN, ORANGE, BROWN,
]


def rand_color():
    return random.choice(colors)


def normalize_cords(x, y):
    x = x - (x % 50)
    y = y - (y % 50)
    return (x, y)


class AlignIt:
    dim = 9

    def __init__(self):
        self.sqr_grid = [[0 for _ in range(self.dim)] for _ in range(self.dim)]
        self.space = [[0 for _ in range(self.dim)] for _ in range(self.dim)]
        self.next_sqrs = []
        self.score = 0
        self.selected_square = None
        self.grow = True
        self.move_made = True
        self.same_color_counter = 0
        self.main()

    def setup_game(self, next_colors):
        global SCREEN, CLOCK
        pygame.init()
        pygame.mixer.music.pause()
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        CLOCK = pygame.time.Clock()
        SCREEN.fill(BLACK)
        self.draw_future_grid(next_colors)
        self.draw_grid(True)

    def main(self):
        next_colors = [rand_color() for _ in range(3)]
        self.setup_game(next_colors)

        while True:
            self.draw_grid(False)
            if self.move_made:
                self.draw_predicted(next_colors)
                next_colors = [rand_color() for _ in range(3)]
                self.draw_future_grid(next_colors)
                self.move_made = False
            self.handle_mouse_click()
            self.handle_selected_square()
            pygame.display.update()

    def handle_mouse_click(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if x < 150 or y < 150:
                    break
                x, y = normalize_cords(x, y)
                x_grid = int((x / 50) - 3)
                y_grid = int((y / 50) - 3)
                if self.selected_square and self.space[x_grid][y_grid] == 0:
                    start = (
                        self.selected_square.grid_x,
                        self.selected_square.grid_y,
                    )
                    end = (x_grid, y_grid)
                    path = astar(self.space, start, end)
                    if path is None:
                        break
                    first = path[0]
                    last = path[-1]
                    color = self.sqr_grid[first[0]][first[1]].color
                    # self.sqr_grid[last[0]][last[1]].color = color
                    self.space[last[0]][last[1]] = 1
                    # self.sqr_grid[first[0]][first[1]].color = BLACK
                    self.space[first[0]][first[1]] = 0
                    self.move_square(path, color)
                    # find color of next square moved
                    lines = self.find_adjacent(last)
                    print(lines)
                    self.move_made = True
                    self.selected_square = None
                    break
                if self.space[x_grid][y_grid] == 0:
                    break
                self.selected_square = self.sqr_grid[x_grid][y_grid]
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def handle_selected_square(self):
        if self.selected_square:
            if self.grow:
                inf_val = 2
                self.grow = False
                color = self.selected_square.color
                sleep(.5)
            else:
                inf_val = -2
                self.grow = True
                color = BLACK
                sleep(.5)
            self.selected_square.inflate_ip(inf_val, inf_val)
            self.selected_square.draw_colored_rect(color, 2, False)
            pygame.display.update()

    def move_square(self, path, color):
        for i, cords in enumerate(path):
            prev_x = path[i-1][0]
            prev_y = path[i-1][1]
            self.sqr_grid[prev_x][prev_y].draw_colored_rect(BLACK)
            x = cords[0]
            y = cords[1]
            self.sqr_grid[x][y].draw_colored_rect(color)
            sleep(0.1)
            pygame.display.update()

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
        for i, color in enumerate(colors):
            self.next_sqrs = ColoredRect(
                color,
                BLOCKSIZE,
                ((i + 5) * BLOCKSIZE) +
                (i * 25),
            ).draw_colored_rect(color)

    def draw_predicted(self, next_colors):
        placed = 0
        while True:
            if placed == 3:
                break
            x = random.randint(OFFSET, WINDOW_WIDTH)
            y = random.randint(OFFSET, WINDOW_HEIGHT)
            x, y = normalize_cords(x, y)
            x_grid = int((x / 50) - 3)
            y_grid = int((y / 50) - 3)
            if (
                0 <= x_grid < len(self.space[0])
                and 0 <= y_grid < len(self.space[0])
                and self.space[x_grid][y_grid] == 0
            ):
                color = next_colors.pop()
                self.sqr_grid[x_grid][y_grid] = ColoredRect(
                    color,
                    x,
                    y,
                ).draw_colored_rect(color)
                self.space[x_grid][y_grid] = 1
                placed += 1

    def find_adjacent(self, x_y):
        x, y = x_y
        directions = [
            (1, 0),  (0, 1), (1, 1), (1, -1),
            (-1, 0),  (0, -1), (-1, -1), (-1, 1),
        ]
        target = self.space[x][y]
        lines = {0: [(x, y)], 1: [(x, y)], 2: [(x, y)], 3: [(x, y)]}
        grid_check = [[False for _ in range(self.dim)]
                      for _ in range(self.dim)]
        for i, direction in enumerate(directions):
            dir_x, dir_y = direction
            while True:
                x += dir_x
                y += dir_y
                try:
                    is_taken = grid_check[x][y] is not True
                    if self.space[x][y] == target and is_taken:
                        if x < 0 or y < 0:
                            continue
                        lines[i % 4].append((x, y))
                        grid_check[x][y] = True
                    else:
                        break
                except Exception:
                    break

        return lines


if __name__ == '__main__':
    AlignIt()
