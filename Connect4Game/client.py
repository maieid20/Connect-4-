import socket
import threading
import numpy as np
import pygame
import sys
import math

host = "127.0.0.1"
port = 7010

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN= (0,255,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COL_COUNT = 7

gameOver = False
turn = True 
flag = 0

sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,port))

def create_thread (target) :
    thread = threading.Thread(target = target)
    thread.daemob = True
    thread.start()

def recieveData ():
    global flag
    global gameOver
    global turn
    while True :
        data = sock.recv(1024).decode()
        dataa = data.split('-')
        row = int(dataa[0])
        col = int(dataa[1])
        if turn == False :
            if isValidLocation (board, col) :
                row = nextOpenRow(board, col)
                dropPiece(board, row, col, 1)
                drawBoard(board)
                flag += 1
                GameOver(board)
                print (str(flag))
                if winning_move(board, 1) :
                    label = myFont.render("Player 1 wins !!", 1, RED)
                    screen.blit (label, (40,10))
                    gameOver = True
                    pygame.display.update()
        if dataa[2] == "YourTurn" :
            turn = True
            print ("Client Turn = "+ str(turn))

create_thread(recieveData)

def createBoard ():
    board = np.zeros((6,7))
    return board

def dropPiece(board, row, col, piece) :
    board[row][col] = piece

def isValidLocation(board, col) :
    return board[ROW_COUNT-1][col] == 0

def nextOpenRow(board, col ) :
    for row in range(ROW_COUNT) :
        if board[row][col] == 0 :
            return row

def printBoard (board) :
    print (np.flip(board, 0))

def GameOver(board) :
    global gameOver
    if flag == 42 and not winning_move(board, 1) and not winning_move(board,2) :
        label = myFont.render("Match Tied !!", 1, GREEN)
        screen.blitt (label, (40,10))
        pygame.display.update()
        pygame.time.wait(3000)
        gameOver = True
        pygame.display.quit()
        sys.exit()

def winning_move(board, piece):
    for c in range(COL_COUNT-3):
        for r in range (ROW_COUNT) :
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece :
                return True

    for c in range(COL_COUNT):
        for r in range (ROW_COUNT-3) :
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece :
                return True

    for c in range(COL_COUNT-3):
        for r in range (ROW_COUNT-3) :
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece :
                return True

    for c in range(COL_COUNT-3):
        for r in range (3, ROW_COUNT) :
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece :
                return True

def drawBoard(board) :
    for c in range (COL_COUNT) :
        for r in range (ROW_COUNT) :
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
    for c in range (COL_COUNT) :
        for r in range (ROW_COUNT) : 
            if board[r][c] == 1 : 
                pygame.draw.circle(screen,RED,(int(c*SQUARE_SIZE+SQUARE_SIZE/2), height - int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
            elif board[r][c] == 2 : 
                pygame.draw.circle(screen,YELLOW,(int(c*SQUARE_SIZE+SQUARE_SIZE/2), height - int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
    pygame.display.update()

board = createBoard()
pygame.init()

SQUARE_SIZE = 80

width = COL_COUNT * SQUARE_SIZE
height = (ROW_COUNT+1)*SQUARE_SIZE

size = (width,height)

RADIUS = int(SQUARE_SIZE/2 -5)

screen=pygame.display.set_mode(size)
drawBoard(board)
pygame.display.update()

myFont=pygame.font.SysFont('monospace',50)

while not gameOver :

    for event in pygame.event.get() :

        if event.type==pygame.QUIT:
            pygame.display.quit()
            sys.exit()

        if event.type==pygame.MOUSEMOTION:
            pygame.draw.rect(screen,BLACK,(0 ,0,width,SQUARE_SIZE))
            posx=event.pos[0]
            if turn==True:
                pygame.draw.circle(screen,YELLOW,(posx,int(SQUARE_SIZE/2)),RADIUS)

        pygame.display.update()

        if event.type==pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,BLACK,(0 ,0,width,SQUARE_SIZE))
            
            if turn==True:
                posX=event.pos[0]
                col=int(math.floor(posX/SQUARE_SIZE))

                if isValidLocation(board,col):
                    row=nextOpenRow(board,col)
                    dropPiece(board,row,col ,2)

                    flag +=1
                    
                    send_data='{}-{}-{}'.format(str(row),str(col),'YourTurn').encode()
                    sock.send(send_data)
                    print(send_data)

                    turn=False
                    
                    GameOver(board)

                    print(str(flag))
                    print(str(turn))

                    if winning_move(board ,2):
                        label=myFont.render('Player 2 wins !!',1,YELLOW)
                        screen.blit(label,(40 ,10))
                        gameOver=True
                        

        drawBoard(board)