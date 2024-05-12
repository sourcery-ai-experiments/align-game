from astar import astar


class SquareGrid:
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 for _ in range(dim)] for _ in range(dim)]

    def find_path(self, start, end):
        return astar(self.grid, start, end)

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
