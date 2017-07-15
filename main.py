"""
MG's Tower of Hanoi for Python - Main Module
"""
import pygame
import sys
import models

#disc number
N = int(sys.argv[1])
# Define some colors constants
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
RED = [255, 0, 0]
BOARD_COLOR = [153, 76, 0]
# Define elements size constants
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
# Game min movements
GAME_MIN_MOVES = (2**N) - 1
# Init pygame
pygame.init()
# Define the screen (and it's properties)
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MG's Tower of Hanoi for Python")

# Define the game sprites lists
all_sprites_list = pygame.sprite.Group()
pos_sprites_list = pygame.sprite.Group()

# Draw the game board (and it's positions)
game_board = models.Block(BOARD_COLOR, BOARD_WIDTH,BOARD_HEIGHT)
game_board.rect.x= BOARD_X
game_board.rect.y= BOARD_Y
first_pos = models.Position(0,BOARD_COLOR, POS_WIDTH,POS_HEIGHT)
first_pos.rect.x = BOARD_X 
first_pos.rect.y=  BOARD_Y - POS_HEIGHT
second_pos = models.Position(1,BOARD_COLOR, POS_WIDTH,POS_HEIGHT)
second_pos.rect.x = (BOARD_X + (BOARD_WIDTH/2)) - (POS_WIDTH/2)
second_pos.rect.y= BOARD_Y - POS_HEIGHT
third_pos = models.Position(2,BOARD_COLOR,POS_WIDTH,POS_HEIGHT)
third_pos.rect.x = (BOARD_X + BOARD_WIDTH) - POS_WIDTH
third_pos.rect.y= BOARD_Y - POS_HEIGHT
all_pos = [first_pos,second_pos,third_pos]
all_sprites_list.add([game_board,all_pos])
pos_sprites_list.add(all_pos)
discs = []
# Draw the game discs
for i in range(0,N):
    if i % 2 == 0:
        disc = models.Disc(0,i,RED,(DISC_WIDTH/(i+1)),DISC_HEIGHT)
    else:
        disc = models.Disc(0,i,GREEN,(DISC_WIDTH/(i+1)),DISC_HEIGHT)
    disc.rect.x = BOARD_X - ((DISC_WIDTH/(i+1)/2)-(DISC_HEIGHT/2))
    disc.rect.y = (BOARD_Y - DISC_HEIGHT) - (DISC_HEIGHT*i)
    discs.append(disc)
    all_pos[0].discs.append(disc)
all_sprites_list.add(discs)
# Discs' move variables
done = False
drag = False
drop = False
move = False
game_over = False
disc_index = None
last_pos = [0,0]
# Moves counter
moves_counter = 0
# Manage how fast the screen updates
clock = pygame.time.Clock()
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
                if discs[i].is_clicked():
                    current_pos = discs[i].current_pos
                    pos_length = len(all_pos[current_pos].discs)
                    if discs[i] == all_pos[current_pos].discs[pos_length-1]:
                        disc_index = i
                        last_pos = [discs[i].rect.x,discs[i].rect.y]
                        move = True
        elif event.type == pygame.MOUSEBUTTONUP:
            drag = False
            drop = True
            
    screen.fill(WHITE)
    # Title line
    pygame.draw.line(screen, BLACK, [0, 60], [SCREEN_WIDTH,60], 5) 
    # Text font,size, bold and italic
    font = pygame.font.SysFont('Calibri', 30, False, False)
    title_font = pygame.font.SysFont('Calibri', 50, False, False)
    # Info Texts
    game_title = title_font.render("MG's Tower of Hanoi ", True, BLACK)
    player_moves = font.render("Player moves: "+str(moves_counter), True, BLACK)
    min_moves = font.render("Minimum of required movements: "+str(GAME_MIN_MOVES), True, BLACK)
    screen.blit(game_title, [((SCREEN_WIDTH/2)-(game_title.get_width()/2)),20])
    screen.blit(player_moves, [20, 80])
    screen.blit(min_moves, [20, 110])
    if game_over:
        if len(all_pos[2].discs) == N:
            if moves_counter == GAME_MIN_MOVES:
                game_over_title = font.render("Congratulations! You just finished the game with the minimums movements! :)", True, BLACK)
                screen.blit(game_over_title, [((SCREEN_WIDTH/2)-(game_over_title.get_width()/2)),SCREEN_HEIGHT/2])
            else:
                game_over_title = font.render("You just finished the game, now try again with the minimums movements! ;)", True, BLACK)
                screen.blit(game_over_title, [((SCREEN_WIDTH/2)-(game_over_title.get_width()/2)),SCREEN_HEIGHT/2])

    else:
        if drag:
            if move:
                pos = pygame.mouse.get_pos()
                discs[disc_index].rect.x = pos[0] - (discs[disc_index].width/2)
                discs[disc_index].rect.y = pos[1] - (discs[disc_index].height/2)
        elif drop:
            if move:
                current_pos = discs[disc_index].current_pos
                new_pos = None
                change = False
                turn_back = True
                position = pygame.sprite.spritecollideany(discs[disc_index],pos_sprites_list)
                if position != None:
                    new_pos = position.pos_index
                    if new_pos != current_pos:
                        disc_length = len(position.discs)
                        if disc_length == 0:
                            turn_back = False
                            change = True
                        elif discs[disc_index].id > position.discs[disc_length-1].id:
                            turn_back = False
                            change = True
                if change:
                    moves_counter = moves_counter + 1
                    all_pos[current_pos].discs.remove(discs[disc_index])
                    discs[disc_index].current_pos = new_pos
                    all_pos[new_pos].discs.append(discs[disc_index])                
                    new_pos_length = len(all_pos[new_pos].discs)
                    discs[disc_index].rect.x = all_pos[new_pos].rect.x - ((DISC_WIDTH/(discs[disc_index].id+1)/2)-(DISC_HEIGHT/2))
                    discs[disc_index].rect.y = (BOARD_Y - DISC_HEIGHT) - (DISC_HEIGHT*(new_pos_length-1))
                    #Check if the game is over
                    if (len(all_pos[2].discs) == N):
                        game_over = True
                if turn_back:
                    discs[disc_index].rect.x = last_pos[0]
                    discs[disc_index].rect.y = last_pos[1]
                move = False
    all_sprites_list.draw(screen)
    # --- update  screen.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)
pygame.quit()
