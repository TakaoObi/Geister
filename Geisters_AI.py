import pygame
from pygame.locals import *
import sys
import random
import time

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
mypieceImg = pygame.image.load("mypiece.png").convert()
enemypieceImg = pygame.image.load("otherpiece.png").convert()

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
TwiceWinFlag = 0
WinCount = 0

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

#以下ＡＩ用変数

#初期設置(乱数)
AiSetPieces = [3] * 4 + [4] * 4
random.shuffle(AiSetPieces)

#自、ＡＩ駒青、赤位置
MyBluePosition = [0] * 4
MyRedPosition = [0] * 4
AiBluePosition = [0] * 4
AiRedPosition = [0] * 4

#相手の手予測用
MyPosition = [0] * 8
MyProbability = [0] * 8


#駒設置関数
def Set_Pieces(Board = [0]*36, ClickSquare = 0, Counter = 0, GameTurn = 0,\
               MyPositon = [0]*8):

    if GameTurn == 0:

        if Counter == 8:
            
                Counter = 0
                GameTurn += 1
                ClickFlag = 0

        
        elif Counter < 4 and (24 < ClickSquare <29 or 30< ClickSquare <35)\
            and Board[ClickSquare] == 0:
            
                Board[ClickSquare] = MyRed
                MyPosition[Counter] = 35 - ClickSquare
                ClickFlag = 0
                Counter += 1


        elif Counter < 8 and (24 < ClickSquare <29 or 30< ClickSquare <35)\
            and Board[ClickSquare] == 0:
            
                Board[ClickSquare] = MyBlue
                MyPositon[Counter] = 35 - ClickSquare
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
#同時に駒の期待値変更
def Move_Piece(Board = [0] * 36, ClickSquare = 0, MyClickPiece = 0,\
               MoveSquares = [0] * 4, GameTurn = 0,\
               MyRedCount = 0, MyBlueCount = 0,\
               MyPosition = [0]*8, MyProbability = [0]*8,\
               AiRedPosition = [0]*4, AiBluePosition = [0]*4,\
               ClickFlag = 0, Counter = 0):

    if(Counter == 1 and ClickFlag == 1):
        GameTurn += 1
        Counter = 0
        MoveFlag = 0
        ClickFlag = 0
        MoveClickFlag = False

        return GameTurn, MoveFlag, MoveClickFlag, ClickSquare,\
               MyRedCount, MyBlueCount,\
               MyPosition, MyProbability, AiRedPosition, AiBluePosition,\
               ClickFlag, Counter
    

    if(ClickSquare in MoveSquares):
        
        if Board[ClickSquare] == 3 :
            
            MyRedCount += 1
            for i in range(4):
                if(AiRedPosition[i] == 35 - ClickSquare):
                    AiRedPosition[i] = None
            for i in range(8):
                if(MyPosition[i] == 35 - MyClickPiece):
                    MyProbability[i] += 2
                
        elif Board[ClickSquare] == 4 :
            
            MyBlueCount += 1
            for i in range(4):
                if(AiBluePosition[i] == 35 - ClickSquare):
                    AiBluePosition[i] = None
            for i in range(8):
                if(MyPosition[i] == 35 - MyClickPiece):
                    MyProbability[i] += 2

        if(ClickSquare > 5 and (Board[ClickSquare - 6] == 3 or Board[ClickSquare - 6] == 4)):
            for i in range(8):
                if(MyPosition[i] == 35 - MyClickPiece):
                    MyProbability[i] += 3
        elif(ClickSquare % 6 != 0 and (Board[ClickSquare - 1] == 3 or Board[ClickSquare - 1] == 4)):
            for i in range(8):
                if(MyPosition[i] == 35 - MyClickPiece):
                    MyProbability[i] += 3
        elif(ClickSquare % 6 != 5 and (Board[ClickSquare + 1] == 3 or Board[ClickSquare + 1] == 4)):
            for i in range(8):
                if(MyPosition[i] == 35 - MyClickPiece):
                    MyProbability[i] += 3
        elif(ClickSquare < 30  and (Board[ClickSquare + 6] == 3 or Board[ClickSquare + 6] == 4)):
            for i in range(8):
                if(MyPosition[i] == 35 - MyClickPiece):
                    MyProbability[i] += 3

        if( int(ClickSquare / 6 + ClickSquare % 6) < 5):
            for i in range(8):
                if(MyPosition[i] == 35 - MyClickPiece):
                    MyProbability[i] -= 5 - int(ClickSquare / 6 + ClickSquare % 6)

        for i in range(8):
            if(MyPosition[i] == 35 - MyClickPiece):
                
                for j in range(4):
                    if(MoveSquares[j] is not None):
                        if(ClickSquare == MoveSquares[j]):
                            if(j == 0):
                                MyProbability[i] += 1
                            elif(j == 1):
                                MyProbability[i] -= 1
                            elif(j == 2 and MyPosition[i] % 6 <= 3):
                                MyProbability[i] -= 1
                            elif(j == 3 and MyPosition[i] % 6 >= 4):
                                MyProbability[i] -= 1
                                
                MyPosition[i] = 35 - ClickSquare
                                
            
                
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
           MyRedCount, MyBlueCount,\
           MyPosition, MyProbability, AiRedPosition, AiBluePosition,\
           ClickFlag, Counter
           

    
