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
Board = [0] * 36

#クリックされたマス
ClickSquare = 0

#クリックされた駒の周りの座標格納用, 0:上,1:左,2:右,3:下
MoveSquares = [0] *4

#クリックされたかのフラグ
ClickFlag = 0

#自分、相手の駒の数字格納用変数
MyRed = 1
MyBlue = 2
EnemyRed = 3
EnemyBlue = 4

#取った駒の数の格納用変数
MyRedCount = 0
MyBlueCount = 0
EnemyRedCount = 0
EnemyBlueCount = 0

#ゲームのターン,偶数で自分,奇数で相手
GameTurn = 0

#前ループでのターンのカウント(ボード入れ替え用)
BackGameTurn = 0

#マス移動時、その前のクリックしたマスを保存するための変数
MyClickPiece = 0

#移動するかのフラグ
MoveFlag = 0

#勝利条件用フラグ
WinFlag = 0

#マウスのx,y座標
x = 0
y = 0

#カウント用変数（繰り返し利用可能?）
Counter = 0

#文字表示用のフォント
sysfont = pygame.font.SysFont(None, 80)
startfont = pygame.font.SysFont(None, 150)

#コマ選択or移動先選択のクリック識別
MoveClickFlag = False

#ターン変更表示用変数
TurnChange = 1

#ターン変更時文字表示
OneStart = startfont.render("1P Start" , False, (0,0,255))
TwoStart = startfont.render("2P Start" , False, (255,0,0))
OneWin = startfont.render("1P Win" , False, (0,0,255))
TwoWin = startfont.render("2P Win" , False, (255,0,0))
OnePlayer = startfont.render("1P" , False, (0,0,255))
TwoPlayer = startfont.render("2P" , False, (255,0,0))


#駒設置関数
def Set_Pieces(Board = [0]*36, ClickSquare = 0, Counter = 0, GameTurn = 0):

    if GameTurn == 0 or GameTurn == 1:

        if Counter == 8:
            
                Counter = 0
                GameTurn += 1
                ClickFlag = 0

        
        elif Counter < 4 and (24 < ClickSquare <29 or 30< ClickSquare <35)\
            and Board[ClickSquare] == 0:
            
                Board[ClickSquare] = MyRed
                ClickFlag = 0
                Counter += 1


        elif Counter < 8 and (24 < ClickSquare <29 or 30< ClickSquare <35)\
            and Board[ClickSquare] == 0:
            
                Board[ClickSquare] = MyBlue
                ClickFlag = 0
                Counter += 1

                          
        else:
            
             ClickFlag = 0
       

    return Counter, ClickFlag, GameTurn


