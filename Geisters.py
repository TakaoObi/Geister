import pygame
from pygame.locals import *
import sys
 
SCREEN_SIZE = (1200, 800)
 
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"ガイスター")

boardImg = pygame.image.load("board.png").convert()
myredImg = pygame.image.load("myred.png").convert()
myblueImg = pygame.image.load("myblue.png").convert()
enemyredImg = pygame.image.load("otherred.png").convert()
enemyblueImg = pygame.image.load("otherblue.png").convert()

board_mass = [0] * 36

turn_count = 0

click_mass = 0
click_check = 0

game_turn = 0

sysfont = pygame.font.SysFont(None, 80)

x = 0
y = 0



while True:
    screen.fill((255,255,255))

    screen.blit(boardImg, (100,100))
    
    hello1 = sysfont.render(str(click_mass) , False, (0,0,0))
    
    screen.blit(hello1, (10,50))


    hello2 = sysfont.render(str(x) , False, (0,0,0))
    hello3 = sysfont.render(str(y) , False, (0,0,0))
    screen.blit(hello2, (10,100))
    screen.blit(hello3, (10,150))

    if game_turn == 0 and click_check == 1:
        if turn_count < 5 and (24 < click_mass <29 or 30<click_mass<35):
            board_mass[int(click_mass)] = 1
            click_check = 0
        elif 24 < click_mass <29 or 30<click_mass<35:
            board_mass[int(click_mass)] = 2
            click_check = 0
            if turn_count == 8:
                turn_count = 0
                game_turn = 1
        else:
            click_check = 0
            turn_count -= 1

    hello4 = sysfont.render(str(turn_count) , False, (0,0,0))
    screen.blit(hello4, (10,200))
        

    for i in range(36):
        if board_mass[i] == 1:
            screen.blit(myredImg, (100 + i%6*100, 100 + i//6*100))
        elif board_mass[i] == 2:
            screen.blit(myblueImg, (100 + i%6*100, 100 + i//6*100))


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

        
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            click_check = 1
            x, y = pygame.mouse.get_pos()
            click_mass = int(((x - 100) // 100) + 6 * ((y - 100) // 100))
            turn_count += 1
