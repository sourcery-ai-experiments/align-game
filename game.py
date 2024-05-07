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
colors = [
    GREEN, RED,  # BLUE, YELLOW, PURPLE, CYAN, ORANGE, BROWN,
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
        self.removed_lines = 0
        self.sqr_grid = [[0 for _ in range(self.dim)] for _ in range(self.dim)]
        self.space = [[0 for _ in range(self.dim)] for _ in range(self.dim)]
        self.next_sqrs = []
        self.score_hr = 0
        self.score_vr = 0
        self.score_tldr = 0
        self.score_dltr = 0
        self.score_hrvr = self.score_hr + self.score_vr
        self.score_diag = self.score_dltr + self.score_tldr
        self.scoreall = self.score_hrvr + self.score_diag
        self.selected_square = None
        self.grow = True
        self.move_made = True
        self.same_color_counter = 0
        self.main()

    def setup_game(self, next_colors):
        global SCREEN, CLOCK
        pygame.init()
        self.text_font = pygame.font.SysFont('Arial', 30)
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
                predicted_col_cords = self.draw_predicted(next_colors)
                for x_grid, y_grid, color in predicted_col_cords:
                    lines = self.find_adjacent_color((x_grid, y_grid), color)
                    self.check_length_remove_square(lines)
                next_colors = [rand_color() for _ in range(3)]
                self.draw_future_grid(next_colors)
                self.move_made = False
            self.handle_mouse_click()
            self.handle_selected_square()
            self.score()
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
                    self.space[last[0]][last[1]] = 1
                    self.space[first[0]][first[1]] = 0
                    self.move_square(path, color)
                    lines = self.find_adjacent_color(last, color)
                    # print(f'hor ---{lines[0]}    ver ---{lines[1]}')
                    # print(f'UL-DR ---{lines[2]}     DL-UR ---{lines[3]}')
                    self.check_length_remove_square(lines)
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

    def game_over(self, text, color, x, y):
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        img = self.text_font.render(text, True, color)
        screen.blit(img, (x, y))

    def score(self):
        img = self.text_font.render(f'score: {self.scoreall}', True, WHITE)
        SCREEN.fill(BLACK, (470, 10, 130, 30))
        SCREEN.blit(img, (470, 10))

    def draw_predicted(self, next_colors):
        placed = 0
        future_square_cord_color = []
        available_positions = 0
        for row in self.space:
            available_positions += row.count(0)
        print(
            f'hor {self.score_hr}',
            f'ver {self.score_vr}',
            f'topL {self.score_tldr}',
            f'downL {self.score_dltr}',
            f'score {self.scoreall:.1f}',
        )
        while placed < 3 and available_positions > 0 and next_colors:

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
                future_square_cord_color.append((x_grid, y_grid, color))
                available_positions -= 1

                lines = self.find_adjacent_color((x_grid, y_grid), color)
                self.check_length_remove_square(lines)
        # self.draw_grid(False)

        if available_positions == 0:
            print('Game Over')
            self.game_over('Game Over', (255, 255, 255), 10, 10)
        return future_square_cord_color

    def find_adjacent_color(self, x_y, color):
        org_x, org_y = x_y
        directions = [
            (1, 0),  (0, 1), (1, 1), (1, -1),
            (-1, 0),  (0, -1), (-1, -1), (-1, 1),
        ]
        lines = {
            0: [(org_x, org_y)],
            1: [(org_x, org_y)],
            2: [(org_x, org_y)],
            3: [(org_x, org_y)],
        }
        for i, direction in enumerate(directions):
            x, y = org_x, org_y
            dir_x, dir_y = direction
            while True:
                x += dir_x
                y += dir_y
                try:
                    color_org = self.sqr_grid[org_x][org_y].color
                    color_adj = self.sqr_grid[x][y].color
                    is_same_color = color_org == color_adj
                    is_taken = self.space[x][y] == 1
                    if is_taken and is_same_color:
                        if x < 0 or y < 0:
                            continue
                        lines[i % 4].append((x, y))
                    else:
                        break
                except Exception:
                    break
        return lines

    def check_length_remove_square(self, lines):
        for direction, line in lines.items():
            if len(line) >= 5:
                for x, y in line:
                    self.sqr_grid[x][y].draw_colored_rect(BLACK)
                    self.space[x][y] = 0
                if direction == 0:
                    self.score_hr += 1
                elif direction == 1:
                    self.score_vr += 1
                elif direction == 2:
                    self.score_tldr += 1
                elif direction == 3:
                    self.score_dltr += 1
                self.removed_lines += 1

                self.score_hrvr = self.score_hr + self.score_vr
                self.score_diag = self.score_dltr + self.score_tldr
                self.scoreall = self.score_hrvr + self.score_diag
                print(self.removed_lines)


if __name__ == '__main__':
    AlignIt()
