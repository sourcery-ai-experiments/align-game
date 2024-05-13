from astar import astar


class SquareGrid:
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 for _ in range(dim)] for _ in range(dim)]

    def find_path(self, start, end):
        return astar(self.grid, start, end)
