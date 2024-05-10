import random
from time import sleep

import pygame

from astar import astar
from buttons_class import Buttons
from coloredRect import ColoredRect
from stats import STATS

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
    GREEN, RED,  BLUE, YELLOW, PURPLE, CYAN, ORANGE, BROWN,
]


def rand_color():
    return random.choice(colors)


def normalize_cords(x, y):
    x = x - (x % BLOCKSIZE)
    y = y - (y % BLOCKSIZE)
    return (x, y)


class AlignIt:
    dim = 9

    def __init__(self):
        self.spawn = True
        self.moves_made = 0
        self.scoreall = 0
        self.buttons_instance = Buttons(self.scoreall, self.moves_made)
        self.removed_lines = 0
        self.sqr_grid = [[0 for _ in range(self.dim)] for _ in range(self.dim)]
        self.space = [[0 for _ in range(self.dim)] for _ in range(self.dim)]
        self.next_sqrs = []
        self.selected_square = None
        self.grow = True
        self.move_made = True
        self.same_color_counter = 0
        self.future_sqr_cord_color = []
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

    def handle_spawning(self, next_colors):
        future_sqr_cord_color = self.draw_predicted(next_colors)
        self.future_sqr_cord_color = future_sqr_cord_color

    def process_turn(self, next_colors):
        if self.spawn:
            self.handle_spawning(next_colors)
            for x_grid, y_grid, color in self.future_sqr_cord_color:
                lines = self.find_adjacent_color((x_grid, y_grid), color)
                self.check_length_remove_square(lines)

    def main(self):
        next_colors = [rand_color() for _ in range(3)]
        self.setup_game(next_colors)

        while True:
            self.draw_grid(False)
            if self.move_made:
                try:
                    success = self.process_turn(next_colors)
                    if not success:
                        print('Failed to process turn.')
                except Exception as e:
                    print(f'An error occurred: {e}')
                self.spawn = True
                next_colors = [rand_color() for _ in range(3)]
                self.draw_future_grid(next_colors)
                self.move_made = False
            self.handle_mouse_click()
            self.handle_selected_square()
            STATS.score(self)
            STATS.movesmade(self)
            pygame.display.update()

    def select_square(self, x, y):
        x, y = normalize_cords(x, y)
        x_grid = int((x / 50) - 3)
        y_grid = int((y / 50) - 3)
        return x_grid, y_grid

    def square_path(self, start, end):
        path = astar(self.space, start, end)
        first = path[0]
        last = path[-1]
        color = self.sqr_grid[first[0]][first[1]].color
        self.space[last[0]][last[1]] = 1
        self.space[first[0]][first[1]] = 0
        self.move_square(path, color)
        lines = self.find_adjacent_color(last, color)
        self.check_length_remove_square(lines)
        self.move_made = True
        return path, color

    def handle_mouse_click(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                x_grid, y_grid = self.select_square(x, y)
                if x < OFFSET or y < OFFSET:
                    break
                if self.selected_square and self.space[x_grid][y_grid] == 0:
                    start = (
                        self.selected_square.grid_x,
                        self.selected_square.grid_y,
                    )
                    end = (x_grid, y_grid)
                    path = self.square_path(start, end)
                    if path is None:
                        break
                    self.selected_square = None
                    break
                if self.space[x_grid][y_grid] == 0:
                    break
                self.selected_square = self.sqr_grid[x_grid][y_grid]
            if event.type == pygame.QUIT:
                self.buttons_instance.quit_menu(
                    'Player name:', 'quit', 'reset', 'load',
                    (255, 255, 255), 200, 200,
                )

    def handle_selected_square(self):
        if self.selected_square:
            sleep(.5)
            if self.grow:
                inf_val = 2
                self.grow = False
                color = self.selected_square.color
            else:
                inf_val = -2
                self.grow = True
                color = BLACK
            self.selected_square.inflate_ip(inf_val, inf_val)
            self.selected_square.draw_colored_rect(color, 2, False)
            pygame.display.update()

    def move_square(self, path, color):
        self.moves_made += 1
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
            for row, x in enumerate(range(OFFSET, WINDOW_WIDTH, BLOCKSIZE)):
                for col, y in enumerate(
                    range(OFFSET, WINDOW_HEIGHT, BLOCKSIZE),
                ):
                    rect = ColoredRect(WHITE, x, y)
                    self.sqr_grid[row][col] = rect.draw_colored_rect(
                        WHITE, 1, False,
                    )
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
        future_sqr_cord_color = []
        available_positions = 0
        for row in self.space:
            available_positions += row.count(0)
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
                future_sqr_cord_color.append((x_grid, y_grid, color))
                available_positions -= 1
                lines = self.find_adjacent_color((x_grid, y_grid), color)
                self.check_length_remove_square(lines)
        if available_positions == 0:
            STATS.game_over(self, 'Game Over', (RED), 10, 10)
        return future_sqr_cord_color

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
                    color_adj = self.sqr_grid[x][y].color
                    is_same_color = color == color_adj
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

    def stop_spawning(self):
        self.spawn = False

    def check_length_remove_square(self, lines):
        for direction, line in lines.items():
            if len(line) >= 5:
                self.stop_spawning()
                for x, y in line:
                    self.sqr_grid[x][y].draw_colored_rect(BLACK)
                    self.space[x][y] = 0
                if direction in [0, 1, 2, 3]:
                    self.scoreall += len(line)


if __name__ == '__main__':
    AlignIt()
