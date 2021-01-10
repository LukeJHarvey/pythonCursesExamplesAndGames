class piece():
    typeDict = {
        "T": [
            [
                [0,0,0,0],
                [0,0,0,0],
                [0,1,0,0],
                [1,1,1,0]
            ],
            [
                [0,0,0,0],
                [0,1,0,0],
                [0,1,1,0],
                [0,1,0,0]
            ],
            [
                [0,0,0,0],
                [0,0,0,0],
                [1,1,1,0],
                [0,1,0,0]
            ],
            [
                [0,0,0,0],
                [0,1,0,0],
                [1,1,0,0],
                [0,1,0,0]
            ]
        ],
        "L": [
            [
                [0,0,0,0],
                [0,1,0,0],
                [0,1,0,0],
                [0,1,1,0]
            ],
            [
                [0,0,0,0],
                [0,0,0,0],
                [1,1,1,0],
                [1,0,0,0]
            ],
            [
                [0,0,0,0],
                [0,1,1,0],
                [0,0,1,0],
                [0,0,1,0]
            ],
            [
                [0,0,0,0],
                [0,0,0,0],
                [0,0,1,0],
                [1,1,1,0]
            ]
        ],
        "J": [
            [
                [0,0,0,0],
                [0,0,1,0],
                [0,0,1,0],
                [0,1,1,0]
            ],
            [
                [0,0,0,0],
                [0,0,0,0],
                [1,0,0,0],
                [1,1,1,0]
            ],
            [
                [0,0,0,0],
                [0,1,1,0],
                [0,1,0,0],
                [0,1,0,0]
            ],
            [
                [0,0,0,0],
                [0,0,0,0],
                [1,1,1,0],
                [0,0,1,0]
            ]
        ],
        "Z": [
            [
                [0,0,0,0],
                [0,0,0,0],
                [1,1,0,0],
                [0,1,1,0]
            ],
            [
                [0,0,0,0],
                [0,0,1,0],
                [0,1,1,0],
                [0,1,0,0]
            ]
        ],
        "S": [
            [
                [0,0,0,0],
                [0,0,0,0],
                [0,1,1,0],
                [1,1,0,0]
            ],
            [
                [0,0,0,0],
                [1,0,0,0],
                [1,1,0,0],
                [0,1,0,0]
            ]
        ],
        "I": [
            [
                [0,1,0,0],
                [0,1,0,0],
                [0,1,0,0],
                [0,1,0,0]
            ],
            [
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [1,1,1,1]
            ]
        ],
        "O": [
            [
                [0,0,0,0],
                [0,0,0,0],
                [0,1,1,0],
                [0,1,1,0]
            ]
        ]
    }
    def __init__(self, pType, y = 0, x = 0):
        piece = self.typeDict.get(pType, None)
        self.arr = self.typeDict.get('T')
        self.curr = 0
        self.x = x
        self.y = y
        self.start = 0
        if(piece != None):
            self.arr = piece
            if(piece != self.typeDict.get("I", None)):
                if(piece != self.typeDict.get("J", None) and piece != self.typeDict.get("L", None)):
                    self.start = 2
                else:
                    self.start = 1
        self.move(-self.start,0)
    def spin(self, direction):
        if(self.curr + direction >= len(self.arr)):
            self.curr = 0
        elif(self.curr + direction < 0):
            self.curr = len(self.arr)-1
        else:
            self.curr += direction
            
        return self.arr[self.curr]

    def nextSpin(self, direction):
        spin = self.curr
        if(spin + direction >= len(self.arr)):
            spin = 0
        elif(spin + direction < 0):
            spin = len(self.arr)-1
        else:
            spin += direction
        
        return self.arr[spin]

    def move(self, y, x):
        self.x += x
        self.y += y
        return (self.x, self.y)

    def drop(self, y = 0):
        self.y = y
        return (self.x, self.y)

    def getPiece(self):
        return self.arr[self.curr]
    
    def isThere(self, y, x, posY = -1, posX = -1):
        posY = (posY, self.y)[posY == -1]
        posX = (posX, self.x)[posX == -1]
        
        posY = y - posY + 3
        posX = x - posX
        if(posX > 3 or posX < 0 or posY > 3 or posY < 0):
            return False
        else:
            if(self.getPiece()[posY][posX] == 1):
                return True
            else:
                return False