#移動可能マス指定関数

def Check_Squares(Board = [0] * 36, ClickSquare = 0):
  
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

    if (EnemyRedCount == 4 or MyBlueCount == 4):
        
        WinFlag = 1
        GameTurn -= 1
        return WinFlag, GameTurn
    

    elif (EnemyBlueCount == 4 or MyRedCount == 4):
        
        WinFlag = 2
        GameTurn -= 1
        return WinFlag, GameTurn
    

    else:
        
        return WinFlag, GameTurn

    
#勝利条件（脱出）
def Twice_Win_Check(Board = [0] * 36, WinFlag = 0, TwiceWinFlag = 0, GameTurn = 0, WinCount = 0, ClickFlag = 0):
    
    if ((Board[0] == 2 or Board[5] == 2) and GameTurn % 2 == 0 and WinCount == 0):


        if(TwiceWinFlag == 1):

            if(ClickFlag == 1):              
                WinFlag = 1
            
            return WinFlag, TwiceWinFlag, WinCount
        
        else:
            
            TwiceWinFlag = 1
            return WinFlag, TwiceWinFlag, WinCount
            

    elif((Board[0] == 4 or Board[5] == 4) and GameTurn % 2 == 1 and WinCount == 0):

        if(TwiceWinFlag == 2):
            
            WinFlag = 2
            return WinFlag, TwiceWinFlag, WinCount
        
        else:
            
            TwiceWinFlag = 2
            return WinFlag, TwiceWinFlag, WinCount

    WinCount = 1
        
    return WinFlag, TwiceWinFlag, WinCount


#以下ＡＩ用関数
   
#ＡＩ駒設置、乱数で設置
def AI_Set_Pieces(Board = [0] * 36, AiSetPieces = [3]*4 + [4]*4, ClickFlag = 0, \
                  GameTurn = 0, Counter = 0, AiRedPosition = [0] * 4, AiBluePosition = [0] * 4):

    if(Counter == 1 and ClickFlag == 1):

        GameTurn += 1
        ClickFlag = 0
        Counter = 0

        return ClickFlag, GameTurn, Counter, AiRedPosition, AiBluePosition

    
    else:
        
        for i in range(4):
            Board[25 + i] = AiSetPieces[i]
            if AiSetPieces[i] == 3:
                for j in range(4):
                    if AiRedPosition[j] == 0:
                        AiRedPosition[j] = 25 + i
                        break
            else:
                for j in range(4):
                    if AiBluePosition[j] == 0:
                        AiBluePosition[j] = 25 + i
                        break

                
        for i in range(4):
            Board[31 + i] = AiSetPieces[i+4]
            if AiSetPieces[i+4] == 3:
                for j in range(4):
                    if AiRedPosition[j] == 0:
                        AiRedPosition[j] = 31 + i
                        break
            else:
                for j in range(4):
                    if AiBluePosition[j] == 0:
                        AiBluePosition[j] = 31 + i
                        break

        Counter = 1

    
    ClickFlag = 0
    

    return ClickFlag, GameTurn, Counter, AiRedPosition, AiBluePosition


