"""
MG's Tower of Hanoi for Python - Models Module
Everything that gets drawn on the screen.
"""
import pygame
# Color Constants class
class ColorConstants():
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    BACKGROUND = (240, 248, 255)
    BOARD_COLOR = (153, 76, 0)
# Clickable button with centered text
class Button():
    def __init__(self, text, font, color, center, value=None, padding=10):
        self.label = font.render(text, True, ColorConstants.BLACK)
        self.rect = self.label.get_rect(center=center).inflate(padding * 2, padding)
        self.color = color
        self.value = value
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.label, self.label.get_rect(center=self.rect.center))
# Game board: knows where pegs and discs go on screen, the rules live in hanoi.py
class Board(ColorConstants):
    PEG_WIDTH = 20
    PEG_HEIGHT = 200
    DISC_HEIGHT = 20
    MIN_DISC_WIDTH = 40
    MAX_DISC_WIDTH = 220
    def __init__(self, screen_width, screen_height):
        self.rect = pygame.Rect(75, screen_height - 105, screen_width - 150, 50)
        # Each peg sits in the middle of its own third of the board
        self.column_width = self.rect.width / 3
        self.peg_x = [round(self.rect.x + self.column_width * (i + 0.5)) for i in range(3)]
    def disc_rect(self, game, peg, level):
        size = game.pegs[peg][level]
        # Widths grow evenly from the smallest to the biggest disc
        step = (self.MAX_DISC_WIDTH - self.MIN_DISC_WIDTH) / max(game.n_discs - 1, 1)
        rect = pygame.Rect(0, 0, self.MIN_DISC_WIDTH + step * (size - 1), self.DISC_HEIGHT)
        rect.midbottom = (self.peg_x[peg], self.rect.top - self.DISC_HEIGHT * level)
        return rect
    def top_disc_rect(self, game, peg):
        return self.disc_rect(game, peg, len(game.pegs[peg]) - 1)
    def disc_color(self, game, size):
        return self.RED if (game.n_discs - size) % 2 == 0 else self.GREEN
    # Peg whose column contains the point, or None if it's off the board
    def peg_at(self, pos):
        if not self.rect.left <= pos[0] < self.rect.right:
            return None
        return min(int((pos[0] - self.rect.left) // self.column_width), 2)
    # Peg whose top disc was clicked, or None
    def top_disc_at(self, game, pos):
        for peg in range(3):
            if game.pegs[peg] and self.top_disc_rect(game, peg).collidepoint(pos):
                return peg
        return None
    def draw(self, screen, game, drag=None):
        pygame.draw.rect(screen, self.BOARD_COLOR, self.rect)
        for x in self.peg_x:
            peg = pygame.Rect(0, 0, self.PEG_WIDTH, self.PEG_HEIGHT)
            peg.midbottom = (x, self.rect.top)
            pygame.draw.rect(screen, self.BOARD_COLOR, peg)
        for peg, discs in enumerate(game.pegs):
            for level, size in enumerate(discs):
                # The dragged disc is drawn last, under the mouse
                if drag and drag.peg == peg and level == len(discs) - 1:
                    continue
                pygame.draw.rect(screen, self.disc_color(game, size), self.disc_rect(game, peg, level))
        if drag:
            rect = self.top_disc_rect(game, drag.peg)
            rect.topleft = (drag.pos[0] - drag.offset[0], drag.pos[1] - drag.offset[1])
            pygame.draw.rect(screen, self.disc_color(game, game.top(drag.peg)), rect)
