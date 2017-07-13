"""
MG's Tower of Hanoi for Python - Main Module
"""
import pygame
import models
 
# Define some colors constants
N = 3 #disc number
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
RED = [255, 0, 0]
BOARD_COLOR = [153, 76, 0]
SCREEN_WIDTH = 900
SCREEN_HEIGTH = 700
BOARD_WIDTH = SCREEN_WIDTH/2
BOARD_HEIGTH = 50
BOARD_X = SCREEN_WIDTH * 0.25
BOARD_Y = SCREEN_HEIGTH - 55
POS_WIDTH = 20
POS_HEIGTH = 200
DISC_WIDTH = 200
DISC_HEIGTH = POS_WIDTH
pygame.init()

# Define the screen (and it's properties)

size = [SCREEN_WIDTH, SCREEN_HEIGTH]

screen = pygame.display.set_mode(size)

pygame.display.set_caption("MG's Tower of Hanoi for Python")

# Define the game sprites lists
all_sprites_list = pygame.sprite.Group()
disc_sprites_list = pygame.sprite.Group()
# Draw the game board (and it's positions)
game_board = models.Block(BOARD_COLOR, BOARD_WIDTH,BOARD_HEIGTH)
game_board.rect.x= BOARD_X
game_board.rect.y= BOARD_Y
first_pos = models.Block(BOARD_COLOR, POS_WIDTH,POS_HEIGTH)
first_pos.rect.x = BOARD_X 
first_pos.rect.y=  BOARD_Y - POS_HEIGTH
second_pos = models.Block(BOARD_COLOR, POS_WIDTH,POS_HEIGTH)
second_pos.rect.x = (BOARD_X + (BOARD_WIDTH/2)) - (POS_WIDTH/2)
second_pos.rect.y= BOARD_Y - POS_HEIGTH
third_pos = models.Block(BOARD_COLOR,POS_WIDTH,POS_HEIGTH)
third_pos.rect.x = (BOARD_X + BOARD_WIDTH) - POS_WIDTH
third_pos.rect.y= BOARD_Y - POS_HEIGTH

all_pos = [first_pos,second_pos,first_pos,third_pos]
player = models.Block(BLACK, 20, 15)
all_sprites_list.add([game_board,all_pos,player])
# Draw the game discs
for i in range(0,N):
    if i % 2 == 0:
        disc = models.Block(RED,(DISC_WIDTH/(i+1)),DISC_HEIGTH)
    else:
        disc = models.Block(GREEN,(DISC_WIDTH/(i+1)),DISC_HEIGTH)
    disc.rect.x = BOARD_X - ((DISC_WIDTH/(i+1)/2)-(DISC_HEIGTH/2))
    disc.rect.y = (BOARD_Y - DISC_HEIGTH) - (DISC_HEIGTH*i)
    all_sprites_list.add(disc)
    disc_sprites_list.add(disc)

# Discs' move variables
done = False
drag = False
drop = False
move = False
last_pos = [0,0]

# Manage how fast the screen updates
clock = pygame.time.Clock()
score = 0

# -------- Main Game Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drag = True
            drop = False
            move = player.is_clicked()
        elif event.type == pygame.MOUSEBUTTONUP:
            drag = False
            drop = True
            last_pos = event.pos
    screen.fill(WHITE)

    if drag:
        if move:
            pos = pygame.mouse.get_pos()
            player.rect.x = pos[0]
            player.rect.y = pos[1]
    elif drop:
        if move:
            player.rect.x = last_pos[0]
            player.rect.y = last_pos[1]
            move = False
    all_sprites_list.draw(screen)
    # --- update  screen.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
