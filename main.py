from stateManager import stateManager
import curses
def main():
    """
    scene = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    scene.keypad(True)
    scene.addstr(0,0, "FUCK")
    scene.getkey()
    curses.nocbreak()
    scene.keypad(False)
    curses.echo()
    curses.endwin()
    """
    manager = stateManager()
    manager.pushState("menu")
    while(manager.running):
        manager.draw()
        manager.handleEvents()
        manager.update()
    #manager.cleanUp()
    
if __name__ == "__main__":
    main()