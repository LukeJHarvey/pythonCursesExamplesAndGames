import curses, time, datetime, math
from states.state import state
from games.tetris.tetris import tetris
class tetrisState(state):
    def __init__(self, pWidth = 3, pHeight = 2, x = 10, y = 20):
        self.bigView = None
        self.gameView = None
        self.pieceView = None
        self.width = x*pWidth
        self.height = y*pHeight
        self.gameEngine = tetris(pWidth, pHeight, x, y)
        self.lastFrame = datetime.datetime.now()
        pass

    def cleanUp(self):
        pass

    def pause(self):
        pass
    def resume(self):
        pass

    def handleEvents(self, manager):
        i = manager.scene.getch()
        self.gameEngine.nextMove = [0,0]
        self.gameEngine.turn = 0
        if(i == curses.KEY_LEFT or i == ord("a")):
            self.gameEngine.nextMove[1] = -1
        elif(i == curses.KEY_RIGHT or i == ord("d")):
            self.gameEngine.nextMove[1] = 1
        elif(i == curses.KEY_UP or i == ord("w")):
            self.gameEngine.nextMove[0] = -1
        elif(i == curses.KEY_DOWN or i == ord("s")):
            self.gameEngine.nextMove[0] = 1
        elif(i == ord("q")):
            self.gameEngine.turn = -1
        elif(i == ord("e")):
            self.gameEngine.turn = 1

    def update(self, manager):
        delta = (datetime.datetime.now() - self.lastFrame).total_seconds()
        self.lastFrame = datetime.datetime.now()
        self.gameEngine.update(delta)
        
        pass
    def draw(self, manager):
        if(not self.bigView):
            self.initWindows(manager)

        for i in range(0,self.height+2):
            for j in range(0, self.width+2):
                if(j == 0 or j == self.width+1):
                    self.bigView.insstr(i, j, "|")
                elif(i == 0 or i == self.height+1):
                    self.bigView.insstr(i, j, "=")
        pSize = [self.gameEngine.pHeight, self.gameEngine.pWidth]
        '''
        for i in range(0, 3 + pSize[0]):
            for j in range(0, 3 + pSize[1]):
                if(j == 0 or j == pSize[1]+3):
                    self.pieceView.insstr(i, j, "|")
                elif(i == 0 or i == pSize[0]-1):
                    self.pieceView.insstr(i, j, "=")
                elif(self.gameEngine.currPiece):
                    p = self.gameEngine.currPiece
                    if(i == pSize[0]-1 and j == 1):
                        x = (0,1)[self.gameEngine.moveCheck(p.nextSpin(1), 0, 0)]
                        self.pieceView.addstr(i, 0, str(x))
                        pass
                    else:
                        pos = [i-1, j-1]
                        Y = (math.floor(pos[0]/pSize[0]), (pos[0]) % (pSize[0]))
                        X = (math.floor(pos[1]/pSize[1]), (pos[1]) % (pSize[1]))
                        try:
                            y = pos[0] - Y[1]
                            x = pos[1] - X[1]
                            if(Y[0] != 0):
                                y = (pos[0]-Y[1])/Y[0]
                            if(X[0] != 0):
                                x = (pos[1]-X[1])/X[0]
                            y = int(y)
                            x = int(x)
                        except: 
                            raise Exception(str(pos[0]) + " " + str(Y[0]) + " " + str(Y[1]) + " " + str(pos[1]) + " " + str(X[0]) + " " + str(X[1]))

                        ch = (" ", "X")[p.getPiece()[y][x] == 1]
                        self.pieceView.insstr(i, j, ch)

        '''
        self.gameEngine.draw(self.gameView)
        manager.scene.touchwin()
        self.bigView.touchwin()
        self.pieceView.refresh()
        self.bigView.refresh()
        self.gameView.refresh()
        manager.scene.refresh()
        pass

    def initWindows(self, manager):
        curses.resizeterm(self.height+2, self.width+20)
        manager.scene.clear()
        manager.scene.refresh()
        curses.newwin(self.height, self.width, 0, 4)
        self.bigView = manager.scene.subwin(self.height+2, self.width+2, 0, 0)
        self.gameView = self.bigView.subwin(self.height,self.width, 1, 1)
        self.pieceView = manager.scene.subwin(3 + (4*self.gameEngine.pHeight), 2 + (4*self.gameEngine.pWidth), 0, self.width+2)