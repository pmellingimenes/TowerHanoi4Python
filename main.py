import pygame
import models
 
# Define some colors constants
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
RED = [255, 0, 0]
BOARD_COLOR = [153, 76, 0]
DISC_WIDTH = 300
DISC_WIDTH = 50
pygame.init()
# Define the screen
size = [700, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("MG's Tower of Hanoi for Python")


all_sprites_list = pygame.sprite.Group()
# Drawing the game board (and it's positions)
game_board = models.Block(BOARD_COLOR, 600,50)
game_board.rect.x= 50
game_board.rect.y= 435
first_pos = models.Block(BOARD_COLOR, 40,200)
first_pos.rect.x = 60
first_pos.rect.y= 235
second_pos = models.Block(BOARD_COLOR, 40,200)
second_pos.rect.x = 335
second_pos.rect.y= 235
third_pos = models.Block(BOARD_COLOR,40,200)
third_pos.rect.x = 600
third_pos.rect.y= 235

all_pos = [first_pos,second_pos,third_pos]
player = models.Block(BLACK, 20, 15)
all_sprites_list.add([game_board,all_pos,player])

done = False
drag = False
drop = False
moveIt = False

last_pos = [0,0]
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
score = 0

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drag = True
            drop = False
            moveIt = player.is_clicked()
        elif event.type == pygame.MOUSEBUTTONUP:
            drag = False
            drop = True
            last_pos = event.pos
    screen.fill(WHITE)

    if drag:
        if moveIt:
            pos = pygame.mouse.get_pos()
            player.rect.x = pos[0]
            player.rect.y = pos[1]
    elif drop:
        if moveIt:
            player.rect.x = last_pos[0]
            player.rect.y = last_pos[1]
            moveIt = False
    all_sprites_list.draw(screen)
    # --- update  screen.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
