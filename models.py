"""
MG's Tower of Hanoi for Python - Models Module
"""
import pygame
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
class Position(Block):
    def __init__(self, pos_index,color, width, height):
        Block.__init__(self,color, width, height)
        self.pos_index = pos_index
        self.discs = []
class Disc(Block):
    def __init__(self,current_pos,id,color, width, height):
        Block.__init__(self,color, width, height)
        self.current_pos = current_pos
        self.id = id