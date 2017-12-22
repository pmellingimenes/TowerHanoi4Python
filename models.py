"""
MG's Tower of Hanoi for Python - Models Module
"""
import pygame
# Color Constants class
class ColorConstants():
        RED = [255, 0, 0]
        BLACK = [0, 0, 0]
        GREEN = [0, 255, 0]
        WHITE = [255, 255, 255]
        BACKGROUND = [240, 248, 255]
        BOARD_COLOR = [153, 76, 0]
# Generic Block class
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())
# Game positions class
class Position(Block):
    def __init__(self, pos_index,color, width, height):
        Block.__init__(self,color, width, height)
        self.pos_index = pos_index
        self.discs = []
# Game discs class
class Disc(Block):
    def __init__(self,current_pos,id,color, width, height):
        Block.__init__(self,color, width, height)
        self.current_pos = current_pos
        self.id = id
# Buttons class
class Button(Block):
    def __init__(self,text,text_color,text_size,text_font,color, width, height):
        Block.__init__(self,color, width, height)
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.SysFont(text_font, text_size, False, False)
        self.text_render = self.font.render(text, 1, text_color)
        self.value = None
    def set_value(self,value):
        self.value = value
    def render_text(self):
        w = (self.width/2-(self.text_render.get_width()/2))
        h = (self.height/2-(self.text_render.get_height()/2))
        self.image.blit(self.text_render,[w,h])
# Main Menu
class MainMenu(ColorConstants):
    def __init__(self,SCREEN_WIDTH,SCREEN_HEIGHT):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.sprites_list = pygame.sprite.Group()
        self.btn_discs = []
        self.label = Button("Select the number of discs",self.BLACK,30,'Calibri',self.WHITE,500,30)
        self.label.rect.x = self.SCREEN_WIDTH/4
        self.label.rect.y = self.SCREEN_HEIGHT/2 - 40
        self.label.render_text()
        self.sprites_list.add(self.label)
        for i in range(3,8):
            btn = Button(str(i),self.BLACK,30,'Calibri',self.BACKGROUND,20,30)
            btn.rect.x = self.SCREEN_WIDTH/3 + 50*(i-2)
            btn.rect.y = self.SCREEN_HEIGHT/2
            btn.render_text()
            btn.set_value(i)
            self.btn_discs.append(btn)
        self.sprites_list.add(self.btn_discs)
        # Game over buttons
        self.btn_play_again = Button("Play again",self.BLACK,30,'Calibri',self.GREEN,130,30)
        self.btn_return = Button("Return to menu",self.BLACK,30,'Calibri',self.BACKGROUND,150,30)
        self.btn_quit = Button("Quit",self.BLACK,30,'Calibri',self.RED,70,30)
        self.btn_play_again.rect.x = self.SCREEN_WIDTH/2 - (self.btn_return.image.get_width()*2)
        self.btn_play_again.rect.y = self.SCREEN_HEIGHT/2 - 40
        self.btn_play_again.render_text()
        self.btn_return.rect.x = self.SCREEN_WIDTH/2  - self.btn_return.image.get_width()/2
        self.btn_return.rect.y = self.SCREEN_HEIGHT/2 - 40
        self.btn_return.render_text()
        self.btn_quit.rect.x = self.SCREEN_WIDTH/2 + (self.btn_return.image.get_width())
        self.btn_quit.rect.y = self.SCREEN_HEIGHT/2 - 40
        self.btn_quit.render_text()
# Game main class
class Game(ColorConstants):
    def __init__(self,SCREEN_WIDTH,SCREEN_HEIGHT):
        # Game sprites groups
        self.sprites_list = pygame.sprite.Group()
        self.pos_sprites_list = pygame.sprite.Group()
        # Game constants
        self.BOARD_WIDTH = SCREEN_WIDTH/2
        self.BOARD_HEIGHT = 50
        self.BOARD_X = SCREEN_WIDTH * 0.25
        self.BOARD_Y = SCREEN_HEIGHT - 55
        self.POS_WIDTH = 20
        self.POS_HEIGHT = 200
        self.DISC_WIDTH = 200
        self.DISC_HEIGHT = self.POS_WIDTH
        # Positions and discs lists
        self.positions = []
        self.discs = []
        # Draw the game board and it's positions
        self.game_board = Block(self.BOARD_COLOR, self.BOARD_WIDTH,self.BOARD_HEIGHT)
        self.game_board.rect.x= self.BOARD_X
        self.game_board.rect.y= self.BOARD_Y
        first_pos = Position(0,self.BOARD_COLOR, self.POS_WIDTH,self.POS_HEIGHT)
        first_pos.rect.x = self.BOARD_X
        first_pos.rect.y=  self.BOARD_Y - self.POS_HEIGHT
        second_pos = Position(1,self.BOARD_COLOR, self.POS_WIDTH,self.POS_HEIGHT)
        second_pos.rect.x = (self.BOARD_X + (self.BOARD_WIDTH/2)) - (self.POS_WIDTH/2)
        second_pos.rect.y= self.BOARD_Y - self.POS_HEIGHT
        third_pos = Position(2,self.BOARD_COLOR,self.POS_WIDTH,self.POS_HEIGHT)
        third_pos.rect.x = (self.BOARD_X + self.BOARD_WIDTH) - self.POS_WIDTH
        third_pos.rect.y= self.BOARD_Y - self.POS_HEIGHT
        self.positions = [first_pos,second_pos,third_pos]
        self.sprites_list.add([self.game_board,self.positions])
        self.pos_sprites_list.add(self.positions)
    # Set discs number and mim movements
    def set_n_discs(self,n_discs):
        self.n_discs = n_discs
        self.min_moves = ((2**self.n_discs)-1)
    # Draw discs method
    def draw_discs(self):
        DISC_WIDTH = 200
        DISC_HEIGHT = self.POS_WIDTH
        for i in range(0,self.n_discs):
            if i % 2 == 0:
                disc = Disc(0,i,self.RED,(DISC_WIDTH/(i+1)),DISC_HEIGHT)
            else:
                disc = Disc(0,i,self.GREEN,(DISC_WIDTH/(i+1)),DISC_HEIGHT)
            disc.rect.x = self.BOARD_X - ((DISC_WIDTH/(i+1)/2)-(DISC_HEIGHT/2))
            disc.rect.y = (self.BOARD_Y - DISC_HEIGHT) - (DISC_HEIGHT*i)
            self.discs.append(disc)
            self.positions[0].discs.append(disc)
        self.sprites_list.add(self.discs)