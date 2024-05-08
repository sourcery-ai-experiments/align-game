import astar


class squareGrid:
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 for _ in range(dim)] for _ in range(dim)]

    def find_path(self, start, end):
        return astar(self.grid, start, end)

    def find_adjacent(self, x_y):
        x, y = x_y
        directions = [
            (1, 0), (0, 1), (1, 1), (1, -1),
            (-1, 0), (0, -1), (-1, -1), (-1, 1),
        ]
        target = self.grid[x][y]
        lines = {0: [], 1: [], 2: [], 3: []}
        grid_check = [[False for _ in range(self.dim)]
                      for _ in range(self.dim)]
        for i, direction in enumerate(directions):
            x, y = x_y
            dir_x, dir_y = direction
            while True:
                x += dir_x
                y += dir_y
                try:
                    is_taken = grid_check[x][y] is not True
                    if self.grid[x][y] == target and is_taken:
                        if x < 0 or y < 0:
                            continue
                        lines[i].append((x, y))
                        grid_check[x][y] = True
                    else:
                        break
                except Exception:
                    break
        return lines
