from states import menuState, tetrisState, progressState
import curses

class stateManager:
    stateDict = {
        "menu": menuState.menuState,
        "prog": progressState.progressState,
        "tetris": tetrisState.tetrisState
    }
    def __init__(self):
        self.stateList = []
        self.currentState = None
        self.scene = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        self.scene.nodelay(True)
        self.scene.keypad(True)
        self.running = True
        self.initColor()
        self.rows, self.cols = self.scene.getmaxyx()

    def cleanUp(self):
        curses.nocbreak()
        self.scene.keypad(False)
        curses.echo()
        curses.endwin()

    def initColor(self):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)


    def changeState(self, state):
        newState = self.stateDict.get(state, None)
        if(newState != None):
            if(self.stateList != []):
                self.stateList[-1].cleanUp()
                self.stateList.append(newState())
            else:
                self.stateList.append(newState())
        else:
            print("State: " + state + " not found")

    def pushState(self, state):
        newState = self.stateDict.get(state, None)
        if(newState != None):
            self.stateList.append(newState())
        else:
            print("State: " + state + " not found")

    def popState(self):
        if(self.stateList != []):
            self.stateList.pop()
        


    def handleEvents(self):
        self.stateList[-1].handleEvents(self)
    def update(self):
        if(self.stateList != []):
            self.stateList[-1].update(self)
            self.handleEvents()
    def draw(self):
        if(self.stateList != []):
            self.stateList[-1].draw(self)
        #self.scene.addstr(11, 0, str(len(self.stateList)), curses.A_NORMAL)
