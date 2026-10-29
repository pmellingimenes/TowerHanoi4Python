"""
MG's Tower of Hanoi for Python - Main Module
"""
from dataclasses import dataclass
import pygame
from hanoi import Hanoi
from models import ColorConstants as Colors, Button, Board
# Define screen constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
FPS = 60
# Game screens
MENU, PLAYING, GAME_OVER = range(3)
# Disc being dragged: which peg it came from, where the mouse grabbed it and where the mouse is now
@dataclass
class Drag():
    peg: int
    offset: tuple
    pos: tuple
def is_left_click(event):
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
class App():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("MG's Tower of Hanoi for Python")
        self.clock = pygame.time.Clock()
        # Fonts are loaded once, not every frame
        self.font = pygame.font.SysFont('Calibri', 30)
        self.title_font = pygame.font.SysFont('Calibri', 50)
        self.board = Board(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.state = MENU
        self.game = None
        self.drag = None
        self.running = True
        # Main menu buttons
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.btn_discs = [Button(str(n), self.font, Colors.BACKGROUND, (cx + 50 * (n - 5), cy), value=n)
                          for n in range(3, 8)]
        # In game button
        self.btn_menu = Button("Menu", self.font, Colors.BACKGROUND, (SCREEN_WIDTH - 70, 95))
        # Game over buttons
        self.btn_play_again = Button("Play again", self.font, Colors.GREEN, (cx - 210, cy - 40))
        self.btn_return = Button("Return to menu", self.font, Colors.BACKGROUND, (cx, cy - 40))
        self.btn_quit = Button("Quit", self.font, Colors.RED, (cx + 175, cy - 40))
    def start_game(self, n_discs):
        self.game = Hanoi(n_discs)
        self.drag = None
        self.state = PLAYING
    # -------- Event handling -----------
    def handle_menu(self, event):
        if not is_left_click(event):
            return
        for btn in self.btn_discs:
            if btn.is_clicked(event.pos):
                self.start_game(btn.value)
    def handle_playing(self, event):
        if is_left_click(event):
            if self.btn_menu.is_clicked(event.pos):
                self.state = MENU
                return
            # Only the top disc of a peg can be picked up
            peg = self.board.top_disc_at(self.game, event.pos)
            if peg is not None:
                rect = self.board.top_disc_rect(self.game, peg)
                self.drag = Drag(peg, (event.pos[0] - rect.x, event.pos[1] - rect.y), event.pos)
        elif event.type == pygame.MOUSEMOTION and self.drag:
            self.drag.pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.drag:
            # Illegal drops are ignored by Hanoi.move, so the disc just goes back to its peg
            dst = self.board.peg_at(event.pos)
            if dst is not None:
                self.game.move(self.drag.peg, dst)
            self.drag = None
            if self.game.is_solved():
                self.state = GAME_OVER
    def handle_game_over(self, event):
        if not is_left_click(event):
            return
        if self.btn_play_again.is_clicked(event.pos):
            self.start_game(self.game.n_discs)
        elif self.btn_return.is_clicked(event.pos):
            self.state = MENU
        elif self.btn_quit.is_clicked(event.pos):
            self.running = False
    # -------- Drawing -----------
    def draw_text(self, text, font, pos, center=False):
        render = font.render(text, True, Colors.BLACK)
        rect = render.get_rect(center=pos) if center else render.get_rect(topleft=pos)
        self.screen.blit(render, rect)
    def draw(self):
        self.screen.fill(Colors.WHITE)
        # Title line
        self.draw_text("MG's Tower of Hanoi", self.title_font, (SCREEN_WIDTH // 2, 35), center=True)
        pygame.draw.line(self.screen, Colors.BLACK, [0, 60], [SCREEN_WIDTH, 60], 5)
        if self.state == MENU:
            self.draw_text("Select the number of discs", self.font, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40), center=True)
            for btn in self.btn_discs:
                btn.draw(self.screen)
            return
        # Info texts
        self.draw_text("Player moves: " + str(self.game.moves), self.font, (20, 80))
        self.draw_text("Minimum of required movements: " + str(self.game.min_moves), self.font, (20, 110))
        self.board.draw(self.screen, self.game, self.drag)
        if self.state == PLAYING:
            self.btn_menu.draw(self.screen)
        else:
            for btn in (self.btn_play_again, self.btn_return, self.btn_quit):
                btn.draw(self.screen)
            if self.game.moves == self.game.min_moves:
                message = "Congratulations! You finished with the minimum moves! :)"
            else:
                message = "You finished! Now try again with the minimum moves ;)"
            self.draw_text(message, self.font, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), center=True)
    # -------- Main Game Loop -----------
    def run(self):
        handlers = {MENU: self.handle_menu, PLAYING: self.handle_playing, GAME_OVER: self.handle_game_over}
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    handlers[self.state](event)
            self.draw()
            pygame.display.flip()
            # Limit to 60 frames per second
            self.clock.tick(FPS)
        pygame.quit()
if __name__ == '__main__':
    App().run()
