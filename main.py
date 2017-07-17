"""
MG's Tower of Hanoi for Python - Main Module
"""
import pygame
import models
import sys
# Define screen constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
# Create game object
game = models.Game(int(sys.argv[1]),SCREEN_WIDTH,SCREEN_HEIGHT)
game.draw_discs()
# Init pygame
pygame.init()
# Define the screen (and it's properties)
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MG's Tower of Hanoi for Python")
# Discs' move variables
done = False
drag = False
drop = False
move = False
game_over = False
init_game = True
disc_index = None
last_pos = [0,0]
# Buttons sprites
btn_play_again = models.Button("Play again",game.BLACK,30,'Calibri',game.GREEN,130,30)
btn_quit = models.Button("Quit",game.BLACK,30,'Calibri',game.RED,70,30)
btn_quit.rect.x = SCREEN_WIDTH/2 + 80
btn_quit.rect.y = SCREEN_HEIGHT/2 - 40
btn_quit.render_text()
btn_play_again.rect.x = SCREEN_WIDTH/2 - 80
btn_play_again.rect.y = SCREEN_HEIGHT/2 - 40
btn_play_again.render_text()
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
                    if btn_quit.is_clicked():
                        done = True
                    if btn_play_again.is_clicked():
                        game.sprites_list.remove(game.discs)
                        game.positions[2].discs = []
                        moves_counter = 0
                        game.discs = []
                        game.draw_discs()
                        game.sprites_list.remove([btn_play_again,btn_quit])
                        game_over = False
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
    game_title = title_font.render("MG's Tower of Hanoi ", True, game.BLACK)
    screen.blit(game_title, [((SCREEN_WIDTH/2)-(game_title.get_width()/2)),20])
    if init_game:
        player_moves = font.render("Player moves: "+str(moves_counter), True, game.BLACK)
        min_moves = font.render("Minimum of required movements: "+str(game.min_moves), True, game.BLACK)

        screen.blit(player_moves, [20, 80])
        screen.blit(min_moves, [20, 110])
        if game_over:
            if len(game.positions[2].discs) == game.n_discs:
                if moves_counter == game.min_moves:
                    game_over_title = font.render("Congratulations! You just finished the game with the minimums movements! :)", True, game.BLACK)
                    screen.blit(game_over_title, [((SCREEN_WIDTH/2)-(game_over_title.get_width()/2)),SCREEN_HEIGHT/2])
                else:
                    game_over_title = font.render("You just finished the game, now try again with the minimums movements! ;)", True, game.BLACK)
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
                            game.sprites_list.add(btn_quit)
                            game.sprites_list.add(btn_play_again)
                    if turn_back:
                        game.discs[disc_index].rect.x = last_pos[0]
                        game.discs[disc_index].rect.y = last_pos[1]
                    move = False
        game.sprites_list.draw(screen)
    # --- update  screen.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)
pygame.quit()