#ＡＩ移動関数、内部
#青の距離チェック
def AI_Blue_Check(AiBluePositon = [0]*4, MyRedPosition = [0]*4,\
                  MyBluePosition = [0]*4, DecidePiece = [0]*3):

    #青距離測定用
    #[0]からと[4]から、４個ずつ
    BlueDistance = [0] * 8 

    for i in range(4):
        if(AiBluePosition[i] is not None):
            BlueDistance[i] = int((AiBluePosition[i] // 6) + (AiBluePosition[i] % 6))
        else:
            BlueDistance[i] = None
    for i in range(4):
        if(AiBluePosition[i] is not None):
            BlueDistance[i+4] = int((AiBluePosition[i] // 6) + (5 - AiBluePosition[i] % 6))
        else:
            BlueDistance[i+4] = None

    for i in range(4):
        if(BlueDistance[i] is not None):
            for j in range(4):
                if(MyBluePosition[j] is not None):
                    if BlueDistance[i] >= int((MyBluePosition[j] // 6) + (MyBluePosition[j] % 6)):
                        break
                if(MyRedPosition[j] is not None):
                    if BlueDistance[i] >= int((MyRedPosition[j] // 6) + (MyRedPosition[j] % 6)):
                        break
                if(j == 3):
                    DecidePiece[0] = 2
                    DecidePiece[1] = i+1
                    if(AiBluePosition[i] < 6):
                        DecidePiece[2] = 2
                    else:
                        DecidePiece[2] = 1

                    return DecidePiece
            
        if(BlueDistance[i+4] is not None):
            for j in range(4):
                if(MyBluePosition[j] is not None):
                    if BlueDistance[i+4] >= int((MyBluePosition[j] // 6) + (5 - MyBluePosition[j] % 6)):
                        break
                if(MyRedPosition[j] is not None):
                    if BlueDistance[i+4] >= int((MyRedPosition[j] // 6) + (5 - MyRedPosition[j] % 6)):
                        break
                if(j == 3):
                    DecidePiece[0] = 2
                    DecidePiece[1] = i+1
                    if(AiBluePosition[i] < 6):
                        DecidePiece[2] = 3
                    else:
                        DecidePiece[2] = 1

                    return DecidePiece

    return DecidePiece
                    

#通常移動
def AI_Normal_Move(Board = [0]*36, AiRedPosition = [0]*4, AiBluePosition = [0]*4, DecidePiece = [0]*3):
    
    #通常移動における周囲の期待値(上、左、右、下)
    AroundExpectation = [0] * 4

    #Max期待値
    MaxExpectation = 0

    #赤処理
    for i in range(4):
        if(AiRedPosition[i] is not None):
                    
            #前にプラス
            if(AiRedPosition[i] > 5):
                AroundExpectation[0] += 2
        
            #横にプラス(一応左優先で)
            if(AiRedPosition[i] % 6 != 0):
                AroundExpectation[1] += 1
            elif(AiRedPosition[i] % 6 != 5):
                AroundExpectation[2] += 1
        
            #周囲の敵を食べる
            if(AiRedPosition[i] > 5):
                if(Board[AiRedPosition[i] - 6] == 1):
                    AroundExpectation[0] += 3 * (2 - EnemyRedCount)
                elif(Board[AiRedPosition[i] - 6] == 2):
                    AroundExpectation[0] += 6
            if(AiRedPosition[i] % 6 != 0):
                if(Board[AiRedPosition[i] - 1] == 1):
                    AroundExpectation[1] += 3 * (2 - EnemyRedCount)
                elif(Board[AiRedPosition[i] - 1] == 2):
                    AroundExpectation[1] += 6
            if(AiRedPosition[i] % 6 != 5):
                if(Board[AiRedPosition[i] + 1] == 1 ):
                    AroundExpectation[2] += 3 * (2 - EnemyRedCount)
                elif(Board[AiRedPosition[i] + 1] == 2):
                    AroundExpectation[2] += 6
            if(AiRedPosition[i] < 30):
                if(Board[AiRedPosition[i] + 6] == 1):
                    AroundExpectation[3] += 3 * (2 - EnemyRedCount)
                elif(Board[AiRedPosition[i] + 6] == 2):
                    AroundExpectation[3] += 6

            #周囲の敵に食べられる
            if(AiRedPosition[i] > 11):
                if(Board[AiRedPosition[i] - 12] == 1 or Board[AiRedPosition[i] - 12] == 2):
                    AroundExpectation[0] += 2
            if(AiRedPosition[i] % 6 > 2):
                if(Board[AiRedPosition[i] - 2] == 1 or Board[AiRedPosition[i] - 2] == 2):
                    AroundExpectation[1] += 2
            if(AiRedPosition[i] % 6 < 4):
                if(Board[AiRedPosition[i] + 2] == 1 or Board[AiRedPosition[i] + 2] == 2):
                    AroundExpectation[2] += 2
            if(AiRedPosition[i] < 24):
                if(Board[AiRedPosition[i] + 12] == 1 or Board[AiRedPosition[i] + 12] == 2):
                    AroundExpectation[3] += 2
            if(AiRedPosition[i] > 5):
                if(AiRedPosition[i] % 6 != 0):
                    if(Board[AiRedPosition[i] - 7] == 1 or Board[AiRedPosition[i] - 7] == 2):
                        AroundExpectation[0] += 2
                        AroundExpectation[1] += 2
                if(AiRedPosition[i] % 6 != 5):
                    if(Board[AiRedPosition[i] - 5] == 1 or Board[AiRedPosition[i] - 5] == 2):
                        AroundExpectation[0] += 2
                        AroundExpectation[2] += 2
            if(AiRedPosition[i] < 30):
                if(AiRedPosition[i] % 6 != 0):
                    if(Board[AiRedPosition[i] + 5] == 1 or Board[AiRedPosition[i] + 5] == 2):
                        AroundExpectation[1] += 2
                        AroundExpectation[3] += 2
                if(AiRedPosition[i] % 6 != 5):
                    if(Board[AiRedPosition[i] + 7] == 1 or Board[AiRedPosition[i] + 7] == 2):
                        AroundExpectation[2] += 2
                        AroundExpectation[3] += 2

            #移動できるか            
            if(AiRedPosition[i] > 5):
                if(Board[AiRedPosition[i] - 6] == 3 or Board[AiRedPosition[i] - 6] == 4):
                   AroundExpectation[0] = None
            else:
                AroundExpectation[0] = None
            if(AiRedPosition[i] % 6 != 0):
                if(Board[AiRedPosition[i] - 1] == 3 or Board[AiRedPosition[i] - 1] == 4):
                    AroundExpectation[1] = None
            else:
                AroundExpectation[1] = None
            if(AiRedPosition[i] % 6 != 5):
                if(Board[AiRedPosition[i] + 1] == 3 or Board[AiRedPosition[i] + 1] == 4):
                    AroundExpectation[2] = None
            else:
                AroundExpectation[2] = None
            if(AiRedPosition[i] < 30):
                if(Board[AiRedPosition[i] + 6] == 3 or Board[AiRedPosition[i] + 6] == 4):
                    AroundExpectation[3] = None
            else:
                AroundExpectation[3] = None
        
            #期待値の最大と比較
            for j in range(4):
                if(AroundExpectation[j] is not None):
                    if(AroundExpectation[j] > MaxExpectation):
                        MaxExpectation = AroundExpectation[j]
                        DecidePiece[0] = 1
                        DecidePiece[1] = i+1
                        DecidePiece[2] = j+1

            print(str(AroundExpectation))
            print(str(DecidePiece))

            #ループごとの期待値初期化
            AroundExpectation = [0] * 4
        

    #青処理
    for i in range(4):
        if(AiBluePosition[i] is not None):


            #前にプラス
            if(AiBluePosition[i] > 5):
                AroundExpectation[0] += 2
        
            #横にプラス(近い端優先で)
            if(AiBluePosition[i] < 3):
                if(AiBluePosition[i] % 6 != 0):
                    AroundExpectation[1] += 1
                else:
                    AroundExpectation[2] += 1
            else:
                if(AiBluePosition[i] % 6 != 5):
                    AroundExpectation[2] += 1
                else:
                    AroundExpectation[1] += 1
        
            #周囲の敵を食べる
            if(AiBluePosition[i] > 5):
                if(Board[AiBluePosition[i] - 6] == 1):
                    AroundExpectation[0] += 3 * (2 - EnemyRedCount)
                elif(Board[AiBluePosition[i] - 6] == 2):
                    AroundExpectation[0] += 6
            if(AiBluePosition[i] % 6 != 0):
                if(Board[AiBluePosition[i] - 1] == 1):
                    AroundExpectation[1] += 3 * (2 - EnemyRedCount)
                elif(Board[AiBluePosition[i] - 1] == 2):
                    AroundExpectation[1] += 6
            if(AiBluePosition[i] % 6 != 5):
                if(Board[AiBluePosition[i] + 1] == 1 ):
                    AroundExpectation[2] += 3 * (2 - EnemyRedCount)
                elif(Board[AiBluePosition[i] + 1] == 2):
                    AroundExpectation[2] += 6
            if(AiBluePosition[i] < 30):
                if(Board[AiBluePosition[i] + 6] == 1):
                    AroundExpectation[3] += 3 * (2 - EnemyRedCount)
                elif(Board[AiBluePosition[i] + 6] == 2):
                    AroundExpectation[3] += 6

            #周囲の敵から逃げる
            if(AiBluePosition[i] > 11):
                if(Board[AiBluePosition[i] - 12] == 1 or Board[AiBluePosition[i] - 12] == 2):
                    AroundExpectation[3] += MyBlueCount * MyBlueCount
            if(AiBluePosition[i] % 6 > 2):
                if(Board[AiBluePosition[i] - 2] == 1 or Board[AiBluePosition[i] - 2] == 2):
                    AroundExpectation[2] += MyBlueCount * MyBlueCount
            if(AiBluePosition[i] % 6 < 4):
                if(Board[AiBluePosition[i] + 2] == 1 or Board[AiBluePosition[i] + 2] == 2):
                    AroundExpectation[1] += MyBlueCount * MyBlueCount
            if(AiBluePosition[i] < 24):
                if(Board[AiBluePosition[i] + 12] == 1 or Board[AiBluePosition[i] + 12] == 2):
                    AroundExpectation[0] += MyBlueCount * MyBlueCount
            if(AiBluePosition[i] > 5):
                if(AiBluePosition[i] % 6 != 0):
                    if(Board[AiBluePosition[i] - 7] == 1 or Board[AiBluePosition[i] - 7] == 2):
                        AroundExpectation[2] += MyBlueCount * MyBlueCount
                        AroundExpectation[3] += MyBlueCount * MyBlueCount
                if(AiBluePosition[i] % 6 != 5):
                    if(Board[AiBluePosition[i] - 5] == 1 or Board[AiBluePosition[i] - 5] == 2):
                        AroundExpectation[1] += MyBlueCount * MyBlueCount
                        AroundExpectation[3] += MyBlueCount * MyBlueCount
            if(AiBluePosition[i] < 30):
                if(AiBluePosition[i] % 6 != 0):
                    if(Board[AiBluePosition[i] + 5] == 1 or Board[AiBluePosition[i] + 5] == 2):
                        AroundExpectation[0] += MyBlueCount * MyBlueCount
                        AroundExpectation[2] += MyBlueCount * MyBlueCount
                if(AiBluePosition[i] % 6 != 5):
                    if(Board[AiBluePosition[i] + 7] == 1 or Board[AiBluePosition[i] + 7] == 2):
                        AroundExpectation[0] += MyBlueCount * MyBlueCount
                        AroundExpectation[1] += MyBlueCount * MyBlueCount

            #移動可能か
            if(AiBluePosition[i] > 5):
                if(Board[AiBluePosition[i] - 6] == 3 or Board[AiBluePosition[i] - 6] == 4):
                   AroundExpectation[0] = None
            else:
                AroundExpectation[0] = None
            if(AiBluePosition[i] % 6 != 0):
                if(Board[AiBluePosition[i] - 1] == 3 or Board[AiBluePosition[i] - 1] == 4):
                    AroundExpectation[1] = None
            else:
                AroundExpectation[1] = None
            if(AiBluePosition[i] % 6 != 5):
                if(Board[AiBluePosition[i] + 1] == 3 or Board[AiBluePosition[i] + 1] == 4):
                    AroundExpectation[2] = None
            else:
                AroundExpectation[2] = None
            if(AiBluePosition[i] < 30):
                if(Board[AiBluePosition[i] + 6] == 3 or Board[AiBluePosition[i] + 6] == 4):
                    AroundExpectation[3] = None
            else:
                AroundExpectation[3] = None
            

            #期待値の最大と比較
            for j in range(4):
                if(AroundExpectation[j] is not None):
                    if(AroundExpectation[j] > MaxExpectation):
                        MaxExpectation = AroundExpectation[j]
                        DecidePiece[0] = 2
                        DecidePiece[1] = i+1
                        DecidePiece[2] = j+1

            print(str(AroundExpectation))
            print(str(DecidePiece))

            #ループごとの期待値初期化
            AroundExpectation = [0] * 4
                

    return DecidePiece


#相手の駒予想
def AI_Expect_Piece(MyPosition = [0]*8, MyProbability = [0]*8, MyRedPosition = [0]*4, MyBluePosition = [0]*4):

    #ソート(時間ないのでバブルソート)、変更すべき
    for i in range(8):
        for j in range(7, i, -1):
            if(MyProbability[j] is not None):
                if(MyProbability[j-1] is None or MyProbability[j] > MyProbability[j-1]):
                    MyProbability[j], MyProbability[j-1] = MyProbability[j-1], MyProbability[j]
                    MyPosition[j], MyPosition[j-1] = MyPosition[j-1], MyPosition[j]

    #赤、青を予想
    for i in range(4):
        if(i + MyRedCount < 4):
            MyRedPosition[i] = MyPosition[i]
        else:
            MyRedPosition[i] = None

    for i in range(4):
        if(i + MyBlueCount < 4):
            MyBluePosition[i] = MyPosition[i + 4 - MyRedCount]
        else:
            MyBluePosition[i] = None

    return MyRedPosition, MyBluePosition

    

#ＡＩ移動関数、まとめ
def AI_Move_Piece(Board = [0]*36, AiRedPosition = [0]*4, AiBluePosition = [0]*4, \
                  MyRedPosition = [0]*4, MyBluePosition = [0]*4, GameTurn = 0,\
                  MyPosition = [0]*8, MyProbability = [0]*8, \
                  EnemyRedCount = 0, EnemyBlueCount = 0, \
                  ClickFlag = 0, Counter = 0):

    if(Counter == 1 and ClickFlag == 1):

        Counter = 0
        ClickFlag = 0
        GameTurn += 1

        return AiRedPosition, AiBluePosition, MyRedPosition, MyBluePosition, \
               MyPosition, MyProbability,\
               EnemyRedCount, EnemyBlueCount, GameTurn, ClickFlag, Counter

    #動かす駒決定
    #1:赤(1)青(2), 2:駒選択(1から4), 3:四方向(1:上 2:左 3:右 4:下)
    DecidePiece = [0] + [0] + [0]

    #動くマス位置
    MoveMass = 0
    
    #相手駒の予想
    MyRedPosition, MyBluePosition = AI_Expect_Piece(MyPosition, MyProbability, MyRedPosition, MyBluePosition)

    
    #移動マス決定
    DecidePiece = AI_Blue_Check(AiBluePosition, MyRedPosition, MyBluePosition, DecidePiece)

    if(DecidePiece[0] == 0 and Counter == 0):
        
        DecidePiece = AI_Normal_Move(Board, AiRedPosition, AiBluePosition , DecidePiece)


    if(DecidePiece[0] == 1 and Counter == 0):
        if(DecidePiece[2] == 1):
            MoveMass = AiRedPosition[DecidePiece[1]-1] - 6
        elif(DecidePiece[2] == 2):
            MoveMass = AiRedPosition[DecidePiece[1]-1] - 1
        elif(DecidePiece[2] == 3):
            MoveMass = AiRedPosition[DecidePiece[1]-1] + 1
        elif(DecidePiece[2] == 4):
            MoveMass = AiRedPosition[DecidePiece[1]-1] + 6

        if Board[MoveMass] ==  1:     
            EnemyRedCount += 1
            for i in range(8):
                if(MoveMass == MyPosition[i]):
                    MyPosition[i] = None
        elif Board[MoveMass] == 2:    
            EnemyBlueCount += 1
            for i in range(8):
                if(MoveMass == MyPosition[i]):
                    MyPosition[i] = None

        Board[MoveMass] = Board[AiRedPosition[DecidePiece[1]-1]]
        Board[AiRedPosition[DecidePiece[1]-1]] = 0
        AiRedPosition[DecidePiece[1]-1] = MoveMass
              
    elif(DecidePiece[0] == 2 and Counter == 0):
        if(DecidePiece[2] == 1):
            MoveMass = AiBluePosition[DecidePiece[1]-1] - 6
        elif(DecidePiece[2] == 2):
            MoveMass = AiBluePosition[DecidePiece[1]-1] - 1
        elif(DecidePiece[2] == 3):
            MoveMass = AiBluePosition[DecidePiece[1]-1] + 1
        elif(DecidePiece[2] == 4):
            MoveMass = AiBluePosition[DecidePiece[1]-1] + 6

        if Board[MoveMass] ==  1:     
            EnemyRedCount += 1
            for i in range(8):
                if(MoveMass == MyPosition[i]):
                    MyPosition[i] = None
        elif Board[MoveMass] == 2:    
            EnemyBlueCount += 1
            for i in range(8):
                if(MoveMass == MyPosition[i]):
                    MyPosition[i] = None

        Board[MoveMass] = Board[AiBluePosition[DecidePiece[1]-1]]
        Board[AiBluePosition[DecidePiece[1]-1]] = 0
        AiBluePosition[DecidePiece[1]-1] = MoveMass
                

    ClickFlag = 0
    Counter = 1


    print(str(DecidePiece))


    return AiRedPosition, AiBluePosition, MyRedPosition, MyBluePosition, \
           MyPosition, MyProbability,\
           EnemyRedCount, EnemyBlueCount, GameTurn, ClickFlag, Counter
        


#これ以降がループ部分
while True:
    
    #スクリーンの背景色指定
    screen.fill((255,255,255))


    #ターン表示用if
    if TurnChange == 0:

        #自駒設置部分
        if GameTurn == 0:
            
            if ClickFlag == 1:
                
                Counter, ClickFlag, GameTurn =\
                         Set_Pieces(Board, ClickSquare, Counter, GameTurn,\
                                    MyPosition)

        #ＡＩ駒設置部分
        elif GameTurn == 1:

            if ClickFlag == 1:

                ClickFlag, GameTurn, Counter, AiRedPosition, AiBluePosition =\
                           AI_Set_Pieces(Board, AiSetPieces, ClickFlag, GameTurn, Counter,\
                                         AiRedPosition, AiBluePosition)
                
            
        #これ以降がゲームのメインループ
        else:
            

            if WinFlag == 0:
                
                #脱出による勝利判定
                WinFlag, TwiceWinFlag, WinCount = Twice_Win_Check(Board, WinFlag, TwiceWinFlag, GameTurn, WinCount, ClickFlag)

                if GameTurn % 2 == 0:
                    
                    #駒移動可能範囲測定
                    if (MoveClickFlag == False) and ( -1 < ClickSquare < 36 ) and\
                       (Counter == 0):
                        
                        ClickFlag, MoveSquares, MoveFlag,\
                        MoveClickFlag, MyClickPiece =\
                                   Check_Squares(Board, ClickSquare)

                    #駒移動、ＡＩにおける各駒期待値変動    
                    else:
                            
                        GameTurn , MoveFlag , MoveClickFlag, ClickSquare,\
                        MyRedCount, MyBlueCount,\
                        MyPosition, MyProbability, AiRedPosition, AiBluePosition,\
                        ClickFlag, Counter= \
                                    Move_Piece(Board, ClickSquare, MyClickPiece,\
                                               MoveSquares, GameTurn,\
                                               MyRedCount, MyBlueCount,\
                                               MyPosition, MyProbability,\
                                               AiRedPosition, AiBluePosition,\
                                               ClickFlag, Counter)

                #ＡＩ駒移動        
                elif GameTurn % 2 == 1:

                    if ClickFlag == 1:

                        AiRedPosition, AiBluePosition, MyRedPosition, MyBluePosition, \
                        MyPosition, MyProbability,\
                        EnemyRedCount, EnemyBlueCount, GameTurn, ClickFlag, Counter = \
                            AI_Move_Piece(Board, AiRedPosition, AiBluePosition, \
                                          MyRedPosition, MyBluePosition, GameTurn,\
                                          MyPosition, MyProbability,\
                                          EnemyRedCount, EnemyBlueCount, \
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
        TurnChange = 1
        WinCount = 0
        

    BackGameTurn = GameTurn



    #これ以降画像表示

    #ボードの画像表示
    if TurnChange == 0 and WinFlag == 0:
    
        screen.blit(boardImg, (100,100))

#以下コメントアウトはバグ発生時に使用

#        AiPosition = sysfont.render(str(AiRedPosition), False, (0,0,0))
#        AiPosition2 = sysfont.render(str(AiBluePosition), False, (0,0,0))
#        screen.blit(AiPosition, (800, 300))
#        screen.blit(AiPosition2, (800, 400))
#        AiPositions3 = sysfont.render(str(MyRedPosition), False, (0,0,0))
#        screen.blit(AiPositions3, (800, 500))
#        AiPositions4 = sysfont.render(str(MyBluePosition), False, (0,0,0))
#        screen.blit(AiPositions4, (800, 600))

#        AiPositions5 = sysfont.render(str(TwiceWinFlag), False, (0,0,0))
#        screen.blit(AiPositions5, (800, 100))
#        AiPositions6 = sysfont.render(str(WinFlag), False, (0,0,0))
#        screen.blit(AiPositions6, (850, 100))
#        AiPositions7 = sysfont.render(str(GameTurn), False, (0,0,0))
#        screen.blit(AiPositions7, (800, 200))
        
                
        #ボード上の駒の表示
        for i in range(36):
            
            if Board[i] == 1:
                screen.blit(myredImg, (100 + i%6*100, 100 + i//6*100))
                
            elif Board[i] == 2:
                screen.blit(myblueImg, (100 + i%6*100, 100 + i//6*100))
                
            elif Board[i] == 3:
                screen.blit(enemypieceImg, (100 + i%6*100, 100 + i//6*100))
                
            elif Board[i] == 4:
                screen.blit(enemypieceImg, (100 + i%6*100, 100 + i//6*100))


        #光るマスの表示
        if MoveFlag == 1:
            
            for i in range(4):
                
                if MoveSquares[i] is not None:
                    
                    pygame.draw.rect(screen, (255,255,0),\
                                     Rect(100 + MoveSquares[i] % 6 * 100,\
                                          100 + MoveSquares[i] // 6 * 100,\
                                          100, 100), 5)

        #取った駒の表示
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

        if WinFlag == 1 or WinFlag == 2:
            
                
            if WinFlag == 2:
                screen.blit(TwoWin, (100,300))
                    
            else:
                screen.blit(OneWin, (100,300))

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
            

