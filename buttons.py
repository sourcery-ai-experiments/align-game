import pygame

from constants import BLACK
from constants import GREY
from constants import WHITE
from constants import WINDOW_HEIGHT
from constants import WINDOW_WIDTH


class Buttons:
    def __init__(self, scoreall, moves_made):
        pygame.font.init()
        self.text_font = pygame.font.SysFont('Arial', 30)
        self.scoreall = scoreall
        self.moves_made = moves_made

    def quit_menu(
        self,
        text,
        load_button_text,
        reset_button_text,
        quit_button_text,
        back_button_text,
        color, x, y,
    ):
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        img = self.text_font.render(text, True, color)
        score_text = self.text_font.render(
            f'Score: {self.scoreall}', True, WHITE,
        )
        moves = self.text_font.render(
            f'Moves made: {self.moves_made}', True, WHITE,
        )
        screen.blit(img, (x, y))
        screen.blit(score_text, (x, y + 50))
        screen.blit(moves, (x, y + 100))
        load_button_rect = pygame.Rect(x, y + 270, 150, 50)
        self.render_reset_button(screen, load_button_rect, load_button_text)
        reset_button_rect = pygame.Rect(x, y + 210, 150, 50)
        self.render_reset_button(screen, reset_button_rect, reset_button_text)
        quit_button_rect = pygame.Rect(x, y + 150, 150, 50)
        self.render_quit_button(screen, quit_button_rect, quit_button_text)
        back_button_rect = pygame.Rect(x, y + 330, 150, 50)
        self.render_quit_button(screen, back_button_rect, back_button_text)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if quit_button_rect.collidepoint(mouse_pos):
                        self.load_function()
                    elif reset_button_rect.collidepoint(mouse_pos):
                        self.reset_function()
                    elif load_button_rect.collidepoint(mouse_pos):
                        self.quit_function()
                    elif back_button_rect.collidepoint(mouse_pos):
                        self.back_function()

    def render_quit_button(self, screen, button_rect, quit_button_text):
        pygame.draw.rect(screen, GREY, button_rect)
        button_text_surface = self.text_font.render(
            quit_button_text, True, BLACK,
        )
        text_rect = button_text_surface.get_rect(center=button_rect.center)
        screen.blit(button_text_surface, text_rect)

    def render_reset_button(self, screen, button_rect, reset_button_text):
        pygame.draw.rect(screen, GREY, button_rect)
        button_text_surface = self.text_font.render(
            reset_button_text, True, BLACK,
        )
        text_rect = button_text_surface.get_rect(center=button_rect.center)
        screen.blit(button_text_surface, text_rect)

    def render_load_button(self, screen, button_rect, load_button_text):
        pygame.draw.rect(screen, GREY, button_rect)
        button_text_surface = self.text_font.render(
            load_button_text, True, BLACK,
        )
        text_rect = button_text_surface.get_rect(center=button_rect.center)
        screen.blit(button_text_surface, text_rect)

    def render_back_button(self, screen, button_rect, back_button_text):
        pygame.draw.rect(screen, GREY, button_rect)
        button_text_surface = self.text_font.render(
            back_button_text, True, BLACK,
        )
        text_rect = button_text_surface.get_rect(center=button_rect.center)
        screen.blit(button_text_surface, text_rect)

    def quit_function(self):
        print('quit')
        pygame.quit()
        quit()

    def reset_function(self):
        print('reset')

    def load_function(self):
        print('load')

    def back_function(self):
        print('back')
