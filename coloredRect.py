from __future__ import annotations

import pygame

BLOCKSIZE = 50


class ColoredRect(pygame.Rect):
    def __init__(self, color, x, y):
        super().__init__(x, y, BLOCKSIZE, BLOCKSIZE)
        x = (x - 150) / 50
        y = (y - 150) / 50
        self.color = color
        self.grid_x = int(x)
        self.grid_y = int(y)

    def __str__(self):
        return f'{super().__str__()}, {self.color}'

    def __repr__(self):
        return repr(self.__str__())

    def draw_colored_rect(self, SCREEN, color, fill=0, overide=True):
        if overide:
            self.color = color
        pygame.draw.rect(SCREEN, color, self, fill)
        return self
