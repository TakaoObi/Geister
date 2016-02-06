import pygame
from pygame.locals import *
import sys

#スクリーンサイズ指定 
SCREEN_SIZE = (1200, 800)

#スクリーンの設定等 
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"ガイスター")

#画像の指定
boardImg = pygame.image.load("board.png").convert()
myredImg = pygame.image.load("myred.png").convert()
myblueImg = pygame.image.load("myblue.png").convert()
enemyredImg = pygame.image.load("otherred.png").convert()
enemyblueImg = pygame.image.load("otherblue.png").convert()

#ボードのマス
board = [0] * 36

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
My_red_Count = 0
My_blue_Count = 0
Enemy_red_Count = 0
Enemy_blue_Count = 0

#ゲームのターン,偶数で自分,奇数で相手
Game_turn = 0

#前ループでのターンのカウント(ボード入れ替え用)
Back_Game_turn = 0

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

#コマ選択or移動先選択のクリック識別
Move_Click_flag = False

#ターン変更表示用変数
Turn_Change = 1

#ターン変更時文字表示
startfont = pygame.font.SysFont(None, 150)
One_Start = startfont.render("1P Start" , False, (0,0,255))
Two_Start = startfont.render("2P Start" , False, (255,0,0))
One_Win = startfont.render("1P Win" , False, (0,0,255))
Two_Win = startfont.render("2P Win" , False, (255,0,0))
One_Player = startfont.render("1P" , False, (0,0,255))
Two_Player = startfont.render("2P" , False, (255,0,0))


#以下デバッグ用
#あれば付け足してください



#駒設置関数、駒配置後一回クリックしてください
def Set_Pieces(boards = [0]*36, Click_Squares = 0, Counter = 0, Game_turn = 0):

    if Game_turn == 0 or Game_turn == 1:

        if Counter == 8:
                Counter = 0
                Game_turn += 1
                Click_flag = 0

        
        elif Counter < 4 and (24 < Click_Squares <29 or 30< Click_Squares <35)\
           and boards[Click_Squares] == 0:
            
                boards[Click_Squares] = My_red
                Click_flag = 0
                Counter += 1

        elif Counter < 8 and (24 < Click_Squares <29 or 30< Click_Squares <35)\
             and boards[Click_Squares] == 0:
                boards[Click_Squares] = My_blue
                Click_flag = 0
                Counter += 1
                          
        else:
             Click_flag = 0
       

    return Counter, Click_flag, Game_turn