#クリックしたマスを返す関数
#クリックと共にClick_Squareにマスの数字が入ります
def Click_Squares(x = 0, y = 0, ClickSquare = 0):

    ClickFlag = 0
    
    if(100 < x < 700 and 100 < y < 700):
        
        ClickSquare = int (((x - 100) // 100) + 6 * ((y - 100) // 100))
        ClickFlag = 1
        

    return ClickSquare, ClickFlag


#駒移動用関数
def Move_Piece(Board = [0] * 36, ClickSquare = 0, MyClickPiece = 0,\
               MoveSquares = [0] * 4, GameTurn = 0,\
               EnemyRedCount = 0, EnemyBlueCount = 0, \
               ClickFlag = 0, Counter = 0):

    if(Counter == 1 and ClickFlag == 1):
        GameTurn += 1
        Counter = 0
        MoveFlag = 0
        ClickFlag = 0
        MoveClickFlag = False

        return GameTurn, MoveFlag, MoveClickFlag, ClickSquare,\
           EnemyRedCount, EnemyBlueCount, ClickFlag, Counter
    

    if(ClickSquare in MoveSquares):
        
        if Board[ClickSquare] == EnemyRed :
            
            EnemyRedCount += 1
                
        elif Board[ClickSquare] == EnemyBlue :
            
            EnemyBlueCount += 1
                
        Board[ClickSquare] = Board[MyClickPiece]
        Board[MyClickPiece] = 0
        MoveFlag = 0
        MoveClickFlag = False
        MoveSquares = [None, None, None, None]
        ClickSquare = 36
        Counter = 1
        
        
    elif(ClickSquare != MyClickPiece):
        
        MoveFlag = 0
        MoveClickFlag = False

        
    else :
        
        MoveFlag = 1
        MoveClickFlag = True

    ClickFlag = 0
        
    return GameTurn, MoveFlag, MoveClickFlag, ClickSquare,\
           EnemyRedCount, EnemyBlueCount, ClickFlag, Counter

    
#移動可能マス指定関数

def Check_Squares(Board = [0] * 36, ClickSquare = 0, ):
  
    if(Board[ClickSquare] == MyRed)or(Board[ClickSquare] == MyBlue):
        
        U = (ClickSquare - 6)
        D = (ClickSquare + 6)
        L = (ClickSquare - 1)
        R = (ClickSquare + 1)
        
        if U < 0:
            
            U = None
            
        elif (Board[U] == MyBlue) or (Board[U] == MyRed) :
            
            U = None
            
        if D > 35:
            
            D = None
            
        elif (Board[D] == MyBlue) or (Board[D] == MyRed):
            
            D = None

        if L < 0:
            
            L = None
            
        elif (Board[L] == MyBlue) or (Board[L] == MyRed) or (L % 6 == 5):

            L = None
            
        if R > 35:
            
            R = None
            
        elif (Board[R] == MyBlue) or (Board[R] == MyRed) or (R % 6 == 0):
            
            R = None


    else:

        U, D, L, R = None, None, None, None
        
        
    if (U == None) and (D == None) and (L == None) and (R == None):
        
        MoveFlag = 0
        MoveClickFlag = False
        MyClickPiece = 0
        
    else:
        
        MoveFlag = 1  
        MoveClickFlag = True
        MyClickPiece = ClickSquare
        
        
    MoveSquares = [U,D,L,R]    
    ClickFlag = 0
    
    return ClickFlag , MoveSquares, MoveFlag ,MoveClickFlag , MyClickPiece
        

    
#勝利条件判定関数

#勝利条件（駒）
def Win_Check(EnemyRedCount = 0, EnemyBlueCount = 0,\
              WinFlag = 0, GameTurn = 0):

    if (EnemyRedCount == 4):
        
        WinFlag = 1
        GameTurn -= 1
        return WinFlag, GameTurn
    

    elif (EnemyBlueCount == 4):
        
        WinFlag = 2
        GameTurn -= 1
        return WinFlag, GameTurn
    

    else:
        
        WinFlag = 0
        return WinFlag, GameTurn

    
#勝利条件（脱出）
def Twice_Win_Check(Board = [0] * 36, WinFlag = 0):
    
    if (Board[0] == MyBlue) or (Board[5] == MyBlue):

        WinFlag = 2
        return WinFlag

    else:
        return WinFlag


#これ以降がループ部分
while True:
    
    #スクリーンの背景色指定
    screen.fill((255,255,255))


    #ターン表示用if
    if TurnChange == 0:

        #駒設置部分
        if GameTurn < 2:
            
            if ClickFlag == 1:
                
                Counter, ClickFlag, GameTurn =\
                         Set_Pieces(Board, ClickSquare, Counter, GameTurn)
                
            
        #これ以降がゲームのメインループ
        else:
            
            WinFlag = Twice_Win_Check(Board, WinFlag)

            if WinFlag == 0:
            
                if (MoveClickFlag == False) and ( -1 < ClickSquare < 36 ) and\
                   (Counter == 0):
                    
                    ClickFlag, MoveSquares, MoveFlag,\
                    MoveClickFlag, MyClickPiece =\
                               Check_Squares(Board, ClickSquare)
                    
                else:
                    
                    GameTurn , MoveFlag , MoveClickFlag, ClickSquare,\
                    EnemyRedCount, EnemyBlueCount, ClickFlag, Counter = \
                              Move_Piece(Board, ClickSquare, MyClickPiece,\
                                         MoveSquares, GameTurn,\
                                         EnemyRedCount, EnemyBlueCount,\
                                         ClickFlag, Counter)
                
    
                WinFlag, GameTurn = Win_Check(EnemyRedCount,\
                                              EnemyBlueCount,\
                                              WinFlag, GameTurn)
    


    #ターンごとのMy, Other, ボードの切り替え
    if(BackGameTurn != GameTurn):
        
        for i in range(18):
            Board[i], Board[35-i] = Board[35-i], Board[i]
            
        MyRed, EnemyRed = EnemyRed, MyRed
        MyBlue, EnemyBlue = EnemyBlue, MyBlue
        MyRedCount, EnemyRedCount = EnemyRedCount, MyRedCount
        MyBlueCount, EnemyBlueCount = EnemyBlueCount, MyBlueCount
        TurnChange = 1
        

    BackGameTurn = GameTurn



    #これ以降画像表示

    #ボードの画像表示
    if TurnChange == 0 and WinFlag == 0:
    
        screen.blit(boardImg, (100,100))
                
        #ボード上の駒の表示
        for i in range(36):
            
            if Board[i] == 1:
                screen.blit(myredImg, (100 + i%6*100, 100 + i//6*100))
                
            elif Board[i] == 2:
                screen.blit(myblueImg, (100 + i%6*100, 100 + i//6*100))
                
            elif Board[i] == 3:
                screen.blit(enemyredImg, (100 + i%6*100, 100 + i//6*100))
                
            elif Board[i] == 4:
                screen.blit(enemyblueImg, (100 + i%6*100, 100 + i//6*100))


        #光るマスの表示
        if MoveFlag == 1:
            
            for i in range(4):
                
                if MoveSquares[i] is not None:
                    
                    pygame.draw.rect(screen, (255,255,0),\
                                     Rect(100 + MoveSquares[i] % 6 * 100,\
                                          100 + MoveSquares[i] // 6 * 100,\
                                          100, 100), 5)

        #取った駒の表示
        if(GameTurn % 2 == 0):
            
            for i in range(MyRedCount):
                screen.blit(myredImg, (750 + i*100, 200))
                
            for i in range(MyBlueCount):
                screen.blit(myblueImg, (750 + i*100, 300))
                
            for i in range(EnemyRedCount):
                screen.blit(enemyredImg, (750 + i*100, 500))
                
            for i in range(EnemyBlueCount):
                screen.blit(enemyblueImg, (750 + i*100, 600))
                
        else:
            
            for i in range(MyRedCount):
                screen.blit(enemyredImg, (750 + i*100, 200))
                
            for i in range(MyBlueCount):
                screen.blit(enemyblueImg, (750 + i*100, 300))
                
            for i in range(EnemyRedCount):
                screen.blit(myredImg, (750 + i*100, 500))
                
            for i in range(EnemyBlueCount):
                screen.blit(myblueImg, (750 + i*100, 600))
            

    #ターン表示 勝利表示
    else:

        if WinFlag != 0:
            
            if GameTurn % 2 == 1:
                
                if WinFlag == 2:
                    screen.blit(TwoWin, (100,300))
                    
                else:
                    screen.blit(OneWin, (100,300))
                    
            else:
                
                if WinFlag == 2:
                    screen.blit(OneWin, (100,300))
                    
                else:
                    screen.blit(TwoWin, (100,300))

        else:
            
            if GameTurn % 2 == 1:
                screen.blit(TwoStart, (100,300))
                
            else:
                screen.blit(OneStart, (100,300))

            if ClickFlag == 1:
                
                TurnChange = 0;
                ClickFlag = 0;
                ClickSquare = 36
                    
        
    

    #画面の更新
    pygame.display.update()

    
    #イベントの取得
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            
        
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            ClickFlag = 1
            x, y = pygame.mouse.get_pos()
            ClickSquare, ClickFlag = Click_Squares(int(x), int(y), ClickSquare)
            

