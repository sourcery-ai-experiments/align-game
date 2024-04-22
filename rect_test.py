import pygame
import sys
from time import sleep

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
BLOCKSIZE = 150
BLACK = (0, 0, 0)
GREY = (160, 160, 160)
WHITE = (200, 200, 200)


def draw_colored_square(x, y, color, fill=0, rect=None):
    if not rect:
        rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
    rect = pygame.draw.rect(SCREEN, color, rect, fill)
    return rect


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    sqrts = []
    grow = True
    rect = draw_colored_square(100, 100, '#ED1C24')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()

main()