#クリックしたマスを返す関数
#クリックと共にClick_Squareにマスの数字が入ります
def Click_Squares(x = 0, y = 0, Click_Square = 0):
    if(100 < x < 700 and 100 < y < 700):
        Click_Square = int (((x - 100) // 100) + 6 * ((y - 100) // 100))

    return Click_Square

    
        
#以下、作成していない部分はコメントアウト


#駒移動用関数

def Move_Piece(Click_Square, boards, My_Click_Piece, Move_Squares, game_turn,\
               Enemy_red_Count, Enemy_blue_Count, Click_flag):
   
    if(Click_Square in Move_Squares):
        
        if boards[Click_Square] == Enemy_red :
            Enemy_red_Count += 1
                
        elif boards[Click_Square] == Enemy_blue :
            Enemy_blue_Count += 1
                
        boards[Click_Square] = boards[My_Click_Piece]
        boards[My_Click_Piece]=0
        Move_flag =0
        Move_Click_flag=0
        Move_Squares=[None,None,None,None]
        Click_Square = 36
        game_turn += 1
        
    elif(Click_Square != My_Click_Piece):
        
        
        Move_Click_flag = 0
        Move_flag = 0
    else :
        Move_flag =1
        Move_Click_flag =1

    Click_flag = 0
        
    return game_turn , Move_flag , Move_Click_flag , Click_Square ,\
           Enemy_red_Count, Enemy_blue_Count, Click_flag

    
#移動可能マス指定関数

def Check_Squares(boards, Click_Squares):
    if(boards[Click_Squares] == My_red)or(boards[Click_Squares] == My_blue):
        U = (Click_Squares - 6)
        D = (Click_Squares + 6)
        L = (Click_Squares - 1)
        R = (Click_Squares + 1)
        if U < 0:
            U = None
        elif (boards[U] == My_blue) or (boards[U] == My_red) :
            U = None
            
        if D > 35:
            D = None
            
        elif (boards[D] == My_blue) or (boards[D] == My_red):
            D = None

        if L < 0:
            L = None
        elif (boards[L] == My_blue) or (boards[L] == My_red) or (L % 6 == 5):
            L = None
        if R > 35:
            R = None
        elif (boards[R] == My_blue) or (boards[R] == My_red) or (R % 6 == 0):
            R = None

    else:
        U,D,L,R = None,None,None,None 
    if (U == None)and(D == None)and(L == None)and(R == None):
        Move_flag = 0
        Move_Click_flag = 0
        My_Click_Piece = 0
    else:
        Move_flag = 1  
        Move_Click_flag = 1
        My_Click_Piece = Click_Squares 
        
    Move_Squares = [U,D,L,R]    
    Click_flag = 0
    
    return Click_flag , Move_Squares, Move_flag ,Move_Click_flag ,\
           My_Click_Piece
        
    
#勝利条件判定関数
#勝利条件（駒）
def Win_Check(Enemy_red_Count, Enemy_blue_Count, Win_flag, Game_turn):

    if (Enemy_red_Count == 4):
        Win_flag = 1
        Game_turn -= 1
        return Win_flag, Game_turn

    elif (Enemy_blue_Count == 4):
        Win_flag = 2
        Game_turn -= 1
        return Win_flag, Game_turn

    else:
        Win_flag = 0
        return Win_flag, Game_turn

#勝利条件（脱出）
def Twice_Win_Check(board, Win_flag):
    
    if  (board[0] == My_blue)or(board[5] == My_blue):
        Win_flag = 2
        return Win_flag

    else:
        return Win_flag  


#これ以降がループ部分
while True:
    
    #スクリーンの背景色指定
    screen.fill((255,255,255))

    

    #以下クリックしたマス、座標の文字表示
    
    hello1 = sysfont.render(str(Click_Square) , False, (0,0,0))
    
    screen.blit(hello1, (10,50))

    hello2 = sysfont.render(str(x) , False, (0,0,0))
    hello3 = sysfont.render(str(y) , False, (0,0,0))
    hello4 = sysfont.render(str(Move_Squares) , False, (0,0,0))    
    screen.blit(hello2, (10,100))
    screen.blit(hello3, (10,150))
    screen.blit(hello4, (800,150))


    #ここまで

    #ターン表示のためにif文を追加しました
    if Turn_Change == 0:

        #駒設置部分
        if Game_turn < 2:
            if Click_flag == 1:
                Counter, Click_flag, Game_turn = \
                         Set_Pieces(board, Click_Square, Counter, Game_turn)
            
        #これ以降がゲームのメインループ
        else:
            Win_flag = Twice_Win_Check(board, Win_flag)

            if Win_flag == 0:
            
                if (Move_Click_flag == False) and (-1 < Click_Square < 36 ):
                    Click_flag, Move_Squares, Move_flag,\
                    Move_Click_flag, My_Click_Piece =\
                               Check_Squares(board, Click_Square)
                else:
                    Game_turn , Move_flag , Move_Click_flag, Click_Square,\
                              Enemy_red_Count, Enemy_blue_Count, Click_flag = \
                              Move_Piece(Click_Square, board, My_Click_Piece,\
                                         Move_Squares, Game_turn,\
                                         Enemy_red_Count, Enemy_blue_Count,
                                         Click_flag)
    
                Win_flag, Game_turn = Win_Check(Enemy_red_Count, \
                                                Enemy_blue_Count, \
                                                Win_flag, Game_turn)
    



    #ターンごとのMy,Otherの切り替え,ボードも切りかえ
    if(Game_turn % 2 == 1):
        My_red = 3
        My_blue = 4
        Enemy_red = 1
        Enemy_blue = 2
        screen.blit(Two_Player, (800,50))
        
    else:
        My_red = 1
        My_blue = 2
        Enemy_red = 3
        Enemy_blue = 4
        screen.blit(One_Player, (800,50))

    if(Back_Game_turn != Game_turn):
        Turn_Change = 1
        for i in range(18):
            board[i], board[35-i] = board[35-i], board[i]
        My_red_Count, Enemy_red_Count = Enemy_red_Count, My_red_Count
        My_blue_Count, Enemy_blue_Count = Enemy_blue_Count, My_blue_Count

    Back_Game_turn = Game_turn


    #これ以降画像表示

    #ボードの画像表示
    #ターン表示のためif文を追加しました
    if Turn_Change == 0 and Win_flag == 0:
    
        screen.blit(boardImg, (100,100))

                
        #ボード上の駒の表示
        for i in range(36):
            if board[i] == 1:
                screen.blit(myredImg, (100 + i%6*100, 100 + i//6*100))
            elif board[i] == 2:
                screen.blit(myblueImg, (100 + i%6*100, 100 + i//6*100))
            elif board[i] == 3:
                screen.blit(enemyredImg, (100 + i%6*100, 100 + i//6*100))
            elif board[i] == 4:
                screen.blit(enemyblueImg, (100 + i%6*100, 100 + i//6*100))


        #光るマスの表示
        if Move_flag == 1:
            for i in range(4):
                if Move_Squares[i] is not None:
                    pygame.draw.rect(screen, (255,255,0), \
                                     Rect(100 + Move_Squares[i] % 6 * 100, \
                                          100 + Move_Squares[i] // 6 * 100, \
                                          100, 100), 5)

        #取った駒の表示
        if(Game_turn % 2 == 1):
            for i in range(My_red_Count):
                screen.blit(myredImg, (750 + i*100, 200))
            for i in range(My_blue_Count):
                screen.blit(myblueImg, (750 + i*100, 300))
            for i in range(Enemy_red_Count):
                screen.blit(enemyredImg, (750 + i*100, 500))
            for i in range(Enemy_blue_Count):
                screen.blit(enemyblueImg, (750 + i*100, 600))
        else:
            for i in range(My_red_Count):
                screen.blit(enemyredImg, (750 + i*100, 200))
            for i in range(My_blue_Count):
                screen.blit(enemyblueImg, (750 + i*100, 300))
            for i in range(Enemy_red_Count):
                screen.blit(myredImg, (750 + i*100, 500))
            for i in range(Enemy_blue_Count):
                screen.blit(myblueImg, (750 + i*100, 600))
            

    #ターン表示 勝利表示
    else:

        if Win_flag != 0:
            if Game_turn % 2 == 1:
                if Win_flag == 2:
                    screen.blit(Two_Win, (100,300))
                else:
                    screen.blit(One_Win, (100,300))
            else:
                if Win_flag == 2:
                    screen.blit(One_Win, (100,300))
                else:
                    screen.blit(Two_Win, (100,300))

        else:
            if Game_turn % 2 == 1:
                screen.blit(Two_Start, (100,300))
            else:
                screen.blit(One_Start, (100,300))

            if Click_flag == 1:
                Turn_Change = 0;
                Click_flag = 0;
                    
        
    

    #画面の更新
    pygame.display.update()

    
    #イベントの取得
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            
        
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            Click_flag = 1
            x, y = pygame.mouse.get_pos()
            Click_Square = Click_Squares(int(x), int(y), Click_Square)
            
