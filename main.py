"""
MG's Tower of Hanoi for Python - Main Module
"""
import pygame
import models
import sys
# Define screen constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
# Color constants object
color = models.ColorConstants()
# Init pygame
pygame.init()
# Define the screen (and it's properties)
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MG's Tower of Hanoi for Python")
# Create main menu object
menu = models.MainMenu(SCREEN_WIDTH,SCREEN_HEIGHT)
# Create game object
game = models.Game(SCREEN_WIDTH,SCREEN_HEIGHT)
# Discs' move variables
done = False
drag = False
drop = False
move = False
game_over = False
init_game = False
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
            if init_game:
                if not game_over:
                    for i in range(0,game.n_discs):
                        if game.discs[i].is_clicked():
                            current_pos = game.discs[i].current_pos
                            pos_length = len(game.positions[current_pos].discs)
                            if game.discs[i] == game.positions[current_pos].discs[pos_length-1]:
                                disc_index = i
                                last_pos = [game.discs[i].rect.x,game.discs[i].rect.y]
                                move = True
                else:
                    if menu.btn_quit.is_clicked():
                        done = True
                    if menu.btn_play_again.is_clicked():
                        game.sprites_list.remove(game.discs)
                        game.positions[2].discs = []
                        moves_counter = 0
                        game.discs = []
                        game.draw_discs()
                        game_over = False
                    if menu.btn_return.is_clicked():
                        menu.sprites_list.remove([menu.btn_play_again,menu.btn_return,menu.btn_quit])
                        menu.sprites_list.add([menu.btn_discs,menu.label])
                        game.sprites_list.remove(game.discs)
                        init_game = False
            else:
                for i in range(0,len(menu.btn_discs)):
                    if menu.btn_discs[i].is_clicked():
                        game.set_n_discs(menu.btn_discs[i].value)
                        game.sprites_list.remove(game.discs)
                        game.discs = []
                        game.positions[2].discs = []
                        moves_counter = 0
                        game.draw_discs()
                        init_game = True
                        game_over = False
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            drag = False
            drop = True
    screen.fill(game.WHITE)
    # Title line
    pygame.draw.line(screen, game.BLACK, [0, 60], [SCREEN_WIDTH,60], 5) 
    # Text font,size, bold and italic
    font = pygame.font.SysFont('Calibri', 30, False, False)
    title_font = pygame.font.SysFont('Calibri', 50, False, False)
    # Info Texts
    game_title = title_font.render("MG's Tower of Hanoi ", True, color.BLACK)
    screen.blit(game_title, [((SCREEN_WIDTH/2)-(game_title.get_width()/2)),20])
    if init_game:
        player_moves = font.render("Player moves: "+str(moves_counter), True, color.BLACK)
        min_moves = font.render("Minimum of required movements: "+str(game.min_moves), True, color.BLACK)
        screen.blit(player_moves, [20, 80])
        screen.blit(min_moves, [20, 110])
        if game_over:
            menu.sprites_list.draw(screen)
            if len(game.positions[2].discs) == game.n_discs:
                if moves_counter == game.min_moves:
                    game_over_title = font.render("Congratulations! You just finished the game with the minimums movements! :)", True, color.BLACK)
                    screen.blit(game_over_title, [((SCREEN_WIDTH/2)-(game_over_title.get_width()/2)),SCREEN_HEIGHT/2])
                else:
                    game_over_title = font.render("You just finished the game, now try again with the minimums movements! ;)", True, color.BLACK)
                    screen.blit(game_over_title, [((SCREEN_WIDTH/2)-(game_over_title.get_width()/2)),SCREEN_HEIGHT/2])
        else:
            if drag:
                if move:
                    pos = pygame.mouse.get_pos()
                    game.discs[disc_index].rect.x = pos[0] - (game.discs[disc_index].width/2)
                    game.discs[disc_index].rect.y = pos[1] - (game.discs[disc_index].height/2)
            elif drop:
                if move:
                    current_pos = game.discs[disc_index].current_pos
                    new_pos = None
                    change = False
                    turn_back = True
                    position = pygame.sprite.spritecollideany(game.discs[disc_index],game.pos_sprites_list)
                    if position != None:
                        new_pos = position.pos_index
                        if new_pos != current_pos:
                            disc_length = len(position.discs)
                            if disc_length == 0:
                                turn_back = False
                                change = True
                            elif game.discs[disc_index].id > position.discs[disc_length-1].id:
                                turn_back = False
                                change = True
                    if change:
                        moves_counter = moves_counter + 1
                        game.positions[current_pos].discs.remove(game.discs[disc_index])
                        game.discs[disc_index].current_pos = new_pos
                        game.positions[new_pos].discs.append(game.discs[disc_index])                
                        new_pos_length = len(game.positions[new_pos].discs)
                        game.discs[disc_index].rect.x = game.positions[new_pos].rect.x - ((game.DISC_WIDTH/(game.discs[disc_index].id+1)/2)-(game.DISC_HEIGHT/2))
                        game.discs[disc_index].rect.y = (game.BOARD_Y - game.DISC_HEIGHT) - (game.DISC_HEIGHT*(new_pos_length-1))
                        #Check if the game is over
                        if (len(game.positions[2].discs) == game.n_discs):
                            game_over = True
                            menu.sprites_list.add([menu.btn_play_again,menu.btn_quit,menu.btn_return])
                            menu.sprites_list.remove([menu.label,menu.btn_discs])
                    if turn_back:
                        game.discs[disc_index].rect.x = last_pos[0]
                        game.discs[disc_index].rect.y = last_pos[1]
                    move = False
        game.sprites_list.draw(screen)
    else:
        menu.sprites_list.draw(screen)

    # --- update  screen.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)
pygame.quit()
