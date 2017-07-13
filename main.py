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
SCREEN_HEIGHT = 700
BOARD_WIDTH = SCREEN_WIDTH/2
BOARD_HEIGHT = 50
BOARD_X = SCREEN_WIDTH * 0.25
BOARD_Y = SCREEN_HEIGHT - 55
POS_WIDTH = 20
POS_HEIGHT = 200
DISC_WIDTH = 200
DISC_HEIGHT = POS_WIDTH
pygame.init()

# Define the screen (and it's properties)

size = [SCREEN_WIDTH, SCREEN_HEIGHT]

screen = pygame.display.set_mode(size)

pygame.display.set_caption("MG's Tower of Hanoi for Python")

# Define the game sprites lists
all_sprites_list = pygame.sprite.Group()
disc_sprites_list = pygame.sprite.Group()
# Draw the game board (and it's positions)
game_board = models.Block(BOARD_COLOR, BOARD_WIDTH,BOARD_HEIGHT)
game_board.rect.x= BOARD_X
game_board.rect.y= BOARD_Y
first_pos = models.Block(BOARD_COLOR, POS_WIDTH,POS_HEIGHT)
first_pos.rect.x = BOARD_X 
first_pos.rect.y=  BOARD_Y - POS_HEIGHT
second_pos = models.Block(BOARD_COLOR, POS_WIDTH,POS_HEIGHT)
second_pos.rect.x = (BOARD_X + (BOARD_WIDTH/2)) - (POS_WIDTH/2)
second_pos.rect.y= BOARD_Y - POS_HEIGHT
third_pos = models.Block(BOARD_COLOR,POS_WIDTH,POS_HEIGHT)
third_pos.rect.x = (BOARD_X + BOARD_WIDTH) - POS_WIDTH
third_pos.rect.y= BOARD_Y - POS_HEIGHT

all_pos = [first_pos,second_pos,first_pos,third_pos]
all_sprites_list.add([game_board,all_pos])
discs = []
# Draw the game discs
for i in range(0,N):
    if i % 2 == 0:
        disc = models.Block(RED,(DISC_WIDTH/(i+1)),DISC_HEIGHT)
    else:
        disc = models.Block(GREEN,(DISC_WIDTH/(i+1)),DISC_HEIGHT)
    disc.rect.x = BOARD_X - ((DISC_WIDTH/(i+1)/2)-(DISC_HEIGHT/2))
    disc.rect.y = (BOARD_Y - DISC_HEIGHT) - (DISC_HEIGHT*i)
    discs.append(disc)
all_sprites_list.add(discs)
# Discs' move variables
done = False
drag = False
drop = False
move = False
disc_index = None
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
            for i in range(0,N):
                if(discs[i].is_clicked()):
                    disc_index = i
                    move = True
                

        elif event.type == pygame.MOUSEBUTTONUP:
            drag = False
            drop = True
            last_pos = event.pos
    screen.fill(WHITE)

    if drag:
        if move:
            pos = pygame.mouse.get_pos()
            discs[disc_index].rect.x = pos[0] - (discs[disc_index].width/2)
            discs[disc_index].rect.y = pos[1] - (discs[disc_index].height/2)
    elif drop:
        if move:
            discs[disc_index].rect.x = last_pos[0] - (discs[disc_index].width/2)
            discs[disc_index].rect.y = last_pos[1] - (discs[disc_index].height/2)
            move = False
    all_sprites_list.draw(screen)
    # --- update  screen.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
