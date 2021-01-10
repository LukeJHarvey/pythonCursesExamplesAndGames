from games.tetris.tetrisPiece import piece
import random
import curses
import math
import copy
class tetris():

    def __init__(self, pWidth = 1, pHeight = 1, x = 10, y = 24):
        self.board = [ [0] * x for _ in range(y)]
        self.pWidth = pWidth
        self.pHeight = pHeight
        self.currPiece = None
        self.clock = 0
        #nextMove = [y,x]
        self.placeNext = False
        self.nextMove = [0,0]
        self.turn = 0

    def newPiece(self, pType, x, y):
        self.currPiece = piece(pType, x, y)
        return self.currPiece

    def pieceDrop(self, pArr: [[]]):
        y = self.currPiece.y
        x = self.currPiece.x
        while(self.moveCheck(pArr, 1, 0, y, x)):
            y += 1
        return (y,x)

    def linecheck(self):
        for i in range(0, len(self.board)):
            delRow = True
            for j in range(0, len(self.board[0])):
                if(self.board[i][j] == 0):
                    delRow = False
            if(delRow):
                self.delRow(i)

    def delRow(self, y):
        prevRow = ([0] * len(self.board[0]), self.board[y-1])[y-1 >= 0]
        for i in range(y, 0, -1):
            prevRow = ([0] * len(self.board[0]), self.board[i-1])[i-1 >= 0] 
            self.board[i] = prevRow

    def place(self):
        posX = self.currPiece.x
        posY = self.currPiece.y
        pieceArr = self.currPiece.getPiece()
        for i in range(0,4):
            for j in range(0,4):
                if(pieceArr[3-i][j] == 1 and posY - i >= 0 and posX + j < len(self.board[0]) and posX + j >= 0):
                    self.board[posY - i][posX + j] = 1
        self.linecheck()
        self.currPiece = None

    def moveCheck(self, pieceArr: [[]], y: int, x: int, posY = -1, posX = -1):
        posY = (posY, self.currPiece.y)[posY == -1]
        posX = (posX, self.currPiece.x)[posX == -1]
        newPosX = posX + x
        newPosY = posY + y
        rows = len(self.board)
        cols = len(self.board[0])
        
        if(posX < 0 and x < 0):
            return False
        if(posY >= rows or newPosY >= rows):
            return False

        for i in range(0,4):
            if(newPosX < 0 and pieceArr[i][0] == 1):
                return False
            for j in range(0,4):
                if(newPosX + j >= cols and pieceArr[i][j] == 1):
                    return False
                if(posY - i < 0 or posY - i >= rows or newPosX + j >= cols or newPosX + j < 0):
                    pass
                elif(self.board[posY - i][newPosX + j] == 1 and pieceArr[3-i][j] == 1):
                    return False
                if(newPosY - i < 0 or newPosY - i >= rows or posX + j >= cols or posX + j < 0):
                    pass
                elif(self.board[newPosY - i][posX + j] == 1 and pieceArr[3-i][j] == 1):
                    return False
        return True
    
    def update(self, delta):
        self.clock += delta
        if(self.clock > 1.5):
            if(self.placeNext):
                self.place()
                self.placeNext = False

        if(self.currPiece == None):
            rand = random.randint(0,len(piece.typeDict)-1)
            pos = [math.floor(len(self.board[0])/2)-2, 3]
            self.currPiece = self.newPiece(list(piece.typeDict.keys())[rand], pos[0], pos[1])
        
        if(self.nextMove[0] != -1):
            if(self.turn != 0):
                self.turn = (0,self.turn)[self.moveCheck(self.currPiece.nextSpin(self.turn), 0, 0)]
            #testing nextMove.x
            if(self.nextMove[1] != 0):
                self.nextMove[1] = (0, self.nextMove[1])[self.moveCheck(self.currPiece.getPiece(), 0, self.nextMove[1])]
            #testing nextMove.y
            if(self.nextMove[0] == 1):
                self.nextMove[0] = (0, self.nextMove[0])[self.moveCheck(self.currPiece.getPiece(), self.nextMove[0], 0)]

            fall = 0
        
            if(self.clock > 1.5):
                fall = (0, 1)[self.moveCheck(self.currPiece.nextSpin(self.turn), self.nextMove[0] + 1, self.nextMove[1])]
            self.currPiece.move(self.nextMove[0] + fall, self.nextMove[1])
            self.currPiece.spin(self.turn)
            if(self.clock > 1.5 and self.pieceDrop(self.currPiece.getPiece())[0] == self.currPiece.y):
                self.placeNext = True
        else:
            x = self.pieceDrop(self.currPiece.getPiece())[0]
            self.currPiece.drop(x)
            self.place()
            self.clock = 0
        
        if(self.clock > 1.5):
            self.clock = 0
        self.nextMove = [0,0]
        self.turn = 0

    def draw(self, window):
        rows, cols = window.getmaxyx()
        hightlightY, hightlightX = (-1,-1)
        if(self.currPiece):
            highlightY, highlightX = self.pieceDrop(self.currPiece.getPiece())
        
        for i in range(0,len(self.board)):
            for j in range(0, len(self.board[0])):
                ch = 'O'
                attr = curses.A_NORMAL
                if(self.board[i][j] != 0 or (self.currPiece and self.currPiece.isThere(i,j))):
                    ch = 'X'
                    attr = curses.A_STANDOUT
                elif(self.currPiece and self.currPiece.isThere(i,j,highlightY,highlightX)):
                    ch = 'Y'
                    attr = curses.A_STANDOUT
                try:
                    for k in range(0, self.pWidth):
                        for k2 in range(0, self.pHeight):
                            window.insstr((i*self.pHeight) + k2, (j*self.pWidth) + k, ch, attr)
                except:
                    raise Exception(str(i) + " " + str(j) + " | " + str(rows) + " " + str(cols))