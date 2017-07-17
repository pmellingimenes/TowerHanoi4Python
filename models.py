"""
MG's Tower of Hanoi for Python - Models Module
"""
import pygame
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
    def render_text(self):
        w = (self.width/2-(self.text_render.get_width()/2))
        h = (self.height/2-(self.text_render.get_height()/2))
        self.image.blit(self.text_render,[w,h])