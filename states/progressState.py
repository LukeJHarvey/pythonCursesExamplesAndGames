from states.state import state
from examples.progressBar import progressClassic, progressClassicColor, progressChasing
import curses
import time
class progressState(state):
    def __init__(self):
        self.reverse = False
        self.classic = progressClassic("Classic", 100)
        self.classicColor = progressClassicColor("Color", 100)
        self.progressChasing = progressChasing("Chase", 100)

    def cleanUp(self):
        pass

    def pause(self):
        pass
    def resume(self):
        pass

    def handleEvents(self, manager):
        time.sleep(.05)
        pass
    def update(self, manager):
        if(self.classic.progress == 100 or self.classic.progress == 0):
            self.reverse = not self.reverse
        change = (-1, 1)[not self.reverse]
        self.classic.addProgress(change)
        self.classicColor.addProgress(change)
        self.progressChasing.addProgress(change)
        pass
    def draw(self, manager):
        self.classic.draw(manager.scene, manager.cols, 0)
        self.classicColor.draw(manager.scene, manager.cols, 1)
        self.progressChasing.draw(manager.scene, manager.cols, 2)
        manager.scene.refresh()
        pass