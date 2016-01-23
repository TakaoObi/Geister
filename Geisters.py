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

#ボードのマス
board = [0] * 36

#ターンのカウント
Turn_Count = 0

#クリックされたマス
Click_Square = 0

#クリックされた駒の周りの座標格納用, 0:上,1:左,2:右,3:下
Move_Squares = [0] *4

#クリックされたかのフラグ
Click_flag = 0

#自分、相手の駒の数字格納用変数
My_red = 1
My_blue = 2
Enemy_red = 3
Enemy_blue = 4

#取った駒の数の格納用変数
My_red_count = 0
My_blue_Count = 0
Enemy_red_Count = 0
Enemy_blue_Count = 0

#ゲームのターン,偶数で自分,奇数で相手
Game_turn = 0

#マス移動時、その前のクリックしたマスを保存するための変数
My_Click_Piece = 0

#移動するかのフラグ
Move_flag = 0

#勝利条件用フラグ
Win_flag = 0

#マウスのx,y座標
x = 0
y = 0

#カウント用変数（繰り返し利用可能?）
Counter = 0

#文字表示用のフォント
sysfont = pygame.font.SysFont(None, 80)

#以下デバッグ用
#あれば付け足してください




def Set_Pieces(boards = [0]*36, Click_Squares = 0, Counter = 0, Game_turn = 0):

    if Game_turn == 0:
        
        if Counter < 4 and (24 < Click_Squares <29 or 30< Click_Squares <35)\
           and boards[Click_Squares] == 0:
            
                boards[Click_Squares] = My_red
                Click_flag = 0
                Counter += 1

        elif (24 < Click_Squares <29 or 30< Click_Squares <35)\
             and boards[Click_Squares] == 0:
                boards[Click_Squares] = My_blue
                Click_flag = 0
                Counter += 1
                if Counter == 8:
                    Counter = 0
                    Game_turn = 1                  
        else:
                Click_flag = 0

    elif Game_turn == 1:
        
        if Counter < 4 and (0 < Click_Squares < 5 or 6 < Click_Squares < 11) \
           and boards[Click_Squares] == 0:
            
                boards[Click_Squares] = My_red
                Click_flag = 0
                Counter += 1

        elif (0 < Click_Squares < 5 or 6 < Click_Squares < 11) \
             and boards[Click_Squares] == 0:
                boards[Click_Squares] = My_blue
                Click_flag = 0
                Counter += 1
                if Counter == 8:
                    Counter = 0
                    Game_turn = 2                  
        else:
                Click_flag = 0
        

    return Counter, Click_flag, Game_turn


def Click_Squares(x = 0, y = 0):
    if(x < 700 and y < 700):
        Click_Square = int (((x - 100) // 100) + 6 * ((y - 100) // 100))

    return Click_Square
        

#def Move_Piece(Click_Square, board):
    

#def Check_Squares(board, Click_Square):
    

#def Win_Check(Enemy_red_Count, Enemy_blue_Count):
    



while True:
    screen.fill((255,255,255))

    screen.blit(boardImg, (100,100))

    #以下クリックしたマス、座標の表示
    
    hello1 = sysfont.render(str(Click_Square) , False, (0,0,0))
    
    screen.blit(hello1, (10,50))

    hello2 = sysfont.render(str(x) , False, (0,0,0))
    hello3 = sysfont.render(str(y) , False, (0,0,0))
    screen.blit(hello2, (10,100))
    screen.blit(hello3, (10,150))

    if Game_turn < 2:
        if Click_flag == 1:
            Counter, Click_flag, Game_turn = \
                     Set_Pieces(board, Click_Square, Counter, Game_turn)

#    else:
#        Move_Piece(Click_Square, board)

#        Win_Check(Enemy_red_Count, Enemy_blue_Count)

    if(Game_turn % 2 == 1):
        My_red = 3
        My_blue = 4
        Enemy_red = 1
        Enemy_blue = 2
        

    if Move_flag == 1:
        for i in range(4):
            if Move_Squares[i] is not None:
                pygame.draw.rect(screen, (255,255,0), \
                                 Rect(100 + Move_Squares[i] % 6 * 100, \
                                      100 + Move_Squares[i] // 6 * 100, \
                                      200 + Move_Squares[i] % 6 * 100, \
                                      200 + Move_Squares[i] // 6 * 100))

    for i in range(36):
        if board[i] == 1:
            screen.blit(myredImg, (100 + i%6*100, 100 + i//6*100))
        elif board[i] == 2:
            screen.blit(myblueImg, (100 + i%6*100, 100 + i//6*100))
        elif board[i] == 3:
            screen.blit(enemyredImg, (100 + i%6*100, 100 + i//6*100))
        elif board[i] == 4:
            screen.blit(enemyblueImg, (100 + i%6*100, 100 + i//6*100))


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

        
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            Click_flag = 1
            x, y = pygame.mouse.get_pos()
            Click_Square = Click_Squares(int(x), int(y))
            
